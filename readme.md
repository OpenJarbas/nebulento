# Nebulento

*A lightweight, dead simple fuzzy matching intent parser*

Built on top of [rapidfuzz](https://github.com/maxbachmann/rapidfuzz)

## Example

```python
from nebulento import IntentContainer, MatchStrategy

container = IntentContainer(fuzzy_strategy=MatchStrategy.TOKEN_SET_RATIO)

container.add_intent('hello', [
    'hello', 'hi', 'how are you', "what's up"
])
container.add_intent('buy', [
    'buy {item}', 'purchase {item}', 'get {item}', 'get {item} for me'
])
container.add_entity('item', [
    'milk', 'cheese'
])

container.calc_intent('hello')
# {'best_match': 'hello',
#  'conf': 1.0,
#  'entities': {},
#  'match_strategy': 'TOKEN_SET_RATIO',
#  'name': 'hello',
#  'utterance': 'hello',
#  'utterance_consumed': 'hello',
#  'utterance_remainder': ''}
                         
container.calc_intent('buy milk')
# {'best_match': 'buy {item}',
#  'conf': 0.71875,
#  'entities': {'item': ['milk']},
#  'match_strategy': 'TOKEN_SET_RATIO',
#  'name': 'buy',
#  'utterance': 'buy milk',
#  'utterance_consumed': 'buy milk',
#  'utterance_remainder': ''}


container.add_intent('look_at_thing', ['I see {thing} (in|on) {place}'])
container.add_entity("place", ["floor", "table"])

container.calc_intent('I see trash in the floor')
#{'best_match': 'i see {thing} in {place}',
# 'conf': 0.65625,
# 'entities': {'place': ['floor']},
# 'match_strategy': 'TOKEN_SET_RATIO',
# 'name': 'look_at_thing',
# 'utterance': 'i see trash in the floor',
# 'utterance_consumed': 'i see in floor',
# 'utterance_remainder': 'trash the'}
            
container.add_entity("thing", ["food"])
container.calc_intent('I see food in the table')
#{'best_match': 'i see {thing} in {place}',
# 'conf': 0.7007978723404256,
# 'entities': {'place': ['table'], 'thing': ['food']},
# 'match_strategy': 'TOKEN_SET_RATIO',
# 'name': 'look_at_thing',
# 'utterance': 'i see food in the table',
# 'utterance_consumed': 'i see in table food',
# 'utterance_remainder': 'the'}

```