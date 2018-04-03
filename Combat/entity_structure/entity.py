from enums import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x=None, y=None, char=None, color=None, name=None, blocks=False, render_order=RenderOrder.CORPSE,
                 team=None, ai=None, combatant=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name

        self.blocks = blocks
        self.render_order = render_order
        self.team = team

        self.ai = ai
        if self.ai:
            self.ai.owner = self
        self.combatant = combatant
        if self.combatant:
            self.combatant.owner = self

        self.tentative_position = None

    def move(self, dest_x, dest_y):
        self.x = dest_x
        self.y = dest_y
