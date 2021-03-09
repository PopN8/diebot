from db.base import Base, session_scope, engine
from db.db_exceptions import PromptIndexError
from db.models import Adventurer, Item, Objective, Location, Prompt, PExpression, PChoice

def update_schemes():
    Base.metadata.create_all(engine)

def clear_db():
    Base.metadata.drop_all(engine)


"""RP section"""
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

def get_objective_by_id(objective_id):
    with session_scope() as Session:
        objective = Session.query(Objective).get(objective_id)
    return objective

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
        location = Session.query(Location).order_by(Location.location_id.desc()).first()
    return location


"""Suggestion section"""
def add_prompt(max_index, prompt):
    with session_scope() as Session:
        Session.add(Prompt(max_index, prompt))

def get_prompt(prompt_id):
    with session_scope() as Session:
        prompt = Session.query(Prompt).get(prompt_id)
    return prompt

def get_all_prompts():
    with session_scope() as Session:
        prompts = Session.query(Prompt).all()
    return prompts

def get_accepted_prompts():
    with session_scope() as Session:
        prompts = Session.query(Prompt).filter_by(approved=True).all()
    return prompts

def get_pending_prompts():
    with session_scope() as Session:
        prompts = Session.query(Prompt).filter_by(approved=False).all()
    return prompts


def add_choice(prompt_id, index, choice):
    with session_scope() as Session:
        prompt = Session.query(Prompt).get(prompt_id)
        if 0 <= index <= prompt.max_index:
            prompt.expressions[index].choices.append(PChoice(choice))
        else:
            raise PromptIndexError(index, prompt.max_index)