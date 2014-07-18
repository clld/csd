# coding: utf8
from __future__ import unicode_literals
import sys
from collections import defaultdict
import re
from itertools import izip_longest

from clld.scripts.util import initializedb, Data, add_language_codes, glottocodes_by_isocode
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.sfm import Dictionary, Entry
from clld.util import nfilter, slug

import csd
from csd import models


SOURCES = {
    'N': 'Nikonha (Tutelo informant)',
    'AG': 'Albert S. Gatschet',
    'ASG': 'Albert S. Gatschet',
    'AWJ': 'A. Wesley Jones',
    'B': '',
    'C': '',
    'DEC': '',
    'DS': '',
    'EB': 'Eugene Buechel',
    'EJ': 'Eli Jones (Lakota speaker)',
    'F + LF': 'Fletcher and Laflesche',
    'FLF': 'Fletcher and Laflesche',
    'Fontaine': 'Fontaine (Saponi word list)',
    'FS': 'Frank T. Siebert',
    'GG': '',
    'GK': '',
    'G': '',
    'GMsf': '',
    'H': '',
    'H&Vf': '',
    'H(N)': 'Hale, Nikonha',
    'H.': 'Horatio Hale',
    'HWM': '',
    'HH': '',
    'J': '',
    'JEK': 'John E. Koontz',
    'JGT': 'Jimm Good Tracks',
    'JOD': 'James Owen Dorsey',
    'JWE': '',
    'KM': 'Kenneth Miner',
    'KS': 'Kathy Shea or the Kansa language',
    'LB': 'Lew Ballard',
    'LF': 'Laflesche',
    'Lawson': '',
    'Lipkind': '',
    'Lk': 'Lipkind',
    'LWR': 'Lila Wistrand Robinson',
    'Marsh': 'Gordon Marsh',
    'M': '',
    'mr': '',
    'MS': '',
    'PAS': 'Pat Shaw',
    'per': '',
    'R': '',
    'RG': 'Randolph Graczyk',
    'RLR': 'Robert L. Rankin',
    'RR': 'Robert L. Rankin',
    'RTC': 'Richard T. Carter',
    'RTG': 'Randolph Graczyk',
    'Sp.': 'Frank Speck',
    'Speck': 'Frank Speck',
    'Taylor': 'Allan R. Taylor',
    'Ssf': '',
    'SW': '',
    'Wm': '',
    'W': '',
    'Miller + Davis': 'Wick Miller and ? Davis',
    'IJAL': 'International Journal of American Linguistics',
    'Voorhis': 'Paul Voorhis',
    'Other Abbreviations': '',
    'Hw.': 'J.N.B. Hewitt',
    'OVS': 'Ohio Valley Siouan',
    'MRS': '',
    'PEA': 'Proto-Eastern Algonquian',
    'PUA': 'Proto-Uto Aztecan',
    'PA': '',
    'MRH': 'Mary R. Haas',
}


def normalize_sid(sid):
    return slug(sid.replace('+', 'and').replace('&', 'and'))

for sid in list(SOURCES.keys()):
    SOURCES[normalize_sid(sid)] = SOURCES[sid]


