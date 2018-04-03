class Combatant:
    def __init__(self, health=0, strength=0, agility=0, endurance=0, mob_number=10):
        self.max_health = health
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        self.mob_number = mob_number
        self.sword_skills_list = {}
        self.move_intent = []  # will be a list of move commands
        self.ss_intent = []
        self.move_to_execute = []
        self.ss_to_execute = []