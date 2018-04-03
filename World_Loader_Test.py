import libtcodpy as libtcod
import math
import textwrap


# See "firstrl.py" comments
# This appears to be the version that took the txt files and converted into a visible map.

# Static Values
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 43
LIMIT_FPS = 20

color_last_light = libtcod.Color(0, 116, 153)
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

# FOV values
FOV_ALGO = 2
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10


class GameState:
    def __init__(self):
        self.game_msgs = []
        self.key = libtcod.Key()
        self.player = Entity(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', 'player', color_last_light)
        self.objects = [self.player]  # TODO add player
        self.active_panel = 'map'
        self.fov_recompute = True
        self.the_game_state = 'playing'
        self.player_action = None
        self.world = {}
        self.dungeon = {}
        self.current_map = None
        self.current_fov_map = None


    def load_overworld(self, map_id, old_map_id=None): # Overworld is composed of multiple floors
        if self.world.get(map_id) is None:
            with open("001.txt") as f:
                print('opened')
                map_id_one = f.readline()
                map_id_two = f.readline()
                map_id_three = f.readline()
                map_id_four = f.readline()
                str_width = f.readline()
                str_height = f.readline()
                width = int(str_width)
                height = int(str_height)
                new_game_map = GameMap(width, height)
                line_counter = 0
                for line in f:
                    ch_counter = 0
                    for ch in line:

                        if ch == '#':
                            new_game_map.tiles[ch_counter][line_counter].make_wall()
                            print('made wall')
                        elif ch == '.':
                            new_game_map.tiles[ch_counter][line_counter].make_open()
                            print('made open')
                        elif ch == '1':
                            new_game_map.tiles[ch_counter][line_counter].make_portal(map_id_one)
                            self.player.x = ch_counter
                            self.player.y = line_counter
                        elif ch == '2':
                            new_game_map.tiles[ch_counter][line_counter].make_portal(map_id_two)
                        elif ch == '3':
                            new_game_map.tiles[ch_counter][line_counter].make_portal(map_id_three)
                        elif ch == '4':
                            new_game_map.tiles[ch_counter][line_counter].make_portal(map_id_four)
                        ch_counter += 1
                    line_counter += 1
            self.world[map_id] = new_game_map
            self.current_map = self.world[map_id]
            fov_map = libtcod.map_new(width, height)
            self.current_fov_map = fov_map
            for h in range(height):
                for w in range(width):
                    libtcod.map_set_properties(fov_map, w, h,
                                               not self.current_map.tiles[w][h].block_sight,
                                               not self.current_map.tiles[w][h].impassable)


    def load_dungeon_floor(self, map_id):
        with open(map_id + ".txt") as f:
            new_map_id = f.readline()
            width = f.readline()
            height = f.readline()
            new_game_map = GameMap(width, height)
            for line in f:
                for ch in f:
                    if ch == 'w':
                        new_game_map.tiles[ch, line].make_wall()
                    elif ch == 'o':
                        new_game_map.tiles[ch, line].make_open()
                    elif ch == 's':
                        new_game_map.tiles[ch, line].make_spawn()
                    elif ch == 'f':
                        new_game_map.tiles[ch, line].make_stairs(new_map_id)
        self.dungeon[map_id] = new_game_map


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(True, True) for y in range(height)] for x in range(width)]


class Tile:
    def __init__(self, impassable=True, block_sight=True, explored=True, stairs=None):
        self.impassable = impassable
        self.block_sight = block_sight
        self.explored = explored
        self.stairs = stairs

    def make_wall(self):
        self.impassable = True
        self.block_sight = True

    def make_open(self):
        self.impassable = False
        self.block_sight = False

    def make_portal(self, map_id):
        self.impassable = False
        self.block_sight = False
        self.stairs = map_id


class Entity:
    def __init__(self,  x, y, char, name, color):
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy, game_state):
        # move by the given amount, if destination is not blocked
        if not is_blocked(game_state.current_map, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            game_state.fov_recompute = True


    def player_move_or_attack(self, dx, dy, game_state):
        self.move(dx, dy, game_state)

    def draw(self, game_state):
        if libtcod.map_is_in_fov(game_state.current_fov_map, self.x, self.y):
            # set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)


def is_blocked(game_map, x, y):
    if game_map.tiles[x][y].impassable:
        return True

    else:
        return False


def render_map(game_state):
    if game_state.fov_recompute:
        # recompute FOV if needed
        game_state.fov_recompute = False
        libtcod.map_compute_fov(game_state.current_fov_map, game_state.player.x, game_state.player.y,
                                TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = libtcod.map_is_in_fov(game_state.current_fov_map, x, y)
            wall = game_state.current_map.tiles[x][y].block_sight
            if not visible:
                # out of player's FOV
                if game_state.current_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
            else:
                if wall:
                    libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET)
                game_state.current_map.tiles[x][y].explored = True

    for entity in game_state.objects:
        if entity:
            entity.draw(game_state)
    game_state.player.draw(game_state)

    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)


def handle_keys(game_state):

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle Fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  # exit game

    if game_state.the_game_state == 'playing':
        # movement keys
        if key.vk == libtcod.KEY_UP:
            game_state.player.player_move_or_attack(0, -1, game_state)
        elif key.vk == libtcod.KEY_DOWN:
            game_state.player.player_move_or_attack(0, 1, game_state)
        elif key.vk == libtcod.KEY_LEFT:
            game_state.player.player_move_or_attack(-1, 0, game_state)
        elif key.vk == libtcod.KEY_RIGHT:
            game_state.player.player_move_or_attack(1, 0, game_state)
        else:
            return 'didnt-take-turn'


################
# Initialization
################

# Setting up font
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

# Initializing window
# False = Not Fullscreen
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)

# off-screen console
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)





# generate map
game_state_1 = GameState()

# list of objects with those two


game_state_1.load_overworld('001')


mouse = libtcod.Mouse()
key = libtcod.Key()


###########
# Main Loop
###########

while not libtcod.console_is_window_closed():
    # render the screen
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
    render_map(game_state_1)

    libtcod.console_flush()

    for local_entity in game_state_1.objects:
        local_entity.clear()

    player_action = handle_keys(game_state_1)
    if player_action == 'exit':
        break
