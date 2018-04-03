import gzip
import os
from importlib import import_module

from tdl.map import Map

import xpLoaderPy3 as xpL
from entity_structure.entity import Entity
from constants import RenderOrder
from mob_spawner import InitialSpawns


# solid square char
poskey_tile_character = 219
# period
poskey_period_character = 46
# pound
poskey_pound_character = 35
# Capital S
poskey_capital_s_character = 83
# numbers
poskey_number_one_character = 49
poskey_number_two_character = 50
poskey_number_three_character = 51
poskey_number_four_character = 52
poskey_number_five_character = 53
poskey_number_six_character = 54
poskey_number_seven_character = 55
poskey_number_eight_character = 56
poskey_number_nine_character = 57
# TODO reorganize and separate normal map loads, first map loads, and game loads

class MapInterface:
    def __init__(self, biome_map=None, initial_spawns=None, stairs=None):
        self.tcod_map = None
        self.explored = None
        self.xp_map = None
        # self.biome_map = biome_map
        self.initial_spawns = initial_spawns
        if self.initial_spawns:
            self.initial_spawns.owner = self
        self.map_id = None
        self.entities = []
        if stairs is None:
            self.stairs = [] # create an empty list
        else:
            self.stairs = stairs

    def update_map_dim(self, width, height):
        self.tcod_map = Map(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]

    def get_tcod_prop(self, x, y):
        return (self.tcod_map.transparent[x][y], self.tcod_map.walkable[x][y])

    def get_spawn_id(self, x, y):
        return self.spawn_map[x][y]

    def load_xp(self, map_id):
        self.map_id = map_id
        ###################
        # Find the path to the file to display
        cur_dir = os.path.dirname(__file__)
        file = os.path.join(cur_dir, map_id + '.xp')
        ###################

        ###################
        # Get data from the .xp file
        unzipped_file = gzip.open(file).read()  # Unzips the .xp file so we can call load_xp_string
        file_attributes = xpL.load_xp_string(unzipped_file)

        self.xp_map = file_attributes

        # print('loaded xp_map: ' + map_id)

    def convert_xp_to_game_map(self):
        self.update_map_dim(self.xp_map["layer_data"][0]["width"], self.xp_map["layer_data"][0]['height'])

        # self.update_map_dim(self.xp_map["layer_data"][0]["width"], self.xp_map["layer_data"][0]['height'])
        for x in range(self.xp_map["layer_data"][0]["width"]):
            for y in range(self.xp_map["layer_data"][0]['height']):
                cell_data = self.xp_map["layer_data"][0]['cells'][x][y]
                if cell_data['keycode'] == poskey_period_character:
                    self.tcod_map.transparent[x][y] = True
                    self.tcod_map.walkable[x][y] = True
                elif cell_data['keycode'] == poskey_pound_character:
                    self.tcod_map.transparent[x][y] = False
                    self.tcod_map.walkable[x][y] = False
                elif cell_data['keycode'] == poskey_capital_s_character:
                    self.tcod_map.transparent[x][y] = True
                    self.tcod_map.walkable[x][y] = True
                    spawn_stairs = Stairs(x, y)
                    self.stairs.append(spawn_stairs)
                self.explored[x][y] = False

    def load_stair_data(self):
        file_to_import = 'map_data.' + self.map_id
        imported_file = import_module(file_to_import)
        stair_list = getattr(imported_file, 'stairs')
        for stair_data in stair_list:
            parsed_stair_data = stair_data.strip().split("/")
            for stair_entity in self.stairs:
                if str(stair_entity.x) == parsed_stair_data[0] and str(stair_entity.y) == parsed_stair_data[1]:
                    stair_entity.dest_map_id = parsed_stair_data[2]

    def initialize_game_map(self, game_status):
        # print(str(self.map_id))
        game_status.world[self.map_id] = self
        game_status.current_map_id = self.map_id
        game_status.current_map = self
        # print(str(game_status.current_map_id))
        for stair_entity in self.stairs:
            if stair_entity.dest_map_id == game_status.current_map_id:
                # print('player at new stairs')
                game_status.player.x = stair_entity.x
                game_status.player.y = stair_entity.y
                # print('PlayerPosSet: ' + str(stair_entity.x) + ', ' + str(stair_entity.y))
                break
            elif stair_entity.dest_map_id == 'spawn':
                game_status.player.x = stair_entity.x
                game_status.player.y = stair_entity.y
                # print('PlayerPosSet: ' + str(stair_entity.x) + ', ' + str(stair_entity.y))
                break

    def check_if_map_is_loaded(self, game_status, stair):
        print('checking for map: ' + str(stair.dest_map_id))
        if game_status.world.get(stair.dest_map_id) is None:
            print('this is a new map')
            return False
        else:
            return True

    def climb_stairs(self, game_status, stair):
        # print('from' + str(self.map_id) + 'to' + stair.dest_map_id)

        # stores current exploration
        game_status.player.explored[self.map_id] = game_status.current_map.explored

        if self.check_if_map_is_loaded(game_status, stair):
            # print('loading previously used map')
            new_map_interface = game_status.world[stair.dest_map_id]
            if game_status.player.explored[stair.dest_map_id] is not None:
                # print('trying to load explored')
                new_map_interface.explored = game_status.player.explored[stair.dest_map_id]
        else:
            new_map_interface = MapInterface()
            new_map_interface.load_xp(stair.dest_map_id)
            new_map_interface.convert_xp_to_game_map()
            new_map_interface.load_stair_data()
            game_status.world[new_map_interface.map_id] = new_map_interface

            new_map_interface.initial_spawns = InitialSpawns(owner=new_map_interface)
            new_map_interface.initial_spawns.load_spawn_data()
            new_map_interface.initial_spawns.populate()


        originating_map_id = game_status.current_map_id
        game_status.current_map_id = new_map_interface.map_id
        game_status.current_map = new_map_interface
        # print('about to check for stair locations')
        # print('currently at' + str(originating_map_id))

        for stair_entity in game_status.current_map.stairs:
            if stair_entity.dest_map_id == 'spawn':
                spawn_stair = stair_entity
            elif stair_entity.dest_map_id == originating_map_id:
                print('player at new stairs')
                game_status.player.x = stair_entity.x
                game_status.player.y = stair_entity.y
                # print('PlayerPosSet: ' + str(stair_entity.x) + ', ' + str(stair_entity.y))
                break
        else:
            if stair_entity.dest_map_id == 'spawn':
                game_status.player.x = spawn_stair.x
                game_status.player.y = spawn_stair.y
                # print('PlayerPosSet: ' + str(spawn_stair.x) + ', ' + str(spawn_stair.y))


class Stairs(Entity):
    def __init__(self, x, y, dest_map_id=None):
        super(Stairs, self).__init__(x, y, 'S', (255, 255, 255), 'Stairs', render_order=RenderOrder.STAIRS)
        self.dest_map_id = dest_map_id

