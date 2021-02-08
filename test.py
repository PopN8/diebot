import json
from random import choice

expressions = {
    'You {} the dice.': [
        ['disrespect', 'poop', 'forehead kiss', 'kiss', 'lick']
    ]
    'You {} the dice {}.': [
        ['yeet', 'gently roll'],
        ['across the room', 'into an active volcano']
    ],
    'You {}, {}, then {} the dice.': [
        ['wind up', 'close your eyes'],
        ['line up your shot', 'pray to the gods'],
        ['tenderly launch', 'whistfully imagine']
    ]
}

with open('expressions.json', 'w') as f:
    json.dump(expressions, f, indent=4)

with open('expressions.json', 'r') as f:
    exp = json.load(f)

for _ in range(10):
    prompt = choice(list(exp.keys()))
    arguments = [choice(a) for a in exp[prompt]]
    print(prompt.format(*arguments))