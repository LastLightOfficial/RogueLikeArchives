from entity_structure.enemy import Enemy
from entity_structure.item import Item
from map_utils import Stairs
from game_states import GameStates
from game_messages import Message
from constants import RenderOrder


class PlayerMovable:
    def is_walkable_check(self, destination_x, destination_y, game_status):
        if game_status.current_map.tcod_map.walkable[destination_x, destination_y]:
            return True
        else:
            return False

    def interaction_check(self, destination_x, destination_y, game_status):
        results = []
        for entity in game_status.current_map.entities:
            if entity.blocks and entity.x == destination_x and entity.y == destination_y:
                results.append(entity)
            if entity.x == destination_x and entity.y == destination_y:
                results.append(entity)
        for stair in game_status.current_map.stairs:
            if stair.x == destination_x and stair.y == destination_y:
                # debug msg print('found stair')
                results.append(stair)

        return results

    def move_or_interact(self, dx, dy, game_status):
        results = []

        gamestate = GameStates.PLAYERS_TURN

        player = self.owner

        destination_x = player.x + dx
        destination_y = player.y + dy

        if self.is_walkable_check(destination_x, destination_y, game_status):
            interact = self.interaction_check(destination_x, destination_y, game_status)

            if not interact:
                player.x = destination_x
                player.y = destination_y
                gamestate = GameStates.ENEMY_TURN

                game_status.fov_recompute = True
            elif isinstance(interact[0], Enemy) and interact[0].render_order == RenderOrder.ACTOR:
                results.extend(self.owner.attack(interact[0]))
                game_status.fov_recompute = True
                gamestate = GameStates.ENEMY_TURN
            elif isinstance(interact[0], Item):
                player.x = destination_x
                player.y = destination_y
                results.extend(interact[0].pick_up(game_status.player, game_status))
                game_status.fov_recompute = True
                gamestate = GameStates.ENEMY_TURN
            elif isinstance(interact[0], Enemy) and interact[0].render_order == RenderOrder.CORPSE:
                player.x = destination_x
                player.y = destination_y
                results.append({'message': Message('{0} squishes under {1}\'s foot'.format(
                    interact[0].name.capitalize(), game_status.player.name.capitalize()))})
                game_status.fov_recompute = True
            elif isinstance(interact[0], Stairs) and interact[0].dest_map_id != 'spawn':
                # debug msg print('found stair 2.0')
                # Move the entity by a given amount
                player.x = destination_x
                player.y = destination_y
                results.append({'message': Message('{0} tries to climb the stairs to {1}'.format(
                    self.owner.name.capitalize(), interact[0].dest_map_id))})

                game_status.current_map.climb_stairs(game_status, interact[0])

                game_status.fov_recompute = True


        return results, gamestate
