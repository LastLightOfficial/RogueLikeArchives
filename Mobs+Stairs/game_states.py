from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ALLIES_TURN = 2
    ENEMY_TURN = 3
    MOB_SPAWN = 4
    PLAYER_DEAD = 5