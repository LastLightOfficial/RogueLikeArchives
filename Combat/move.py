from game_messages import Message

class MoveCommand:
    def __init__(self):
        self.time = None
        self.x = None
        self.y = None
        self.owner = None
        self.interrupted = False
        self.bumps_into = None
        self.final_move_command = False

    def execute(self):
        results = []

        if self.interrupted:
            results.append({'message': Message('{0} is cut off by {1}'.format(
                self.owner.name.capitalize(), self.bumps_into.name.capitalize()
            ))})
        else:
            print(self.owner.name + ' moves to: ' + str(self.x) + ", " + str(self.y))
            self.owner.x = self.x
            self.owner.y = self.y

        # tentatively only clearing moves on the last move, but shouldnt matter since they should be stored
        # in timings for the execution phase
        if self.final_move_command:
            self.owner.combatant.move_intent = []

        return results