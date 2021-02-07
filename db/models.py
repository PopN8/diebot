from base import Base
from json_encode import JSONEncodedType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from typing import List

class Objective(Base):
    __tablename__ = 'objective'

    id = Column(Integer, Sequence('objective_id_seq'), primary_key=True)
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

    id = Column(Integer, Sequence('location_id_seq'), primary_key=True)
    place = Column(String)

    def __init__(self, place):
        self.place = place

    def __repr__(self):
        return f"<Location(place={self.place})>"

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
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
    #item_id = Column(Integer, ForeignKey('item.id'))
    inventory = relationship('Item', lazy='joined')

    def __init__(self, uid, name, inventory:List[Item]=[]):
        self.uid = uid
        self.name = name
        self.inventory = inventory

    def __repr__(self):
        return f"<Adventurer(uid={self.uid}, name={self.name}, inventory={self.inventory})>"