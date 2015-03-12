import re

from sqlalchemy.orm import joinedload

from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, DetailsRowLinkCol
from clld.web.datatables.value import Values
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.util.helpers import linked_references, map_marker_img
from clld.web.util.htmllib import HTML
from clld.db.util import get_distinct_values, icontains, collkey
from clld.db.models.common import ValueSet, Value, Language, Parameter
from clld.util import nfilter

from csd.models import Counterpart, Languoid, Entry
from csd.util import markup_form, markup_italic


class RefsCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return linked_references(self.dt.req, item)


class LanguageCol(LinkCol):
    def order(self):
        return Languoid.ord

    def format(self, item):
        return HTML.span(
            map_marker_img(self.dt.req, self.get_obj(item)),
            LinkCol.format(self, item))


class Languoids(Languages):
    def col_defs(self):
        return [
            LanguageCol(self, 'name', get_object=lambda c: c),
            LinkToMapCol(self, 'm'),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
        ]


class CognateCol(LinkCol):
    def __init__(self, dt, name, **kw):
        kw['sTitle'] = 'Reconstruction' if dt.language and dt.language.proto \
            else 'Cognate'
        LinkCol.__init__(self, dt, name, **kw)

    def get_attrs(self, item):
        return dict(label=markup_form(item.name))

    def search(self, qs):
        return icontains(Value.name, qs)

    def order(self):
        return collkey(Value.name)


class PhoneticCol(Col):
    def __init__(self, dt, name, **kw):
        kw['sTitle'] = 'Alternative reconstruction' if dt.language and dt.language.proto \
            else 'Phonetic Siouan'
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        return markup_form(item.phonetic)

    def search(self, qs):
        return icontains(Counterpart.phonetic, qs)

    def order(self):
        return collkey(Counterpart.phonetic)


class Counterparts(Values):
    def get_options(self):
        opts = super(Values, self).get_options()
        if not self.language:
            opts['aaSorting'] = [[0, 'asc'], [1, 'asc']]
        return opts

    def base_query(self, query):
        query = Values.base_query(self, query)
        if not self.language and not self.parameter:
            query = query\
                .join(ValueSet.language)\
                .join(ValueSet.parameter)\
                .options(
                    joinedload(Value.valueset, ValueSet.language),
                    joinedload(Value.valueset, ValueSet.parameter))
        return query

    def col_defs(self):
        get_param = lambda v: v.valueset.parameter
        get_lang = lambda v: v.valueset.language
        core = nfilter([
            CognateCol(self, 'name'),
            PhoneticCol(self, 'phonetic')
            if not (self.language and self.language.proto) else None,
            Col(self, 'description', sTitle='Meaning'),
            Col(self, 'comment',
                model_col=Counterpart.comment,
                format=lambda i: markup_italic(i.comment)),
        ])
        if self.language:
            return [
                LinkCol(self, 'lemma', get_object=get_param, model_col=Parameter.name)] +\
                core + [RefsCol(self, 'sources')]
        if self.parameter:
            return [
                LanguageCol(
                    self, 'language', model_col=Language.name, get_object=get_lang)] +\
                core + [RefsCol(self, 'sources')]
        return [
            LinkCol(self, 'lemma', get_object=get_param, model_col=Parameter.name),
            LanguageCol(self, 'language', model_col=Language.name, get_object=get_lang)] +\
            core


class SemanticDomainCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = [(sd, sd.replace('_', ' ')) for sd in get_distinct_values(Entry.sd)]
        kw['model_col'] = Entry.sd
        Col.__init__(self, dt, name, **kw)

    def search(self, qs):
        return Entry.sd.startswith(qs)

    def format(self, item):
        return (item.sd or '').replace('_', ' ')


class Entries(Parameters):
    def get_options(self):
        opts = super(Parameters, self).get_options()
        opts['aaSorting'] = [[1, 'asc'], [3, 'asc']]
        return opts

    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'more'),
            LinkCol(self, 'name', sTitle='Lemma'),
            SemanticDomainCol(self, 'semantic_domain'),
            Col(self, 'part_of_speech',
                choices=get_distinct_values(Entry.ps), model_col=Entry.ps),
        ]


def includeme(config):
    config.register_datatable('values', Counterparts)
    config.register_datatable('parameters', Entries)
    config.register_datatable('languages', Languoids)
