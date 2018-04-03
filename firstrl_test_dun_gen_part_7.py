import libtcodpy as libtcod
import math
import textwrap


# This was last worked on 7/15/2017
# As of 4/3/2018 I am commenting this so that I remember how far I have progressed.
# This was originally following the Rogue=like tutorial here:
# http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod
# This used Python2, originally. I was receiving help from the Roguelike Discord as well.
# They encouraged me to not use global variables, so I have the GameState class that essentially functioned as one.
# At this point I've learned more about Singletons and how to use them.

# Static Values
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 43
LIMIT_FPS = 20

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

color_last_light = libtcod.Color(0, 116, 153)
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

# parameters for generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3

# FOV values
FOV_ALGO = 2
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10


class GameState:
    def __init__(self):
        self.map_list = []
        self.fov_map_list = []
        self.fov_recompute = True
        self.the_game_state = 'playing'
        self.player_action = None
        self.current_map = None

    def update_current_game_map(self, game_map, fov_map):
        self.current_map = game_map
        self.map_list.append(game_map)
        self.current_fov_map = fov_map
        self.fov_map_list.append(fov_map)


class GameMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(True) for y in xrange(height)] for x in xrange(width)]

    def create_room(self, room):  # usage floorOne.create_room(rectangle)
        # go through the tiles in the rectangle and make them passable
        for x in xrange(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in xrange(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in xrange(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def generate_map(self):
        rooms = []
        num_rooms = 0

        for r in range(MAX_ROOMS):
            # random width and height
            w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            # random position within map boundaries
            x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

            new_room = Rect(x, y, w, h)

            failed = False
            # check for intersections
            for other_room in rooms:
                if new_room.is_intersecting(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections/overlap so the room is valid

                # 'paint' it to map tile's
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, and player spawn
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    if libtcod.random_get_int(0, 0, 1) == 1:
                        new_x += libtcod.random_get_int(0, 0, (new_room.w / 2) - 1)
                    else:
                        new_x -= libtcod.random_get_int(0, 0, (new_room.w / 2) - 1)

                    if libtcod.random_get_int(0, 0, 1) == 1:
                        new_y += libtcod.random_get_int(0, 0, (new_room.h / 2) - 1)
                    else:
                        new_y -= libtcod.random_get_int(0, 0, (new_room.h / 2) - 1)

                    if libtcod.random_get_int(0, 0, 1) == 1:
                        # creates horizontal, then vertical tunnel
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # creates vertical then horizontal tunnel
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # adds content to the room
                place_objects(self, new_room)

                # append new room to the list
                rooms.append(new_room)
                num_rooms += 1


class Tile:
    # a tile of the game_map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # all tiles start unexplored
        self.explored = False

        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Rect:
    # a rectangle on the map, used to characterize a room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h

    def center(self):
        center_x = (self.x1 + self.x2)/2
        center_y = (self.y1 + self.y2)/2
        return (center_x, center_y)

    def is_intersecting(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)


class Entity:
    # this is a generic object: the player, a monster, an item, the stairs
    # it's always represented by a character on screen
    def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None):
        self.name = name
        self.blocks = blocks
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy, game_state):
        # move by the given amount, if destination is not blocked
        if not is_blocked(game_state.current_map, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y, game_state):
        # vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1, then round it and ocnvert it to integer
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy, game_state)

    def player_move_or_attack(self, dx, dy, game_state):
        tentative_x = self.x + dx
        tentative_y = self.y + dy

        target = None
        for stuff in objects:
            if stuff.fighter and stuff.x == tentative_x and stuff.y == tentative_y:
                target = stuff
                break

        if target is not None:
            player.fighter.attack(target, game_state)
        else:
            player.move(dx, dy, game_state)
            game_state.fov_recompute = True

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def send_to_back(self):
        global objects
        objects.remove(self)
        objects.insert(0, self)

    def draw(self, game_state):
        if libtcod.map_is_in_fov(game_state.current_fov_map, self.x, self.y):
            # set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)


class Fighter:
    # combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, death_function=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def attack(self, target, game_state):
        damage = self.power - target.fighter.defense

        if damage > 0:
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage, game_state)
        else:
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

    def take_damage(self, damage, game_state):
        if damage > 0:
            self.hp -= damage

            if self.hp <= 0:
                function = self.death_function
                if function is player_death:
                    player_death(self.owner, game_state)
                elif function is not None:
                    function(self.owner)


class BasicMonster:
    # AI for a basic monster.
    def take_turn(self, game_state, player):
        monster = self.owner
        if libtcod.map_is_in_fov(game_state.current_fov_map, monster.x, monster.y):

            # needs to move closer
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y, game_state)

            # close enough, attack
            elif player.fighter.hp > 0:
                monster.fighter.attack(player, game_state)


def is_blocked(game_map, x, y):
    if game_map.tiles[x][y].blocked:
        return True

    for stuff in objects:
        if stuff.blocks and stuff.x == x and stuff.y == y:
            return True

    return False


