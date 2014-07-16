from __future__ import unicode_literals
import sys
from collections import defaultdict

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.sfm import Dictionary, Entry
from clld.util import nfilter

import csd
from csd import models


LANGUAGES = {
    'psc': ('Proto-Siouan-Catawba', None, None),
    'psi': ('Proto-Siouan', 'sio', 'siou1252'),
    'cr': ('Crow', 'cro', 'crow1244'),
    'hi': ('Hidatasa', 'hid', 'hida1246'),
    'ma': ('Mandan', 'mhq', 'mand1446'),
    'la': ('Lakota', 'lkt', 'lako1247'),
    'da': ('Dakota', 'dak', 'dako1258'),
    'as': ('Assiniboine', 'asb', 'assi1247'),
    'ya': ('Yanktonai', 'dak', 'dako1258'),
    'sa': ('Santee-Sisseton', 'dak', 'dako1258'),
    'st': ('Stoney', 'sto', 'ston1242'),
    'ch': ('Chiwere', 'iow', 'iowa1245'),
    'io': ('Ioway', 'iow', 'iowa1245'),
    'ot': ('Otoe', 'iow', 'iowa1245'),
    'wi': ('Hoocak', 'win', 'hoch1243'),
    'om': ('Omaha', 'oma', 'omah1247'),
    'op': ('Omaha-Ponca', 'oma', 'omah1247'),
    'pn': ('Ponca', 'oma', 'omah12477'),
    'po': ('Ponca', 'oma', 'omah1247'),
    'ks': ('Kanza/Kaw', 'ksk', 'kans1243'),
    'os': ('Osage', 'osa', 'osag1243'),
    'qu': ('Quapaw', 'qua', 'quap1242'),
    'bi': ('Biloxi', 'bll', 'bilo1248'),
    'of': ('Ofo', 'of', 'ofoo1242'),
    'tu': ('Tutelo', 'tu', 'tute1247'),
    'pca': ('Proto-Catawba', None, None),
    'ca': ('Catawba', 'chc', 'cata1286'),
}


class CsdEntry(Entry):
    def get_words(self):
        res = defaultdict(list)
        forms = None
        for k, v in self:
            if k in LANGUAGES:
                if forms:
                    # missing \*me field, e.g. for proto forms.
                    res[forms[0]].extend(zip(forms[1], [''] * len(forms[1])))
                forms = (k, nfilter([s.strip() for s in v.split(',')]))
            if k.endswith('me') and k[:-2] in LANGUAGES:
                if forms:
                    res[forms[0]].extend(zip(forms[1], [v] * len(forms[1])))
                forms = None
        return res


def main(args):
    data = Data()

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

    #
    # TODO: add editors!
    #

    d = Dictionary(
        args.data_file('CSD_RLR_Master_version_17.txt'),
        entry_impl=CsdEntry,
        entry_sep='\\lx ')
    print(len(d.entries))
    d.entries = list(filter(lambda r: r.get('lx'), d.entries))
    print(len(d.entries))

    for k, v in LANGUAGES.items():
        data.add(common.Language, k, id=k, name=v)

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
        meaning = data.add(common.Parameter, lemma, id=str(i + 1), name=pname)

        for lid, forms in entry.get_words().items():
            vsid = '%s-%s' % (lid, meaning.id)
            vs = data.add(
                common.ValueSet, vsid,
                id=vsid,
                parameter=meaning,
                contribution=contrib,
                language=data['Language'][lid])

            for j, form in enumerate(forms):
                common.Value(
                    id='%s-%s' % (vsid, j + 1), name=form[0], description=form[1], valueset=vs)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
