# coding: utf8
from __future__ import unicode_literals
import sys
from collections import defaultdict
import re
from itertools import izip_longest

from sqlalchemy import Index

from clld.scripts.util import (
    initializedb, Data, add_language_codes, glottocodes_by_isocode,
)
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import with_collkey_ddl, collkey
from clld.lib.sfm import Dictionary, Entry
from clld.util import nfilter, slug

import csd
from csd import models
from csd.scripts.util import PS, SD, _LANGUAGES, normalize_sid, get_sources


TXT = 'CSD_RLR_Master_version_28final.txt'


def normalize_comma_separated(s, d, lower=False):
    if not s:
        return
    chunks = nfilter([_s.strip() for _s in s.split(',')])
    return ', '.join(
        d.get(_s.lower(), _s.lower() if lower else _s) for _s in chunks)


LANGUAGES = {t[0]: list(t)[1:] for t in _LANGUAGES}

# The following pattern is used to determine markers with language specific content:
MARKER_PATTERN = re.compile(
    '(?P<lang>%s)(?P<key>oo|me|cm|so|cf|_org)$' % '|'.join(LANGUAGES.keys()))
SEP_PATTERN = re.compile(',|;')
SID_PATTERN = re.compile('(?P<key>JGT92|((\(|[a-zA-Z])[\)a-zA-Z\+\s&\./]*))((\-|:)\s*(?P<year>[0-9]{4}:)?\s*(?P<pages>[0-9]+[a-z]*(\.[0-9]+)?)?)?(\s*\(\?\))?$')


class CsdEntry(Entry):
    def append(self, item):
        m, v = item
        #try:
            #assert len(v.split('|')) % 2 == 1
            #assert len(v.split('"')) % 2 == 1
            #assert v.count('(') == v.count(')')
            #assert v.count('[') == v.count(']')
            #assert v.count('{') == v.count('}')
            #assert len(re.findall("(^|\s)'", v)) == len(re.findall("'($|\s)", v))
        #except:
            #print m
            #print v.encode("utf8")
            #print
        item = ({
                    #'psi': 'psioo',
                    #'or': 'psi',
                    #'or_org': 'psi_org',
                    #'orso': 'psiso'
                    }.get(m, m), v)
        Entry.append(self, item)

    def language_chunks(self):
        """

        :return: yields dictionaries where the value of 'forms' are the phonetic siouan\
        forms for a particular language.
        """
        data = defaultdict(list)
        for k, v in self:
            if k in LANGUAGES:
                # a language marker starts a new chunk.
                if data.get('forms') or data.get('oo'):
                    yield data
                data = defaultdict(list)
                data.update(language=k, forms=v or None)
            else:
                match = MARKER_PATTERN.match(k)
                if match:
                    lang = match.group('lang')
                    if 'language' in data and lang != data['language']:
                        # a language-specific-data marker may also start a new chunk.
                        yield data
                        data = defaultdict(list)
                        data.update(language=lang, forms=None)
                    data[match.group('key')].append(v)
                else:
                    if k == 'or':
                        if data:
                            data['or'].append(v)
        if data.get('forms') or data.get('oo'):
            yield data

    def get_words(self):
        res = defaultdict(list)
        for chunk in self.language_chunks():
            #chunk['so'] = nfilter(
            #    [s.strip() for s in SEP_PATTERN.split(chunk.get('so', ''))])
            if 'language' in chunk:
                res[chunk['language']].append(chunk)
        return res


with_collkey_ddl()


