from tdl.map import Map

from random import randint
from render_functions import RenderOrder
from entity import Entity

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




class MapInterface:
    def __init__(self, width, height, biome_map=None, spawn_map=None, stairs=None):
        self.tcod_map = Map(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]
        self.xp_map = None
        # self.biome_map = biome_map
        self.spawn_map = spawn_map
        self.map_id = None
        if stairs is None:
            self.stairs = [] # create an empty list
        else:
            self.stairs = stairs

    def get_tcod_prop(self, x, y):
        return (self.tcod_map.transparent[x][y], self.tcod_map.walkable[x][y])

    # def get_biome(self, x, y):
        # return self.biome_map[x][y]

    def get_spawn_id(self, x, y):
        return self.spawn_map[x][y]

    def get_stair(self, x, y):
        return self.stairs[x][y]


class Stairs(Entity):
    def __init__(self, x, y, dest_map_id=None):
        super(Stairs, self).__init__(x, y, 'S', (255, 255, 255), 'Stairs', render_order=RenderOrder.STAIRS)
        self.dest_map_id = dest_map_id


def convert_to_game_map(map_interface):
    for x in range(map_interface.xp_map["layer_data"][0]["width"]):
        for y in range(map_interface.xp_map["layer_data"][0]['height']):
            cell_data = map_interface.xp_map["layer_data"][0]['cells'][x][y]
            if cell_data['keycode'] == poskey_period_character:
                map_interface.tcod_map.transparent[x][y] = True
                map_interface.tcod_map.walkable[x][y] = True
            elif cell_data['keycode'] == poskey_pound_character:
                map_interface.tcod_map.transparent[x][y] = False
                map_interface.tcod_map.walkable[x][y] = False
            elif cell_data['keycode'] == poskey_capital_s_character:
                map_interface.tcod_map.transparent[x][y] = True
                map_interface.tcod_map.walkable[x][y] = True
                spawn_stairs = Stairs(x, y)
                map_interface.stairs.append(spawn_stairs)
                print('stair created')
            map_interface.explored[x][y] = False


def load_stair_data(game_status, map_interface, map_id):
    with open(map_id + ".txt") as f:
        line_one = f.readline().strip()
        line_two = f.readline().strip()
        line_three = f.readline().strip()
        line_four = f.readline().strip()



def initial_populate_game_map(game_status, map_interface):
    if game_status.player.x is None:
        for stair_entity in map_interface.stairs:
            if stair_entity.dest_map_id == 'spawn':
                game_status.player.x = stair_entity.x
                game_status.player.y = stair_entity.y
                game_status.current_map_id = map_interface.map_id
                game_status.current_map = map_interface
                print('PlayerPosSet')
    else:
        for stair_entity in map_interface.stairs:
            if stair_entity.dest_map_id == game_status.current_map_id:
                game_status.player.x = stair_entity.x
                game_status.player.y = stair_entity.y
                game_status.current_map_id = map_interface.map_id
                game_status.current_map = map_interface
                print('PlayerPosSet')


def load_xp(map_interface, file_attributes, reverse_endian=True):
    map_interface.xp_map = file_attributes
    print('width: ' + str(file_attributes["width"]))
    print('height: ' + str(file_attributes["height"]))
    print('layer_data: ' + str(file_attributes["layer_data"]))

