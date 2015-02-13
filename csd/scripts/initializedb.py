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
from csd.scripts.util import PS, SD, SOURCES


def normalize_sid(sid):
    return slug(sid.replace('+', 'and').replace('&', 'and'))

for sid in list(SOURCES.keys()):
    SOURCES[normalize_sid(sid)] = SOURCES[sid]


def normalize_comma_separated(s, d, lower=False):
    if not s:
        return
    chunks = nfilter([_s.strip() for _s in s.split(',')])
    return ', '.join(
        d.get(_s.lower(), _s.lower() if lower else _s) for _s in chunks)


#
# TODO: color-code lineages!
#
_LANGUAGES = [
    ('psc', 'Proto-Siouan-Catawba', None, 'siou1252', 'f0fff0'),
    ('psi', 'Proto-Siouan', 'sio', 'core1249', 'f0fff0'),

    ('pch', 'Proto-Crow-Hidatsa', None, 'miss1252', '87ceff'),
    ('cr', 'Crow', 'cro', 'crow1244', 'b0e2ff'),
    ('hi', 'Hidatasa', 'hid', 'hida1246', 'b0e2ff'),

    ('pma', 'Proto-Mandan', None, None, '7fff00'),
    ('ma', 'Mandan', 'mhq', 'mand1446', 'c0ff3e'),

    ('pmv', 'Proto-Mississipi-Valley', None, 'miss1254', 'f0fff0'),

    ('pda', 'Proto-Dakota', None, 'dako1257', 'ff83fa'),
    ('la', 'Lakota', 'lkt', 'lako1247', 'ffbbff'),
    ('da', 'Dakota', 'dak', 'dako1258', 'ffbbff'),
    ('as', 'Assiniboine', 'asb', 'assi1247', 'ffbbff'),
    ('ya', 'Yanktonai', 'dak', 'dako1258', 'ffbbff'),
    ('sa', 'Santee-Sisseton', 'dak', 'dako1258', 'ffbbff'),
    ('st', 'Stoney', 'sto', 'ston1242', 'ffbbff'),
    ('sv', 'Sioux-Valley', None, None, 'ffbbff'),

    ('pwc', 'Proto-Hoocąk-Chiwere', None, 'winn1245', 'ff0000'),
    ('ch', 'Chiwere', 'iow', 'iowa1245', 'ff4500'),
    ('io', 'Ioway', 'iow', 'iowa1245', 'ff4500'),
    ('ot', 'Otoe', 'iow', 'iowa1245', 'ff4500'),
    ('wi', 'Hoocąk', 'win', 'hoch1243', 'ff4500'),

    ('pdh', 'Proto-Dhegiha', None, 'dheg1241', 'ffff00'),
    ('om', 'Omaha', 'oma', 'omah1247', 'fff68f'),
    ('op', 'Omaha-Ponca', 'oma', 'omah1247', 'fff68f'),
    ('pn', 'Ponca', 'oma', 'omah12477', 'fff68f'),
    ('po', 'Ponca', 'oma', 'omah1247', 'fff68f'),
    ('ks', 'Kanza/Kaw', 'ksk', 'kans1243', 'fff68f'),
    ('os', 'Osage', 'osa', 'osag1243', 'fff68f'),
    ('qu', 'Quapaw', 'qua', 'quap1242', 'fff68f'),

    ('pbo', 'Proto-Biloxi-Ofo', None, 'bilo1247', 'ffb90f'),
    ('bi', 'Biloxi', 'bll', 'bilo1248', 'ffd700'),
    ('of', 'Ofo', 'ofo', 'ofoo1242', 'ffd700'),
    ('tu', 'Tutelo', 'tta', 'tute1247', 'ffd700'),
    ('sp', 'Saponi', 'tta', 'tute1247', 'ffd700'),

    ('pca', 'Proto-Catawba', None, 'cata1285', 'b5b5b5'),
    ('ca', 'Catawba', 'chc', 'cata1286', 'b5b5b5'),
    ('wo', 'Woccon', 'xwc', 'wocc1242', 'b5b5b5'),
]
LANGUAGES = {t[0]: list(t)[1:] for t in _LANGUAGES}

MARKER_PATTERN = re.compile(
    '(?P<lang>%s)(?P<key>_ih|oo|me|cm|so|cf|_org)$' % '|'.join(LANGUAGES.keys()))
SEP_PATTERN = re.compile(',|;')
SID_PATTERN = re.compile('(?P<key>JGT92|((\(|[a-zA-Z])[\)a-zA-Z\+\s&\./]*))((\-|:)\s*(?P<year>[0-9]{4}:)?\s*(?P<pages>[0-9]+[a-z]*(\.[0-9]+)?)?)?(\s*\(\?\))?$')


