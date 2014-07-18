from sqlalchemy.orm import joinedload

from clld.web.datatables.base import Col, LinkCol
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.util.helpers import linked_references
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import ValueSet, Value, Language, Parameter

from csd.models import Counterpart, Languoid, Entry


class RefsCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return linked_references(self.dt.req, item)


class LanguageCol(LinkCol):
    def get_obj(self, item):
        return item.valueset.language

    def order(self):
        return Languoid.ord


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
        if self.language:
            return [
                LinkCol(
                    self, 'lemma',
                    get_object=lambda v: v.valueset.parameter,
                    model_col=Parameter.name),
                Col(self, 'cognate', model_col=Counterpart.cognate),
                Col(self, 'name'),
                Col(self, 'description', sTitle='Meaning'),
                Col(self, 'comment', model_col=Counterpart.comment),
                RefsCol(self, 'sources'),
            ]
        if self.parameter:
            return [
                LanguageCol(self, 'language', model_col=Language.name),
                Col(self, 'cognate', model_col=Counterpart.cognate),
                Col(self, 'name'),
                Col(self, 'description', sTitle='Meaning'),
                Col(self, 'comment', model_col=Counterpart.comment),
                RefsCol(self, 'sources'),
            ]
        return [
            LinkCol(
                self, 'lemma',
                get_object=lambda v: v.valueset.parameter,
                model_col=Parameter.name),
            LanguageCol(self, 'language', model_col=Language.name),
            Col(self, 'name'),
            Col(self, 'description', sTitle='Meaning'),
            Col(self, 'comment', model_col=Counterpart.comment),
        ]


class Entries(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Lemma'),
            Col(self, 'semantic_domain',
                choices=get_distinct_values(Entry.sd), model_col=Entry.sd),
            Col(self, 'part_of_speech',
                choices=get_distinct_values(Entry.ps), model_col=Entry.ps),
        ]


def includeme(config):
    config.register_datatable('values', Counterparts)
    config.register_datatable('parameters', Entries)