def main(args):
    sources = get_sources(args)
    Index('ducet1', collkey(common.Value.name)).create(DBSession.bind)
    Index('ducet2', collkey(models.Counterpart.phonetic)).create(DBSession.bind)
    data = Data()
    glottocodes, geocoords = {}, defaultdict(lambda: (None, None))
    for k, v in glottocodes_by_isocode(
            'postgresql://robert@/glottolog3',
            cols=['id', 'latitude', 'longitude']).items():
        glottocodes[k] = v[0]
        geocoords[k] = (v[1], v[2])
    geocoords['win'] = (43.50, -88.50)

    dataset = common.Dataset(
        id=csd.__name__,
        name="Comparative Siouan Dictionary",
        description="Comparative Siouan Dictionary",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        contact='iren.hartmann@gmail.com',
        domain='csd.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)
    contrib = common.Contribution(id='csd', name=dataset.name)
    for i, spec in enumerate([
        ('Robert L. Rankin', True),
        ('Richard T. Carter', True),
        ('A. Wesley Jones', True),
        ('John E. Koontz', True),
        ('David S. Rood', True),
        ('Iren Hartmann', True),
    ]):
        name, primary = spec
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i, primary=primary))

    d = Dictionary(
        args.data_file(TXT),
        entry_impl=CsdEntry,
        entry_sep='\\lx ')
    d.entries = list(filter(lambda r: r.get('lx'), d.entries))[1:]
    print(len(d.entries))

    for i, v in enumerate(_LANGUAGES):
        l = data.add(
            models.Languoid, v[0],
            id=v[0],
            name=v[1],
            ord=i,
            color=v[4].lower(),
            proto=v[0].startswith('p') and len(v[0]) == 3,
            latitude=geocoords[v[2]][0],
            longitude=geocoords[v[2]][1],
            parent=data['Languoid'].get(v[5]))
        if v[2]:
            add_language_codes(data, l, v[2], glottocodes=glottocodes)
        if l.id == 'pn':
            l.latitude, l.longitude = (42.75, -98.03)
        if l.id == 'op':
            l.latitude, l.longitude = (43.5, -96.6)
        if l.id == 'mo':
            l.latitude, l.longitude = (40.05, -95.52)

    pnames = set()

    def _get(d, marker):
        _l = set(nfilter(d.get(marker, [])))
        if _l:
            _l = list(_l)
            if marker not in ['oo', 'or']:
                assert len(_l) == 1
                _l = _l[0]
            return _l

    def add_counterpart(d, vs, id,
                        phonetic,  # forms
                        cognate,  # oo
                        me, cm, so, org):
        assert phonetic or cognate

        if not cognate:
            if vs.language.proto:
                cognate = phonetic
                phonetic = None
            else:
                cognate = '[%s]' % phonetic
        m = models.Counterpart(
            id=id,
            name=cognate,
            phonetic=phonetic,
            description=me or '[%s]' % vs.parameter.name,
            comment=cm,
            original_entry=org,
            other_reconstructions='; '.join(_get(d, 'or') or []) if vs.language.id == 'psi' else None,
            valueset=vs)
        if so:
            for sid in nfilter([s.strip() for s in SEP_PATTERN.split(so or '')]):
                match = SID_PATTERN.match(sid)
                if not match:
                    continue

                name = sid
                sid = normalize_sid(match.group('key'))
                source = data['Source'].get(sid)
                if not source:
                    if sid in sources:
                        s = sources[sid]
                        source = data.add(
                            common.Source, sid,
                            id=sid,
                            name=s['Name'],
                            description=s.get('Title', s['citation']),
                            author=s.get('Author'),
                            title=s.get('Title'),
                            year=s.get('Year'),
                        )
                    else:
                        source = data.add(common.Source, sid, id=sid, name=name)
                m.references.append(models.ValueReference(
                    source=source, description=match.group('pages')))

    for i, entry in enumerate(sorted(d.entries, key=lambda d: d.get('lx'), reverse=True)):
        lemma = entry.get('lx')
        if not lemma or not lemma.strip():
            continue
        pname = lemma
        j = 1
        while pname in pnames:
            pname = '%s (%s)' % (lemma, j)
            j += 1
        pnames.add(pname)
        contrib = data.add(
            common.Contribution, pname, id=str(i + 1), name='Entry "%s"' % pname)
        meaning = data.add(
            models.Entry, pname,
            id=str(i + 1),
            name=pname,
            contribution=contrib,
            description=entry.get('com'),
            psi_reconstruction_with_root_extension_code=entry.get('lxcm'),
            sd=normalize_comma_separated(entry.get('sd'), SD, lower=True),
            ps=normalize_comma_separated(entry.get('ps'), PS),
            othlgs='\n---\n'.join(entry.getall('othlgs')))
        if meaning.description:
            meaning.description = meaning.description.replace('.\n', '.\n\n')

        for lid, words in entry.get_words().items():
            vsid = '%s-%s' % (lid, meaning.id)
            vs = data.add(
                common.ValueSet, vsid,
                id=vsid,
                parameter=meaning,
                contribution=contrib,
                language=data['Languoid'][lid])

            for j, d in enumerate(words):
                looped = False

                for k, (oo, me, so, cm, org) in enumerate(izip_longest(
                        *[d.get(_m, []) for _m in 'oo me so cm _org'.split()])):
                    if not oo:
                        continue
                    looped = True
                    add_counterpart(d,
                        vs,
                        '%s-%s-%s' % (vsid, j + 1, k + 1),
                        d['forms'],
                        oo,
                        me,
                        cm,
                        so,
                        org)

                if not looped:  # not oo
                    if not d['forms']:
                        print '--->', d
                        continue
                    add_counterpart(d,
                        vs,
                        '%s-%s-%s' % (vsid, j + 1, 1),
                        d['forms'],
                        '; '.join(_get(d, 'oo') or []),
                        _get(d, 'me'),
                        _get(d, 'cm'),
                        _get(d, 'so'),
                        _get(d, '_org'))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    entries = {e.name.lower(): e for e in DBSession.query(models.Entry)}
    hit, miss = [], []

    def lemma_repl(match):
        label = match.group('lemma').strip()
        if label.endswith(','):
            label = label[:-1].strip()
        lookup = re.sub('\s+', ' ', label.lower())
        if lookup in entries:
            label = "**%s**" % entries[lookup].id
            hit.append(label)
        elif match.group('cf'):
            print ("    '%s'" % label).encode('utf8')
            miss.append(label)
        label = "‘%s’" % label
        if match.group('cf'):
            label = 'Cf. %s' % label
        return label

    lemma_pattern = re.compile("(?P<cf>Cf\.\s*)?‘(?P<lemma>[^’]+)’", re.MULTILINE)

    def language_repl(m):
        return '**%s**' % m.group('id')

    language_pattern = re.compile('(?P<id>%s)' % '|'.join(k.upper() for k in LANGUAGES.keys()))

    for entry in entries.values():
        if entry.description:
            #print ('\\lx %s' % entry.name).encode('utf8')
            entry.description = lemma_pattern.sub(lemma_repl, entry.description)
            entry.description = language_pattern.sub(language_repl, entry.description)
    print 'hits:', len(hit)
    print 'miss:', len(miss)

    def level(l):
        _level = 0
        while l.parent:
            _level += 1
            l = l.parent
        return _level

    for lang in DBSession.query(models.Languoid):
        lang.level = level(lang)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache, bootstrap=True)
    sys.exit(0)
