from constants import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x=None, y=None, char=None, color=None, name=None, blocks=False, render_order=RenderOrder.CORPSE):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
