from entity_structure.combatant import Combatant
from constants import RenderOrder


class Enemy(Combatant):

    def __init__(self, x=None, y=None, char=None, color=None, name=None, health=None, blocks=True,
                 render_order=RenderOrder.ACTOR, movable=None, ai=None):
        super().__init__(x, y, char, color, name,
                         health=health, blocks=True, render_order=RenderOrder.ACTOR)
        self.movable = movable
        if self.movable:
            self.movable.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self
