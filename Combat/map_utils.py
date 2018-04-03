import gzip
import os
import xpLoaderPy3 as xpL

from tdl.map import Map


poskey_period_character = 46
# pound
poskey_pound_character = 35


class MapInterface:
    def __init__(self):
        self.tcod_map = None
        self.explored = None
        self.xp_map = None
        self.map_id = None
        self.initial_spawns = None
        self.entities = []

    def update_map_dim(self, width, height):
        self.tcod_map = Map(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]

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
                self.explored[x][y] = True  # TODO change this to False later

    def initialize_game_map(self, game_status):
        # print(str(self.map_id))
        game_status.world[self.map_id] = self
        game_status.current_map_id = self.map_id
        game_status.current_map = self