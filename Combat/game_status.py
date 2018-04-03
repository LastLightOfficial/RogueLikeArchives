from ai.player_ai import PlayerLogic
from constants import MSG_X, MSG_WIDTH, MSG_HEIGHT
from entity_structure.combatant import Combatant
from entity_structure.entity import Entity
from enums import RenderOrder, GameStates, Team
from game_messages import MessageLog


class GameStatus:
    def __init__(self):
        self.message_log = MessageLog(MSG_X, MSG_WIDTH, MSG_HEIGHT)
        self.fov_recompute = True
        self.game_state = GameStates.PLAYERS_TURN
        self.panel_state = None
        self.active_panel = 'map' # TODO temporary
        self.world = {}
        self.current_map = None
        self.current_map_id = None
        player_combatant = Combatant(health=50, strength=10, agility=10, endurance=10, mob_number=0)
        player_logic = PlayerLogic()
        self.player = Entity(x=40, y=20, char='@', color=(255, 255, 255), name='Player', blocks=True,
                             render_order=RenderOrder.ACTOR, team=Team.PLAYER,
                             ai=player_logic, combatant=player_combatant)
        self.nothing_entity = Entity(name='nothing')

    def change_panel(self, new_panel):
        return None
