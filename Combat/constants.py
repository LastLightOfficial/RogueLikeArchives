from enum import Enum

SCREEN_WIDTH = 118
SCREEN_HEIGHT = 80

MAP_WINDOW_WIDTH = 80
MAP_WINDOW_HEIGHT = 60

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
MSG_HEIGHT = LOWER_PANEL_HEIGHT - 4

RIGHT_UI_X = MAP_WINDOW_WIDTH
RIGHT_UI_WIDTH = SCREEN_WIDTH - MAP_WINDOW_WIDTH
RIGHT_UI_HEIGHT = SCREEN_HEIGHT


RIGHT_MENU_START_STR_X = 4
RIGHT_MENU_START_STR_Y = 10

FOV_ALGORITHM = 'BASIC'
FOV_LIGHT_WALLS = True
FOV_RADIUS = 30


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


