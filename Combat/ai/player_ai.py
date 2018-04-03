from move import MoveCommand


class PlayerLogic:
    def is_walkable(self, game_status, dx, dy):
        player = self.owner

        destination_x = player.x + dx
        destination_y = player.y + dy

        for entity in game_status.current_map.entities:
            if entity.x == destination_x and entity.y == destination_y and entity.blocks == True:
                return False

        if game_status.current_map.tcod_map.walkable[destination_x, destination_y]:
            return True
        else:
            print('movement blocked')
            return False

    def update_tentative_position(self, game_status, dx, dy):
        player = self.owner
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

            # print('x_direction: ' + str(x_direction))
            # print('y_direction: ' + str(y_direction))
            # print('tiles_occupied: ' + str(tiles_occupied))

            time_elapsed = 0
            x_pos = player.x
            y_pos = player.y
            for i in range(0, tiles_occupied + 1):
                move_command = MoveCommand()
                move_command.time = time_elapsed
                move_command.x = x_pos
                move_command.y = y_pos
                move_command.owner = player
                if i == tiles_occupied:
                    move_command.final_move_command = True
                player.combatant.move_intent.append(move_command)
                print('appending move command: ' + player.name + ' moves to: ' + str(x_pos) + ", " + str(y_pos))
                x_pos += (i + int(x_direction))
                y_pos += (i + int(y_direction))
                time_elapsed += time_on_tile

        else:
            return None

    def stationary_position(self):
        player = self.owner
        move_command = MoveCommand()
        move_command.time = 0
        move_command.x = player.x
        move_command.y = player.y
        move_command.owner = player
        player.combatant.move_intent.append(move_command)

    def calculate_turn(self, game_status):
        timing = []
        player = self.owner

        if not player.combatant.move_intent:
            self.stationary_position()

        tent_pos_ls = player.combatant.move_intent

        player.combatant.move_to_execute = self.check_move(game_status, tent_pos_ls)
        # print('there are ' + str(len(tent_pos_ls)) + ' commands')
        for move_command in tent_pos_ls:
            if move_command.time != 0:  # removes t0 move commands as they are not needed to be executed...maybe
                timing.append(move_command)
                # this appends because it returns a single Object
                # print('appending timing')

        if player.combatant.ss_intent:  # this only ever contains a single object
            timing.extend(player.combatant.ss_intent.calculate(game_status, player))
            # this is extend b/c it returns a list of two Objects

        return timing

    def check_move(self, game_status, tent_ls):  # TODO include enemy pos enemy ss

        player = self.owner

        for move_command in tent_ls:
            for entity in game_status.current_map.entities:
                if entity is not player:
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
                                    pass  # player takes priority in cases where AGI is identical
                        else:  # command is clear and did not match with any others
                            pass  # command goes through

        return tent_ls
