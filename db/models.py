from db.base import Base
from db.json_encode import JSONEncodedType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from typing import List

"""RP section"""
class Objective(Base):
    __tablename__ = 'objective'

    objective_id = Column(Integer, Sequence('objective_id_seq'), primary_key=True)
    name = Column(String)
    description = Column(String)
    is_solved = Column(Boolean, default=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Objective(name={self.name}, description={self.description})>"

class Location(Base):
    __tablename__ = 'location'

    location_id = Column(Integer, Sequence('location_id_seq'), primary_key=True)
    place = Column(String)

    def __init__(self, place):
        self.place = place

    def __repr__(self):
        return f"<Location(place={self.place})>"

class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String)
    description = Column(String)
    count = Column(Integer)
    attributes = Column(MutableList.as_mutable(JSONEncodedType))
    adventurer_uid = Column(String, ForeignKey('adventurer.uid'))

    def __init__(self, name, description, count=1, attributes=[]):
        self.name = name
        self.description = description
        self.count = count
        self.attributes = attributes

    def __repr__(self):
        return f"<Item(name={self.name}, description={self.description}, count={self.count}, attributes={self.attributes})>"

class Adventurer(Base):
    __tablename__ = 'adventurer'

    uid = Column(String, primary_key=True)
    name = Column(String)
    inventory = relationship('Item', lazy='joined')

    def __init__(self, uid, name, inventory:List[Item]=[]):
        self.uid = uid
        self.name = name
        self.inventory = inventory

    def __repr__(self):
        return f"<Adventurer(uid={self.uid}, name={self.name}, inventory={self.inventory})>"



"""Suggestion section"""
class PChoice(Base):
    __tablename__ = 'pchoice'

    choice_id = Column(Integer, Sequence('pchoice_id_seq'), primary_key=True)
    choice = Column(String)
    approved = Column(Boolean)
    expression_id = Column(Integer, ForeignKey('pexpression.expression_id'))

    def __init__(self, choice, approved=False):
        self.choice = choice
        self.approved = approved

    def __repr__(self):
        return f"<PChoice(choice={self.choice})>"

class PExpression(Base):
    __tablename__ = 'pexpression'

    expression_id = Column(Integer, Sequence('pexpression_id_seq'), primary_key=True)
    choices = relationship('PChoice', lazy='joined')
    prompt_id = Column(Integer, ForeignKey('prompt.prompt_id'))

    def __init__(self, choices:List[PChoice]=[]):
        self.choices = choices

    def __repr__(self):
        return f"<PExpression(choices={self.choices})>"

class Prompt(Base):
    __tablename__ = 'prompt'

    prompt_id = Column(Integer, Sequence('prompt_id_seq'), primary_key=True)
    prompt = Column(String)
    expressions = relationship('PExpression', lazy='joined')
    approved = Column(Boolean)

    def __init__(self, max_index, prompt, expressions:List[PExpression]=[], approved=False):
        self.max_index = max_index
        self.prompt = prompt
        self.expressions = expressions
        self.approved = approved

    def __repr__(self):
        return f"<Prompt(id={self.prompt_id}, prompt={self.prompt}, expressions={self.expressions})>"