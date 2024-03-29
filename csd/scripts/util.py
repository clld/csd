from clldutils.misc import slug
from csvw.dsv import reader


_LANGUAGES = [
    ('psc', 'Proto-Siouan-Catawba', None, 'siou1252', 'D2B48C', None),
        ('psi', 'Proto-Siouan', 'sio', 'core1249', 'FFE4C4', 'psc'),
            ('pch', 'Proto-Crow-Hidatsa', None, 'miss1252', '87CEEB', 'psi'),
                ('cr', 'Crow', 'cro', 'crow1244', 'ADD8E6', 'pch'),
                ('hi', 'Hidatsa', 'hid', 'hida1246', 'ADD8E6', 'pch'),
            ('pma', 'Pre-Mandan', None, None, '2E8B57', 'psi'),
                ('ma', 'Mandan', 'mhq', 'mand1446', '3CB371', 'pma'),
            ('pmv', 'Proto-Mississipi-Valley', None, 'miss1254', 'BA55D3', 'psi'),
                ('pda', 'Proto-Dakota', None, 'dako1257', 'DA70D6', 'pmv'),
                    ('la', 'Lakota', 'lkt', 'lako1247', 'EE82EE', 'pda'),
                    ('da', 'Dakota', 'dak', 'dako1258', 'EE82EE', 'pda'),
                    ('as', 'Assiniboine', 'asb', 'assi1247', 'EE82EE', 'pda'),
                    ('ya', 'Yanktonai', 'dak', 'dako1258', 'EE82EE', 'pda'),
                    ('st', 'Stoney', 'sto', 'ston1242', 'EE82EE', 'pda'),
                    ('sv', 'Sioux Valley', None, None, 'EE82EE', 'pda'),
                ('pwc', 'Proto-Hoocąk-Chiwere', None, 'winn1245', 'FF4500', 'pmv'),
                    ('ch', 'Chiwere', 'iow', 'iowa1245', 'FF7F50', 'pwc'),
                    #('io', 'Ioway', 'iow', 'iowa1245', 'FF7F50', 'pwc'),
                    ('mo', 'Missouria', None, 'miss1249', 'FF7F50', 'pwc'),
                    ('ot', 'Otoe', 'iow', 'iowa1245', 'FF7F50', 'pwc'),
                    ('wi', 'Hoocąk', 'win', 'hoch1243', 'FF7F50', 'pwc'),
                ('pdh', 'Proto-Dhegiha', None, 'dheg1241', 'FFA500', 'pmv'),
                    ('om', 'Omaha', 'oma', 'omah1247', 'FFD700', 'pdh'),
                    ('op', 'Omaha-Ponca', 'oma', 'omah1247', 'FFD700', 'pdh'),
                    ('pn', 'Ponca', 'oma', 'omah1247', 'FFD700', 'pdh'),
                    ('ks', 'Kanza/Kaw', 'ksk', 'kans1243', 'FFD700', 'pdh'),
                    ('os', 'Osage', 'osa', 'osag1243', 'FFD700', 'pdh'),
                    ('qu', 'Quapaw', 'qua', 'quap1242', 'FFD700', 'pdh'),
            ('pse', 'Proto-Southeastern', None, 'bilo1247', '008080', 'psi'),
                ('pbo', 'Proto-Biloxi-Ofo', None, 'bilo1247', '008B8B', 'pse'),
                    ('bi', 'Biloxi', 'bll', 'bilo1248', '00FFFF', 'pbo'),
                    ('of', 'Ofo', 'ofo', 'ofoo1242', '00FFFF', 'pbo'),
                ('pts', 'Proto-Tutelo-Saponi', None, 'bilo1247', '008B8B', 'pse'),
                    ('tu', 'Tutelo', 'tta', 'tute1247', '00FFFF', 'pts'),
                    ('sp', 'Saponi', 'tta', 'tute1247', '00FFFF', 'pts'),
        ('pca', 'Proto-Catawba', None, 'cata1285', '778899', 'psc'),
            ('ca', 'Catawba', 'chc', 'cata1286', 'B0C4DE', 'pca'),
            ('wo', 'Woccon', 'xwc', 'wocc1242', 'B0C4DE', 'pca'),
    ]

