from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Value, HasSourceMixin, Language, Parameter, Contribution


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class Languoid(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    ord = Column(Integer)
    color = Column(String)
    proto = Column(Boolean, default=False)
    parent_pk = Column(Integer, ForeignKey('languoid.pk'))
    children = relationship(
        'Languoid',
        order_by='Languoid.ord',
        foreign_keys=[parent_pk],
        backref=backref('parent', remote_side=[pk]))
    level = Column(Integer)


@implementer(interfaces.IParameter)
class Entry(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    ps = Column(Unicode)
    sd = Column(Unicode)
    psi_reconstruction_with_root_extension_code = Column(Unicode)
    othlgs = Column(Unicode)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    contribution = relationship(Contribution)


@implementer(interfaces.IValue)
class Counterpart(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    phonetic = Column(Unicode)
    comment = Column(Unicode)
    original_entry = Column(Unicode)
    other_reconstructions = Column(Unicode)


class ValueReference(Base, HasSourceMixin):
    """
    """
    value_pk = Column(Integer, ForeignKey('value.pk'))
    value = relationship(Value, backref="references")
