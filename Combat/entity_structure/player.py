from entity_structure.entity import Entity
from entity_structure.combatant import Combatant
from ai.player_ai import PlayerLogic
from enums import RenderOrder, Team


class Player(Entity):
    def __init__(self):
        player_combatant = Combatant(health=50, strength=10, agility=10, endurance=10, mob_number=0)
        player_logic = PlayerLogic()
        super().__init__(x=40, y=20, char='@', color=(255, 255, 255), name='Player', blocks=True,
                             render_order=RenderOrder.ACTOR, team=Team.PLAYER,
                             ai=player_logic, combatant=player_combatant)