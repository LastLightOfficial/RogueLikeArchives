from entity_structure.combatant import Combatant
from constants import RenderOrder


class Player(Combatant):

    def __init__(self, x, y, char, color, name, health=None, strength=None, blocks=True, render_order=RenderOrder.ACTOR,
                 movable=None):
        super().__init__(x, y, char, color, name,
                         health=health, blocks=True, render_order=RenderOrder.ACTOR)
        self.strength = strength
        self.movable = movable
        if self.movable:
            self.movable.owner = self
        self.explored = {}