def place_objects(game_map, room):  # room is type Rect
    # choose random number of monsters to spawn
    num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        x = libtcod.random_get_int(0, room.x1, room.x2)
        y = libtcod.random_get_int(0, room.y1, room.y2)

        if not is_blocked(game_map, x, y):
            spawn_choice = libtcod.random_get_int(0, 0, 100)
            if spawn_choice < 60:  # 60% spawn rate
                fighter_component = Fighter(hp=10, defense=0, power=3, death_function=monster_death)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'o', 'orc', libtcod.desaturated_amber, blocks=True,
                                 fighter=fighter_component, ai=ai_component)
            elif spawn_choice < 60+20:  # the next 20%
                fighter_component = Fighter(hp=10, defense=1, power=2, death_function=monster_death)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'g', 'greblin', libtcod.desaturated_green, blocks=True,
                                 fighter=fighter_component, ai=ai_component)
            else:  # final 20%
                fighter_component = Fighter(hp=16, defense=1, power=4, death_function=monster_death)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'T', 'troll', libtcod.darker_green, blocks=True,
                                 fighter=fighter_component, ai=ai_component)

            objects.append(monster)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    # render the bar on top
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, x + total_width /2, y,
                             libtcod.BKGND_NONE, libtcod.CENTER, name + ": " + str(value) + '/' + str(maximum))


def get_names_under_mouse(game_state):
    global mouse
    global objects

    # return a string with the names of all objects under the mouse
    (x, y) = (mouse.cx, mouse.cy)

    names = [obj.name for obj in objects
             if obj.x == x and obj.y == y and libtcod.map_is_in_fov(game_state.current_fov_map, obj.x, obj.y)]

    names = ', '.join(names)
    return names.capitalize()


def render_all(game_state):

    if game_state.fov_recompute:
        game_state.fov_recompute = False
        libtcod.map_compute_fov(game_state.current_fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    # go through all tiles, and set their background color
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

    # draw all objects in the list
    for entity in objects:
        if entity != player:
            entity.draw(game_state)
    player.draw(game_state)

    # blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)

    # prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # print the game messages, one line at a time
    msg_iterator = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, msg_iterator, libtcod.BKGND_NONE, libtcod.LEFT, line)
        msg_iterator += 1

    # show the player's stats
    render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    # display names of objects under the mouse
    libtcod.console_set_default_foreground(panel, libtcod.light_grey)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(game_state))

    # blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)


def message(new_msg, color=libtcod.white):
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]

        game_msgs.append((line, color))


def handle_keys(game_state):

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle Fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  # exit game

    if game_state.the_game_state == 'playing':
        # movement keys
        if key.vk == libtcod.KEY_UP:
            player.player_move_or_attack(0, -1, game_state)
        elif key.vk == libtcod.KEY_DOWN:
            player.player_move_or_attack(0, 1, game_state)
        elif key.vk == libtcod.KEY_LEFT:
            player.player_move_or_attack(-1, 0, game_state)
        elif key.vk == libtcod.KEY_RIGHT:
            player.player_move_or_attack(1, 0, game_state)
        else:
            return 'didnt-take-turn'


def player_death(player, game_state):
    message('You died!', libtcod.red)
    game_state.the_game_state = 'dead'

    player.char = '%'
    player.color = libtcod.dark_red


def monster_death(monster):
    message(monster.name.capitalize() + ' is dead!', libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()

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

# panel
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

# Uncomment below for real-time
# libtcod.sys_set_fps(LIMIT_FPS)

# create object representing the player
fighter_component = Fighter(hp=30, defense=2, power=5, death_function=player_death)
player = Entity(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', 'player', libtcod.white,
                blocks=True, fighter=fighter_component)

# list of objects with those two
objects = [player]

# generate map
game_state_1 = GameState()

test_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
test_map.generate_map()
# create FOV map
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for h in range(MAP_HEIGHT):
    for w in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, w, h,
                                   not test_map.tiles[w][h].block_sight, not test_map.tiles[w][h].blocked)

game_state_1.update_current_game_map(test_map, fov_map)

# create the list of game messages and their colors, starts empty
game_msgs = []


message('Welcome stranger! Prepare to die hehe XD FILLER FILLER FILLER FILLER FILLER', libtcod.red)

mouse = libtcod.Mouse()
key = libtcod.Key()


###########
# Main Loop
###########

while not libtcod.console_is_window_closed():

    # render the screen
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
    render_all(game_state_1)

    libtcod.console_flush()

    # erase all objects at their old locations, before they move
    for local_entity in objects:
        local_entity.clear()

    # handle keys and exit game if needed
    player_action = handle_keys(game_state_1)
    if player_action == 'exit':
        break

    if game_state_1.the_game_state == 'playing' and player_action != 'didnt-take-turn':
        for thing in objects:
            if thing.ai:
                thing.ai.take_turn(game_state_1, player)
