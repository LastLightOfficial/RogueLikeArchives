from random import randint
from importlib import import_module


class InitialSpawns:
    def __init__(self, rooms=None, spawn_table=None, owner=None):
        self.rooms = rooms
        self.spawn_table = spawn_table
        self.owner = owner

    def load_spawn_data(self):
        parent_map = self.owner
        file_to_import = 'map_data.' + parent_map.map_id
        imported_file = import_module(file_to_import)
        self.rooms = getattr(imported_file, 'rooms')
        self.spawn_table = getattr(imported_file, 'spawn_table')

    def populate(self):

        parent_map = self.owner
        room_iterator = 0
        for room_list in self.rooms:
            x = room_list[0]
            y = room_list[1]
            w = room_list[2]
            h = room_list[3]
            spawn_table_iterator = 0
            for mob_chance in self.spawn_table[room_iterator]:
                monster, chance = self.spawn_table[room_iterator][spawn_table_iterator]
                if randint(1, 100) <= int(chance):
                    monster.x = randint(x, x + w)
                    monster.y = randint(y, y + h)
                    parent_map.entities.append(monster)
                    # print(str(len(parent_map.entities)))
                    # print("iterator: " + str(spawn_table_iterator))
                spawn_table_iterator += 1
            room_iterator += 1



class Nests:
    def __init__(self, x=None, y=None, r=None, mob_table=None, spawn_table=None):
        self.x = x
        self.y = y
        self.r = r
        self.mob_table = mob_table
        self.spawn_table = spawn_table

    def load_nest_data(self, game_map):
        file_to_import = 'map_data.' + game_map.map_id
        imported_file = import_module(file_to_import)
        nest_dict = getattr(imported_file, 'nests')
        self.x = nest_dict['x']
        self.y = nest_dict['y']
        self.r = nest_dict['r']
        self.mob_table = nest_dict['mob_table']
        self.spawn_table = nest_dict['spawn_table']