class CsdEntry(Entry):
    def language_chunks(self):
        data = defaultdict(list)
        for k, v in self:
            if k in LANGUAGES:
                if data.get('forms') or data.get('oo') or data.get('_ih'):
                    yield data
                data = defaultdict(list)
                data.update(language=k, forms=v)
            else:
                match = MARKER_PATTERN.match(k)
                if match:
                    lang = match.group('lang')
                    if 'language' in data and lang != data['language']:
                        yield data
                        data = defaultdict(list)
                        data.update(language=lang, forms=None)
                    data[match.group('key')].append(v)
                else:
                    if k == 'or':
                        if data:
                            data['or'].append(v)
        if data.get('forms') or data.get('oo') or data.get('_ih'):
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
    Index('ducet', collkey(common.Value.name)).create(DBSession.bind)
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
        license="http://creativecommons.org/licenses/by/3.0/",
        domain='csd.clld.org')
    DBSession.add(dataset)
    contrib = common.Contribution(id='csd', name=dataset.name)

    for i, spec in enumerate([
        ('Richard T. Carter', True),
        ('A. Wesley Jones', True),
        ('Robert L. Rankin', True),
        ('John E. Koontz', False),
        ('David S. Rood', False),
    ]):
        name, primary = spec
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i, primary=primary))

    d = Dictionary(
        args.data_file('CSD_RLR_Master_version_21.txt'),
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
            color=v[4],
            proto=v[1].startswith('Proto-'),
            latitude=geocoords[v[2]][0],
            longitude=geocoords[v[2]][1])
        if v[2]:
            add_language_codes(data, l, v[2], glottocodes=glottocodes)

    pnames = set()
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
            sd=normalize_comma_separated(entry.get('sd'), SD, lower=True),
            ps=normalize_comma_separated(entry.get('ps'), PS))

        for lid, words in entry.get_words().items():
            vsid = '%s-%s' % (lid, meaning.id)
            vs = data.add(
                common.ValueSet, vsid,
                id=vsid,
                parameter=meaning,
                contribution=contrib,
                language=data['Languoid'][lid])

            for j, d in enumerate(words):
                _l = lambda _m: d.get(m, [])
                looped = False

                for k, t in enumerate(izip_longest(
                        *[d.get(_m, []) for _m in '_ih oo me so cm'.split()])):
                    ih, oo, me, so, cm = t
                    oo = oo or ih
                    if not oo:
                        continue
                    looped = True
                    m = models.Counterpart(
                        id='%s-%s-%s' % (vsid, j + 1, k + 1),
                        name=d['forms'] or oo,
                        altform=oo if d['forms'] else None,
                        description=me or '[%s]' % vs.parameter.name,
                        comment=cm,
                        valueset=vs)
                    for sid in nfilter([s.strip() for s in SEP_PATTERN.split(so or '')]):
                        match = SID_PATTERN.match(sid)
                        if not match:
                            #print sid
                            continue

                        name = sid
                        sid = normalize_sid(match.group('key'))
                        source = data['Source'].get(sid)
                        if not source:
                            source = data.add(
                                common.Source, sid,
                                id=sid,
                                name=SOURCES.get(sid) or name,
                            )
                        m.references.append(models.ValueReference(
                            source=source, description=match.group('pages')))
                if not looped:
                    def _get(d, marker):
                        _l = set(nfilter(d.get(marker, [])))
                        if _l:
                            return list(_l)
                    # loop was not run!
                    if not d['forms']:
                        print(d)
                        continue
                        #raise ValueError()
                    me = _get(d, 'me')
                    if me:
                        if len(me) > 1:
                            print d
                        me = me[0]
                    cm = _get(d, 'cm')
                    if cm:
                        assert len(cm) == 1
                        cm = cm[0]
                    m = models.Counterpart(
                        id='%s-%s-%s' % (vsid, j + 1, 1),
                        name=d['forms'],
                        altform='; '.join(_get(d, 'or') or []) or None,
                        description=me or '[%s]' % vs.parameter.name,
                        comment=cm,
                        valueset=vs)
                    so = _get(d, 'so')
                    if so:
                        if len(so) > 1:
                            print d
                        so = so[0]
                        for sid in nfilter([s.strip() for s in SEP_PATTERN.split(so or '')]):
                            match = SID_PATTERN.match(sid)
                            if not match:
                                #print sid
                                continue

                            name = sid
                            sid = normalize_sid(match.group('key'))
                            source = data['Source'].get(sid)
                            if not source:
                                source = data.add(
                                    common.Source, sid,
                                    id=sid,
                                    name=SOURCES.get(sid) or name,
                                )
                            m.references.append(models.ValueReference(
                                source=source, description=match.group('pages')))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    #freeze_func(args)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache, bootstrap=True)
    sys.exit(0)
