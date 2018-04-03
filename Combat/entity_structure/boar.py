from entity_structure.entity import Entity
from entity_structure.combatant import Combatant
from enums import RenderOrder, Team
from ai.boar_ai import BasicBoarAI
from sword_skills.ineffective_attack import IneffectiveAttack


class Boar(Entity):
    def __init__(self, x=None, y=None, char='b', color=(255, 114, 114), name='Boar', blocks=True,
                 render_order=RenderOrder.ACTOR, team=Team.ENEMY, ai=BasicBoarAI(), combatant=Combatant()):
        super().__init__(x=x, y=y, char=char, color=color, name=name, blocks=blocks, render_order=render_order,
                         team=team, ai=ai, combatant=combatant)
        self.combatant.sword_skills_list['IneffectiveAttack'] = IneffectiveAttack()