SOURCES = {
    'N': 'Nikonha (Tutelo informant)',
    'AG': 'Albert S. Gatschet',
    'ASG': 'Albert S. Gatschet',
    'AWJ': 'A. Wesley Jones',
    'B': 'Eugene Buechel dictionary',
    'C': 'RICHARD T. CARTER',
    'DEC': 'DICTIONARY OF EVERYDAY CROW (GORDON/GRACZYK)',
    'DS': 'DORSEY/SWANTON OFO DICTIONARY',
    'EB': 'Eugene Buechel',
    'EJ': 'Eli James (Lakota speaker)',
    'Fontaine': 'Fontaine (Saponi word list)',
    'FS': 'Frank T. Siebert',
    'GG': 'GORDON AND GRACZYK',
    'GK': 'GEOFFREY KIMBALL',
    'G': 'GORDON? GILLMORE? GRACZYK?',
    'GMsf': 'GORDON MARSH SOMETHING',
    'H': 'ROBERT HOLLOW',
    'H&Vf': 'HOLLOW AND ?? (ONLY ONE INSTANCE)',
    'H(N)': 'Hale, Nikonha',
    'H.': 'Horatio Hale',
    'HWM': 'WASHINGTON MATTHEWS 1877 HIDATSA GRAMMAR',
    'HH': 'HORATIO HALE',
    'J': 'A. WESLEY JONES',
    'JEK': 'John E. Koontz',
    'JGT': 'Jimm Good Tracks',
    'JOD': 'James Owen Dorsey',
    'JWE': 'YES - WHITE EAGLE',
    'KM': 'Kenneth Miner',
    'KS': 'Kathy Shea or the Kansa language',
    'LB': 'Lew Ballard',
    'LF': 'Laflesche',
    'Lawson': 'JOHN LAWSON WOCCON VOCABULARY',
    'Lipkind': 'WILLIAM LIPKIND WINNEBAGO GRAMMAR',
    'Lk': 'Lipkind',
    'LWR': 'Lila Wistrand Robinson',
    'Marsh': 'Gordon Marsh',
    'M': 'GH MATTHEWS',
    'mr': "SEEMS TO BE ONE OF BOB'S KANSA SPEAKERS - CK HIS DICTIONARY INTRO",
    'MS': 'MAURICE SWADESH OR "MANUSCRIPT?"',
    'PAS': 'Pat Shaw',
    'R': 'STEPHEN R. RIGGS DICTIONARY',
    'RG': 'Randolph Graczyk',
    'RLR': 'Robert L. Rankin',
    'RR': 'Robert L. Rankin',
    'RTC': 'Richard T. Carter',
    'RTG': 'Randolph Graczyk',
    'Sp.': 'Frank Speck',
    'Speck': 'Frank Speck',
    'Taylor': 'Allan R. Taylor',
    'Ssf': 'SOMETHING WITH OFO DATA',
    'SW': '?MARK SWETLAND DICTIONARY?',
    'Wm': 'WILLIAMSON ENGLISH-DAKOT DICTIONARY',
    'W': "CAN''T FIND IT -- WOLFF? WHITMAN?  NEED TO KNOW LANGUAGE",
    'Miller + Davis': 'Wick Miller and ? Davis',
    'IJAL': 'International Journal of American Linguistics',
    'Voorhis': 'Paul Voorhis',
    'Other Abbreviations': '',
    'Hw.': 'J.N.B. Hewitt',
    'OVS': 'Ohio Valley Siouan',
    'MRS': 'MISSOURI RIVER SIOUAB',
    'PEA': 'Proto-Eastern Algonquian',
    'PUA': 'Proto-Uto Aztecan',
    'PA': 'PROTO-ALGONQUIAN',
    'MRH': 'Mary R. Haas',
}


def normalize_sid(sid):
    return slug(sid.replace('+', 'and').replace('&', 'and'))