_LANGUAGES = [
    ('psc', 'Proto-Siouan-Catawba', None, None),
    ('psi', 'Proto-Siouan', 'sio', 'siou1252'),
    ('pch', 'Proto-Crow-Hidatsa', None, None),
    ('cr', 'Crow', 'cro', 'crow1244'),
    ('hi', 'Hidatasa', 'hid', 'hida1246'),
    ('pma', 'Proto-Mandan', None, None),
    ('ma', 'Mandan', 'mhq', 'mand1446'),
    ('pmv', 'Proto-Mississipi-Valley', None, None),
    ('pda', 'Proto-Dakota', None, None),
    ('la', 'Lakota', 'lkt', 'lako1247'),
    ('da', 'Dakota', 'dak', 'dako1258'),
    ('as', 'Assiniboine', 'asb', 'assi1247'),
    ('ya', 'Yanktonai', 'dak', 'dako1258'),
    ('sa', 'Santee-Sisseton', 'dak', 'dako1258'),
    ('st', 'Stoney', 'sto', 'ston1242'),
    ('sv', 'Sioux-Valley', None, None),
    ('pwc', 'Proto-Hoocąk-Chiwere', None, None),
    ('ch', 'Chiwere', 'iow', 'iowa1245'),
    ('io', 'Ioway', 'iow', 'iowa1245'),
    ('ot', 'Otoe', 'iow', 'iowa1245'),
    ('wi', 'Hoocak', 'win', 'hoch1243'),
    ('pdh', 'Proto-Dhegiha', None, None),
    ('om', 'Omaha', 'oma', 'omah1247'),
    ('op', 'Omaha-Ponca', 'oma', 'omah1247'),
    ('pn', 'Ponca', 'oma', 'omah12477'),
    ('po', 'Ponca', 'oma', 'omah1247'),
    ('ks', 'Kanza/Kaw', 'ksk', 'kans1243'),
    ('os', 'Osage', 'osa', 'osag1243'),
    ('qu', 'Quapaw', 'qua', 'quap1242'),
    ('bi', 'Biloxi', 'bll', 'bilo1248'),
    ('of', 'Ofo', 'of', 'ofoo1242'),
    ('tu', 'Tutelo', 'tu', 'tute1247'),
    ('pca', 'Proto-Catawba', None, None),
    ('ca', 'Catawba', 'chc', 'cata1286'),
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
                if data and data.get('forms'):
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
        if data and data.get('forms'):
            yield data

    def get_words(self):
        res = defaultdict(list)
        for chunk in self.language_chunks():
            #chunk['so'] = nfilter(
            #    [s.strip() for s in SEP_PATTERN.split(chunk.get('so', ''))])
            if 'language' in chunk:
                res[chunk['language']].append(chunk)
        return res


def main(args):
    data = Data()
    glottocodes, geocoords = {}, defaultdict(lambda: (None, None))
    for k, v in glottocodes_by_isocode(
            'postgresql://robert@/glottolog3',
            cols=['id', 'latitude', 'longitude']).items():
        glottocodes[k] = v[0]
        geocoords[k] = (v[1], v[2])

    dataset = common.Dataset(
        id=csd.__name__,
        name="Comparative Siouan Dictionary",
        publisher_name ="Max Planck Institute for Evolutionary Anthropology",
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
        args.data_file('CSD_RLR_Master_version_17.txt'),
        entry_impl=CsdEntry,
        entry_sep='\\lx ')
    print(len(d.entries))
    d.entries = list(filter(lambda r: r.get('lx'), d.entries))
    print(len(d.entries))

    for i, v in enumerate(_LANGUAGES):
        l = data.add(
            models.Languoid, v[0],
            id=v[0],
            name=v[1],
            ord=i,
            latitude=geocoords[v[2]][0],
            longitude=geocoords[v[2]][1])
        if v[2]:
            add_language_codes(data, l, v[2], glottocodes=glottocodes)

    pnames = defaultdict(int)
    for i, entry in enumerate(d.entries):
        pnames[entry.get('lx')] += 1

    disambiguation_numbers = defaultdict(int)

    for i, entry in enumerate(d.entries):
        lemma = entry.get('lx')
        if not lemma:
            continue
        pname = lemma
        if pnames[lemma] > 1:
            disambiguation_numbers[lemma] += 1
            pname += ' (%s)' % disambiguation_numbers[lemma]
        meaning = data.add(
            models.Entry, lemma,
            id=str(i + 1),
            name=pname,
            description=entry.get('com'),
            sd=entry.get('sd'),
            ps=entry.get('ps'))

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
                k = None
                for k, t in enumerate(izip_longest(
                        *[d.get(_m, []) for _m in '_ih oo me so cm'.split()])):
                    ih, oo, me, so, cm = t
                    oo = oo or ih
                    if not oo:
                        oo = d['forms']

                    m = models.Counterpart(
                        id='%s-%s-%s' % (vsid, j + 1, k + 1),
                        name=oo,
                        cognate=d['forms'],
                        description=me,
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
                if k is None:
                    # loop was not run!
                    m = models.Counterpart(
                        id='%s-%s-%s' % (vsid, j + 1, 1),
                        name=d['forms'],
                        cognate=d['forms'],
                        description=None,
                        comment=None,
                        valueset=vs)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
