import libtcodpy as libtcod
import math
import textwrap


# This part of the project was my first attempt to create static maps instead of generating them.
# This took approximately 3 days, from 7/12-7/15 2017 (guessing based on last modified dates)
# This version did not take advantage of REXPaint and instead used text files with "#" and "."
# Looking through my files, it appears, I never really made a composite version of this and instead started
# a large number of new files to test various parts.

# Static Values
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 80

MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
LOWER_PANEL_HEIGHT = 20
LOWER_PANEL_Y = SCREEN_HEIGHT - LOWER_PANEL_HEIGHT
# LOWER_PANEL_WIDTH = MAP_WIDTH
# LOWER_PANEL_X = 0

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = MAP_WIDTH - BAR_WIDTH - 42
MSG_HEIGHT = LOWER_PANEL_HEIGHT - 1

RIGHT_UI_X = MAP_WIDTH + 2
RIGHT_UI_WIDTH = SCREEN_WIDTH - MAP_WIDTH - 2
RIGHT_UI_HEIGHT = SCREEN_HEIGHT

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
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10


def render_panels():


    # prepare to render the GUI panel
    libtcod.console_set_default_background(lower_panel, libtcod.black)
    libtcod.console_clear(lower_panel)

    # print the game messages, one line at a time
    msg_iterator = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(lower_panel, color)
        libtcod.console_print_ex(lower_panel, MSG_X, msg_iterator, libtcod.BKGND_NONE, libtcod.LEFT, line)
        msg_iterator += 1


def message(new_msg, color=libtcod.white):
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]

        game_msgs.append((line, color))


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
lower_panel = libtcod.console_new(MAP_WIDTH, LOWER_PANEL_HEIGHT)
right_panel = libtcod.console_new(RIGHT_UI_WIDTH, RIGHT_UI_HEIGHT)

# Uncomment below for real-time
# libtcod.sys_set_fps(LIMIT_FPS)


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
    render_panels()

    libtcod.console_flush()

    # erase all objects at their old locations, before they move
    for local_entity in objects:
        local_entity.clear()

    # handle keys and exit game if needed
    game_exit = handle_keys()
    if game_exit:
        break
