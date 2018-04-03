from game_messages import Message

class IneffectiveAttack: # this is a placeholder skill for feedback tests
    def __init__(self):
        self.damage_formula = None
        self.frame_data = []
        self.windup = 0
        self.activation_arc = 0.2
        self.post_motion_delay = 0.9
        self.actual_wu = self.windup
        self.actual__aa = self.activation_arc
        self.actual_pmd = self.post_motion_delay
        self.results = None

    def prepare(self, user, dx, dy): # TODO have WU, AA, PMD be affected by user stats
        self.frame_data = []
        dest_x = user.x + dx
        dest_y = user.y + dy
        actual_wu = self.windup
        actual__aa = self.activation_arc
        actual_pmd = self.post_motion_delay
        self.frame_data.append([dest_x, dest_y, actual_wu, actual__aa, actual_pmd])
        # print(user.name + ' is preparing to attack at ' + str(dest_x) + ", " + str(dest_y))

        user.combatant.ss_intent = self

    def calculate(self, game_status, user):
        results = []

        for strike in self.frame_data:  # Single hit SS will not need this clause
            # this pulls the prepared frame data
            dest_x = strike[0]
            dest_y = strike[1]
            wu = strike[2]
            aa = strike[3]
            pmd = strike[4]
            print('trying to attack at: ' + str(dest_x) + ', ' + str(dest_y))

            for entity in game_status.current_map.entities:
                for move_command in entity.combatant.move_intent:
                    print('move_command.x: ' + str(move_command.x))
                    print('move_command.y: ' + str(move_command.y))
                    if (move_command.x == dest_x) and (move_command.y == dest_y):
                        print('found match')
                        # normally, calculate frames vs target and handle damage
                        results.append(IneffectiveAttackWindUp(user, entity))
                        results.append(IneffectiveAttackActiveArc(user, entity, aa))
            else:
                if not results:
                    # if results are empty
                    results.append(IneffectiveAttackWindUp(user, game_status.nothing_entity))
                    results.append(IneffectiveAttackActiveArc(user, game_status.nothing_entity, aa))

        return results



class IneffectiveAttackWindUp:
    def __init__(self, user, target, time=0):
        self.user = user
        self.target = target
        self.time = time

    def execute(self):
        results = []

        results.append({'message': Message('{0} prepares to attack {1}'.format(
            self.user.name.capitalize(), self.target.name.capitalize()
        ))})

        return results


class IneffectiveAttackActiveArc:
    def __init__(self, user, target, time):
        self.user = user
        self.target = target
        self.time = time

    def execute(self):
        results = []

        results.append({'message': Message('{0} ineffectively attacks {1}'.format(
            self.user.name.capitalize(), self.target.name.capitalize()))})

        return results
