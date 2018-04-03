class BasicMonster:
    def take_turn(self, game_status):
        results = []

        target = game_status.player

        monster = self.owner

        if game_status.current_map.tcod_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_status)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results

