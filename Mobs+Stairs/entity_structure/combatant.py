from entity_structure.entity import Entity
from constants import RenderOrder
from game_messages import Message


class Combatant(Entity):
    def __init__(self, x=None, y=None, char=None, color=None, name=None, health=None, strength=None, blocks=True,
                 render_order=RenderOrder.ACTOR):
        super().__init__(x, y, char, color, name, blocks, render_order)
        self.max_health = health
        self.health = health
        self.strength = strength
        self.skills = {}
        self.inventory = []

    def take_damage(self, amount):
        results = []

        self.health -= amount

        if self.health <= 0:
            results.append({'dead': self})

        return results

    def attack(self, target):
        results = []

        damage = self.strength

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.name.capitalize(), target.name, str(damage)))})
            results.extend(target.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.name.capitalize(), target.name))})

        return results
