from entity_structure.player import Player
from game_messages import Message


class BasicMonsterMovable:
    def is_walkable_check(self, destination_x, destination_y, game_status):
        if game_status.current_map.tcod_map.walkable[destination_x, destination_y]:
            return True
        else:
            return False

    def interaction_check(self, destination_x, destination_y, game_status):

        if game_status.player.x == destination_x and game_status.player.y == destination_y:
            return game_status.player

        for entity in game_status.current_map.entities:
            if entity.blocks and entity.x == destination_x and entity.y == destination_y:
                return entity

        return None

    def move_or_interact(self, dx, dy, game_status):
        results = []

        monster = self.owner

        destination_x = monster.x + dx
        destination_y = monster.y + dy

        if self.is_walkable_check(destination_x, destination_y, game_status):
            interact = self.interaction_check(destination_x, destination_y, game_status)
            if isinstance(interact, Player):
                results.append({'message': Message('{0} tries to attack {1}'.format(
                    self.owner.name.capitalize(), interact.name))})
            elif isinstance(interact, Enemy):
                results.append({'message': Message('{0} says Hello! to {1}'.format(
                    self.owner.name.capitalize(), interact.name))})
                pass
            elif interact is None:
                monster.x = destination_x
                monster.y = destination_y
                pass

        return results