from enum import Enum

SCREEN_WIDTH = 118
SCREEN_HEIGHT = 80

bar_width = 20
panel_height = 7
PANEL_Y = SCREEN_HEIGHT - panel_height

MAP_WINDOW_WIDTH = 80
MAP_WINDOW_HEIGHT = 60

TAB_WIDTH = 6
TAB_HEIGHT = 5

TAB_ONE_X = 2
TAB_TWO_X = 9
TAB_THREE_X = 16
TAB_FOUR_X = 23
TAB_FIVE_X = 30


LEFT_PANEL_WIDTH = 22
LEFT_PANEL_HEIGHT = 20
# LEFT_PANEL_X = 0
LEFT_PANEL_Y = SCREEN_HEIGHT - LEFT_PANEL_HEIGHT

LOWER_PANEL_HEIGHT = 20
LOWER_PANEL_Y = SCREEN_HEIGHT - LOWER_PANEL_HEIGHT
LOWER_PANEL_WIDTH = MAP_WINDOW_WIDTH - LEFT_PANEL_WIDTH
LOWER_PANEL_X = LEFT_PANEL_WIDTH

MSG_X = LOWER_PANEL_X + 2
MSG_WIDTH = LOWER_PANEL_WIDTH - 4 # 2 UNIT BUFFER ON SIDES
MSG_HEIGHT = LOWER_PANEL_HEIGHT - 2

RIGHT_UI_X = MAP_WINDOW_WIDTH
RIGHT_UI_WIDTH = SCREEN_WIDTH - MAP_WINDOW_WIDTH
RIGHT_UI_HEIGHT = SCREEN_HEIGHT


INVENTORY_STR_X = 4
INVENTORY_STR_Y = TAB_HEIGHT + 5


PLAYER_POS_X = MAP_WINDOW_WIDTH / 2
PLAYER_POS_Y = MAP_WINDOW_HEIGHT / 2

FOV_ALGORITHM = 'BASIC'
FOV_LIGHT_WALLS = True
FOV_RADIUS = 15

max_monsters_per_room = 3

colors = {
    'dark_wall': (0, 0, 100),
    'dark_ground': (50, 50, 150),
    'light_wall': (130, 110, 50),
    'light_ground': (200, 180, 50),
    'desaturated_green': (63, 127, 63),
    'darker_green': (0, 127, 0),
    'dark_red': (191, 0, 0),
    'white': (255, 255, 255),
    'lighter_gray': (225, 225, 225),
    'light_gray': (175, 175, 175),
    'gray': (125, 125, 125),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'orange': (255, 127, 0),
    'light_red': (255, 114, 114),
    'darker_red': (127, 0, 0)
    }





class RenderOrder(Enum):
    CORPSE = 1
    STAIRS = 2
    ITEM = 3
    ACTOR = 4
