from constants import MSG_X, MSG_WIDTH, MSG_HEIGHT
from entity_structure.player import Player
from game_messages import MessageLog
from game_states import GameStates
from movables.player_movable import PlayerMovable
from constants import RenderOrder


class GameStatus:
    def __init__(self):
        player_movable = PlayerMovable()
        self.player = Player(10, 10, '@', (255, 255, 255), 'Player', health=30, strength=5, blocks=True,
                             render_order=RenderOrder.ACTOR, movable=player_movable)
        # print('playerhealth at init_game: ' + str(self.player.health))
        self.entities = []
        self.fov_recompute = True
        self.message_log = MessageLog(MSG_X, MSG_WIDTH, MSG_HEIGHT)
        self.mouse_coordinates = (0, 0)
        self.active_panel = 'map'
        self.last_active_tab = 'inventory'
        self.world = {}
        self.current_map = None
        self.current_map_id = None
        self.current_fov_map = None
        self.game_state = GameStates.PLAYERS_TURN
        self.explored = None

    def change_panel(self, new_panel):
        if new_panel == 'map':
            if self.active_panel is 'inventory':
                self.last_active_tab = 'inventory'
                self.active_panel = 'map'
            elif self.active_panel is 'two':
                self.last_active_tab = 'two'
                self.active_panel = 'map'
            elif self.active_panel is 'three':
                self.last_active_tab = 'three'
                self.active_panel = 'map'
            elif self.active_panel is 'four':
                self.last_active_tab = 'four'
                self.active_panel = 'map'
            elif self.active_panel is 'five':
                self.last_active_tab = 'five'
                self.active_panel = 'map'
        if new_panel == 'next':
            if self.active_panel is 'inventory':
                self.last_active_tab = 'inventory'
                self.active_panel = 'two'
            elif self.active_panel is 'two':
                self.last_active_tab = 'two'
                self.active_panel = 'three'
            elif self.active_panel is 'three':
                self.last_active_tab = 'three'
                self.active_panel = 'four'
            elif self.active_panel is 'four':
                self.last_active_tab = 'four'
                self.active_panel = 'five'
            elif self.active_panel is 'five':
                self.last_active_tab = 'five'
                self.active_panel = 'map'
            elif self.active_panel is 'map':
                self.active_panel = 'inventory'
