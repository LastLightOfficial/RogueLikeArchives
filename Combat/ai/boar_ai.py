import math
from move import MoveCommand


class BasicBoarAI:
    def is_walkable(self, game_status, dx, dy):
        boar = self.owner

        destination_x = boar.x + dx
        destination_y = boar.y + dy

        if game_status.current_map.tcod_map.walkable[destination_x, destination_y]:
            return True
        else:
            print('movement blocked')
            return False

    def update_tentative_position(self, game_status, dx, dy):
        monster = self.owner
        if self.is_walkable(game_status, dx, dy):
            x_tiles_occupied = abs(dx) + 1
            if dx == 0:
                x_direction = 0
            else:
                x_direction = dx / abs(dx)
            x_time_on_tile = 1000 // x_tiles_occupied

            y_tiles_occupied = abs(dy) + 1
            if dy == 0:
                y_direction = 0
            else:
                y_direction = dy / abs(dy)
            y_time_on_tile = 1000 // y_tiles_occupied

            if x_time_on_tile > y_time_on_tile:
                time_on_tile = x_time_on_tile
                tiles_occupied = x_tiles_occupied
            else:
                time_on_tile = y_time_on_tile
                tiles_occupied = y_tiles_occupied

            print('boar x_direction: ' + str(x_direction))
            print('boar y_direction: ' + str(y_direction))
            print('boar tiles_occupied: ' + str(tiles_occupied))

            time_elapsed = 0
            x_pos = monster.x
            y_pos = monster.y
            pos = (x_pos, y_pos)
            for i in range(0, tiles_occupied + 1):
                # use x_pos and y_pos as the key in the dictionary
                pos = (x_pos, y_pos)
                print('adding pos: ' + str(pos))
                move_command = MoveCommand()
                move_command.time = time_elapsed
                move_command.x = x_pos
                move_command.y = y_pos
                move_command.owner = monster
                if i == tiles_occupied:
                    move_command.final_move_command = True
                monster.combatant.move_intent.append(move_command)
                x_pos += (i + int(x_direction))
                y_pos += (i + int(y_direction))
                time_elapsed += time_on_tile
        else:
            return None

    def stationary_position(self):
        monster = self.owner
        move_command = MoveCommand()
        move_command.time = 0
        move_command.x = monster.x
        move_command.y = monster.y
        move_command.owner = monster
        monster.combatant.move_intent.append(move_command)

    def move_towards(self, game_status, other):
        monster = self.owner

        path = game_status.current_map.tcod_map.compute_path(monster.x, monster.y, other.x, other.y, diagonal_cost=0)

        dx = path[0][0] - monster.x
        dy = path[0][1] - monster.y

        if game_status.current_map.tcod_map.walkable[path[1][0], path[1][1]]:
            return self.update_tentative_position(game_status, dx, dy)

    def distance_to(self, other):
        monster = self.owner
        dx = other.x - monster.x
        dy = other.y - monster.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def prepare_turn(self, game_status):
        monster = self.owner
        print(monster.name + ' is preparing their turn')
        player = game_status.player

        # print('distance between is: ' + str(self.distance_to(player)))

        if self.distance_to(player) > 10:
            self.stationary_position()
            return None
        elif 1 < self.distance_to(player) <= 10:
            # print('boar tries to move towards player')
            self.move_towards(game_status, player)
        elif self.distance_to(player) <= 1:
            self.stationary_position()
            dx = player.x - monster.x
            dy = player.y - monster.y
            monster.combatant.sword_skills_list['IneffectiveAttack'].prepare(monster, dx, dy)

    def calculate_turn(self, game_status):  # this is called by the engine
        timing = []
        monster = self.owner
        # print(monster.name + ' is calculating their turn')
        tent_pos_ls = monster.combatant.move_intent
        print(monster.name + ' move intent: ' + str(monster.combatant.move_intent))

        monster.combatant.move_to_execute = self.check_move(game_status, tent_pos_ls)

        for move_command in tent_pos_ls:
            if move_command.time != 0:
                timing.append(move_command)

        if monster.combatant.ss_intent:
            timing.extend(monster.combatant.ss_intent.calculate(game_status, monster))

        return timing

    def check_move(self, game_status, tent_ls):  # TODO include other stuffs

        monster = self.owner

        for move_command in tent_ls:
            for entity in game_status.current_map.entities:
                if entity is not monster:
                    for other_move_command in entity.combatant.move_intent:
                        if move_command.x == other_move_command.x and move_command.y == other_move_command.y:
                            if move_command.time > other_move_command.time:
                                move_command.interrupted = True
                                move_command.bumps_into = entity
                            elif move_command.time < other_move_command.time:
                                pass  # this command goes through
                            else:  # case where its the same frame
                                if move_command.owner.combatant.agility < other_move_command.owner.combatant.agility:
                                    move_command.interrupted = True
                                    move_command.bumps_into = entity
                                elif move_command.owner.combatant.agility > other_move_command.owner.combatant.agility:
                                    pass  # this command goes through
                                else:  # case where its the same agility
                                    if move_command.owner.combatant.mob_number >\
                                            other_move_command.owner.combatant.mob_number:
                                        move_command.interrupted = True
                                        move_command.bumps_into = entity
                                    elif move_command.owner.combatant.mob_number <\
                                            other_move_command.owner.combatant.mob_number:
                                        pass  # this command goes through
                                    else:
                                        print('ya dun goofed, there are two mobs with the same number')
                        else:  # command is clear and did not match with any others
                            pass  # command goes through

        return tent_ls