def get_sources(args):
    res = {}

    for d in reader(args.data_file('sources_CSD.csv'), delimiter=',', dicts=True):
        res[normalize_sid(d['Abbreviation'])] = d

    for sid in list(SOURCES.keys()):
        _sid = normalize_sid(sid)
        if _sid not in res:
            print('missing sid: %s' % sid)
            res[_sid] = dict(citation=SOURCES[sid], Name=sid, title=SOURCES[sid])

    return res


SD = {
    'anml': 'animal',
    'bdypart': 'body part',
    'bdyprt': 'body part',
    'clr': 'color',
    'cltr': 'cultural item',
    'cltrtrm': 'cultural term',
    'kin': 'kinship',
    'kintrm': 'kinship',
    'kintr': 'kinship',
    'kinrm': 'kinship',
    'geol': 'geological',
    'humn': 'human',
    'mtrlg': 'meteorological',
    'plant': 'plant',
}

PS = {
    '12Act': 'inclusive active',
    '12Caus': 'inclusive causative',
    '12Poss': 'inclusive possessive',
    '12Stat': 'inclusive stative',
    '1Act': 'first person active',
    '1Caus': 'first person causative',
    '1Poss': 'first person possessive',
    '1Stat': 'first person stative',
    '2Act': 'second person active',
    '2Caus': 'second person causative',
    '2Poss': 'second person possessive',
    '2Stat': 'second person stative',
    '3Act': 'third person active',
    '3Caus': 'third person causative',
    '3Pl': 'third person plural',
    '3Poss': 'third person possessive',
    '3Stat': 'third person stative',
    'Abil': 'ability',
    'Adj': 'adjective',
    'Adv': 'adverb',
    'Advr': 'adverbializer',
    'Ag': 'agentive',
    'Al': 'alienable',
    'All': 'allative',
    'Aprx': 'aproximative',
    'Ben': 'benefactive',
    'Caus': 'causative',
    'Cmplr': 'complementizer',
    'Cmpr': 'comparative',
    'Coll': 'collective',
    'Conj': 'conjunction',
    'Deic': 'deictic',
    'Dem': 'demonstrative',
    'Des': 'desiderative',
    'Detr': 'detransitive',
    'Dimn': 'diminutive',
    'Dstr': 'distributive',
    'Dur': 'durative',
    'Fmtv': 'formative',
    'Form': 'form',
    'Hab': 'habitual',
    'Imp': 'imperative',
    'Inch': 'inchoative',
    'Incl': 'inclusive',
    'Indef': 'indefinite',
    'Inst': 'instrumental',
    'Interj': 'interjection',
    'Interr': 'interrogative',
    'Intns': 'intensive',
    'Intr': 'intransitive',
    'Iter': 'iterative',
    'Loc': 'locative',
    'Mode': 'modal',
    'Mom': 'momentary',
    'Mot': 'motion',
    'Neg': 'negative',
    'N': 'noun',
    'NFnl': 'noun final',
    'Nomr': 'nominalizer',
    'NSuf': 'noun suffix',
    'Num': 'numeral',
    'Part': 'partitive',
    'PassRefl': 'passive-reflexive',
    'Pl': 'plural',
    'Pos': 'positional',
    'Prf': 'perfect',
    'Prob': 'probable',
    'Pron': 'pronoun',
    'Prox': 'proximal',
    'Ptcl': 'particle',
    'Qual': 'qualitative',
    'Quan': 'quantitative',
    'Quot': 'quotative',
    'Rcp': 'reciprocal',
    'Rdup': 'reduplication',
    'Refl': 'reflexive',
    'ReflPoss': 'reflexive possessive',
    'Rel': 'relative',
    'Sbj': 'subject',
    'Sg': 'singular',
    'Sim': 'similative',
    'Stem': 'stem',
    'Tact': 'tactile',
    'Tr': 'transitive',
    'V': 'verb',
    'Vert': 'vertitive',
    'VFnl': 'verb final',
    'VPrfx': 'verb prefix',
    'VRt': 'verb root',
    'VSuf': 'verb suffix',
}
for k in list(PS.keys()):
    PS[k.lower()] = PS[k]
