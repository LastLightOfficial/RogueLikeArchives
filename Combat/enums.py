from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    STAIRS = 2
    ITEM = 3
    ACTOR = 4


class GameStates(Enum):
    PLAYERS_TURN = 1
    ALLIES_TURN = 2
    ENEMY_TURN = 3
    CALCULATE_TURN = 5
    RESOLVE_TURN = 6
    MOB_SPAWN = 7
    PLAYER_PROMPT = 10
    SKILLS_MENU = 11
    INVENTORY_MENU = 12
    PLAYER_DEAD = 21


class Team(Enum):
    PLAYER = 1
    ALLY = 2
    ENEMY = 3


class EntityStatus(Enum):
    MOVEMENT = 0
    SWORDSKILL = 1
