from entity_structure.combatant import Entity
from constants import RenderOrder
from game_messages import Message


class Item(Entity):
    def __init__(self, x=None, y=None, char=None, color=None, name=None, blocks=False, render_order=RenderOrder.ITEM):
        super().__init__(x, y, char, color, name, blocks=blocks, render_order=render_order)

    def pick_up(self, entity, game_status):
        results = []

        entity.inventory.append(self)
        results.append({'message': Message('{0} places {1} in their inventory'.format(
            entity.name.capitalize(), self.name.capitalize()))})
        game_status.current_map.entities.remove(self)

        return results
