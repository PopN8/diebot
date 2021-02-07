from base import Base, session_scope, engine
from models import Adventurer, Item, Objective, Location

def update_schemes():
    Base.metadata.create_all(engine)

def clear_db():
    Base.metadata.drop_all(engine)


def add_adventurer(uid, name):
    with session_scope() as Session:
        Session.add(Adventurer(uid, name))

def get_adventurer(uid):
    with session_scope() as Session:
        adventurer = Session.query(Adventurer).get(uid)
    return adventurer


def give_item(adventurer_uid, item_name, description, count, attributes=[]):
    item = Item(item_name, description, count, attributes)
    with session_scope() as Session:
        adventurer = Session.query(Adventurer).get(adventurer_uid)
        inventory = adventurer.inventory
        match = list(filter(lambda i: i.name == item.name, inventory))
        if match:
            match[0].count += item.count
        else:
            adventurer.inventory.append(item)

def get_inventory(adventurer_uid):
    with session_scope() as Session:
        adventurer = Session.query(Adventurer).get(adventurer_uid)
        inventory = adventurer.inventory
    return inventory

def remove_item(adventurer_uid, item_name, count):
    with session_scope() as Session:
        adventurer = Session.query(Adventurer).get(adventurer_uid)
        inventory = adventurer.inventory
        match = list(filter(lambda i: i.name == item_name, inventory))
        if match:
            match[0].count -= count
            if match[0].count <= 0:
                inventory.remove(match[0])


def add_objective(name, description):
    with session_scope() as Session:
        Session.add(Objective(name, description))

def get_current_objectives():
    with session_scope() as Session:
        objective = Session.query(Objective).filter_by(is_solved=False).all()
    return objective

def solve_objective(objective_id):
    with session_scope() as Session:
        objective = Session.query(Objective).get(objective_id)
        objective.is_solved = True


def add_location(place):
    with session_scope() as Session:
        Session.add(Location(place))

def get_current_location():
    with session_scope() as Session:
        location = Session.query(Location).order_by(Location.id.desc()).first()
    return location