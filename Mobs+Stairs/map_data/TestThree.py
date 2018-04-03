from entity_structure.boar import Boar

stairs = [
    '22/19/TestOne',
    '40/24/TestTwo'
    ]
rooms = [
    [17, 11, 5, 6],
    [32, 12, 3, 4]
]
spawn_table = [
    [[Boar(color=(255, 114, 114), char='b', name='boar', health=10, blocks=True), 100],
     [Boar(color=(255, 114, 114), char='b', name='boar', health=10, blocks=True), 50]],
    [[Boar(color=(255, 114, 114), char='b', name='boar', health=10, blocks=True), 100]]
]