from sqlalchemy.orm import joinedload

from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, DetailsRowLinkCol
from clld.web.datatables.value import Values
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.util.helpers import linked_references, map_marker_img
from clld.web.util.htmllib import HTML
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import ValueSet, Value, Language, Parameter

from csd.models import Counterpart, Languoid, Entry


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


class Counterparts(Values):
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
        if self.language:
            return [
                LinkCol(self, 'lemma', get_object=get_param, model_col=Parameter.name),
                Col(self, 'name', sTitle='Cognate'),
                Col(self, 'altform',
                    model_col=Counterpart.altform, sTitle='Alternative form'),
                Col(self, 'description', sTitle='Meaning'),
                Col(self, 'comment', model_col=Counterpart.comment),
                RefsCol(self, 'sources'),
            ]
        if self.parameter:
            return [
                LanguageCol(
                    self, 'language', model_col=Language.name, get_object=get_lang),
                Col(self, 'name', sTitle='Cognate'),
                Col(self, 'altform',
                    model_col=Counterpart.altform, sTitle='Alternative form'),
                Col(self, 'description', sTitle='Meaning'),
                Col(self, 'comment', model_col=Counterpart.comment),
                RefsCol(self, 'sources'),
            ]
        return [
            LinkCol(self, 'lemma', get_object=get_param, model_col=Parameter.name),
            LanguageCol(self, 'language', model_col=Language.name, get_object=get_lang),
            Col(self, 'name', sTitle='Cognate'),
            Col(self, 'altform',
                model_col=Counterpart.altform, sTitle='Alternative form'),
            Col(self, 'description', sTitle='Meaning'),
            Col(self, 'comment', model_col=Counterpart.comment),
        ]


class Entries(Parameters):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'more'),
            LinkCol(self, 'name', sTitle='Lemma'),
            Col(self, 'semantic_domain',
                choices=get_distinct_values(Entry.sd), model_col=Entry.sd),
            Col(self, 'part_of_speech',
                choices=get_distinct_values(Entry.ps), model_col=Entry.ps),
        ]


def includeme(config):
    config.register_datatable('values', Counterparts)
    config.register_datatable('parameters', Entries)
    config.register_datatable('languages', Languoids)
