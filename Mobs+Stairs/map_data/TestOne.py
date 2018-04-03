from entity_structure.boar import Boar
from entity_structure.item import Item

stairs = [
    '25/17/TestThree',
    '40/13/TestTwo',
    '37/23/spawn'
]
rooms = [
    [17, 11, 5, 6],
    [32, 12, 3, 4]
]
spawn_table = [
    [[Boar(color=(255, 114, 114), char='b', name='boar', health=10, blocks=True), 100],
     [Boar(color=(255, 114, 114), char='b', name='boar', health=10, blocks=True), 50],
     [Item(color=(200, 50, 150), char='I', name='item'), 100]],
    [[Boar(color=(255, 114, 114), char='b', name='boar', health=10, blocks=True), 100]]
]