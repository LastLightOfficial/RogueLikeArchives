import math


class BasicMonster:
    def take_turn(self, game_status):
        results = []

        target = game_status.player

        monster = self.owner

        if game_status.current_map.tcod_map.fov[monster.x, monster.y]:
            if self.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_status)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results

    def move_towards(self, target_x, target_y, game_status):
        monster = self.owner

        path = game_status.current_map.tcod_map.compute_path(monster.x, monster.y, target_x, target_y)

        dx = path[0][0] - monster.x
        dy = path[0][1] - monster.y

        if game_status.current_map.tcod_map.walkable[path[1][0],path[1][1]]\
                and not monster.movable.move_check(game_status.entities, self.x + dx, self.y + dy):
            monster.movable.move(dx, dy) # TODO make sure this lines up with Enemy Entity like monster.movable.move

    def distance_to(self, other):
        monster = self.owner
        dx = other.x - monster.x
        dy = other.y - monster.y
        return math.sqrt(dx ** 2 + dy ** 2)