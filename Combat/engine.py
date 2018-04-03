import tdl

import map_utils
import constants
from operator import attrgetter, itemgetter
from enums import RenderOrder, GameStates, Team, EntityStatus
from input_handlers import handle_keys
from game_status import GameStatus
from game_messages import Message
from render_functions import render_all, clear_all
from mob_spawns import InitialSpawns
from map_utils import MapInterface

from sword_skills.ineffective_attack import IneffectiveAttack


def main():

    # Initialization stuff
    game_status_1 = GameStatus()

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
    root_console = tdl.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title='Roguelike Tutorial Revised')
    con = tdl.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    left_panel = tdl.Console(constants.LEFT_PANEL_WIDTH, constants.LEFT_PANEL_HEIGHT)
    lower_panel = tdl.Console(constants.LOWER_PANEL_WIDTH, constants.LOWER_PANEL_HEIGHT)
    right_panel = tdl.Console(constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT)

    map_interface_one = map_utils.MapInterface()
    map_interface_one.load_xp('TestOne for Combat')
    map_interface_one.convert_xp_to_game_map()
    map_interface_one.initialize_game_map(game_status_1)
    map_interface_one.entities = [game_status_1.player]

    map_interface_one.initial_spawns = InitialSpawns()
    map_interface_one.initial_spawns.owner = map_interface_one
    map_interface_one.initial_spawns.load_spawn_data()
    map_interface_one.initial_spawns.populate()

    game_status_1.message_log.add_message(Message('Welcome Player!'))

    # TODO temp
    game_status_1.player.combatant.sword_skills_list['Ineffective Attack'] = IneffectiveAttack()

    # Main Loop
    while not tdl.event.is_window_closed():
        if game_status_1.fov_recompute:
            game_status_1.current_map.tcod_map.compute_fov(game_status_1.player.x, game_status_1.player.y,
                                                           radius=constants.FOV_RADIUS,
                                                           light_walls=constants.FOV_LIGHT_WALLS,
                                                           fov=constants.FOV_ALGORITHM)

        render_all(game_status_1, con, left_panel, lower_panel, right_panel, root_console, constants.colors)
        tdl.flush()

        clear_all(con, game_status_1)

        game_status_1.fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                game_status_1.mouse_coordinates = event.cell
        else:
            user_input = None

        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit = action.get('exit')
        skill = action.get('skill')
        fullscreen = action.get('fullscreen')
        if action.get('change panel') is not None:
            game_status_1.change_panel(action.get('change panel'))

        # print('reset')
        # player_turn_expectations = [None, None]
        # game_status_1.player.combatant.move_expectations = None #TODO move these somewhere that makes sense
        # game_status_1.player.combatant.ss_expectations = None #TODO not needed?

        if move and game_status_1.game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            game_status_1.player.ai.update_tentative_position(game_status_1, dx, dy)

        if skill and game_status_1.game_state == GameStates.PLAYERS_TURN:
            game_status_1.message_log.add_message(Message('Awaiting Directional Input'))
            game_status_1.game_state = GameStates.PLAYER_PROMPT

        if move and game_status_1.game_state == GameStates.PLAYER_PROMPT:
            game_status_1.game_state = GameStates.PLAYERS_TURN
            dx, dy = move
            game_status_1.player.combatant.sword_skills_list['Ineffective Attack'].prepare(game_status_1.player, dx, dy)
            game_status_1.player.ai.stationary_position()

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if game_status_1.player.combatant.move_intent or game_status_1.player.combatant.ss_intent:
            game_status_1.game_state = GameStates.ENEMY_TURN
            print('ENEMY TURN')

        if game_status_1.game_state == GameStates.ENEMY_TURN:
            for entity in game_status_1.current_map.entities:
                pass
                if entity.team == Team.ENEMY and entity.render_order == RenderOrder.ACTOR:
                    entity.ai.prepare_turn(game_status_1)
                    # entity.ai.take_turn(game_status_1)
            else:
                game_status_1.game_state = GameStates.CALCULATE_TURN
                print('CALC TURN')

        if game_status_1.game_state == GameStates.CALCULATE_TURN:
            timing = []

            for entity in game_status_1.current_map.entities:
                timing.extend(entity.ai.calculate_turn(game_status_1))

            else:
                for entity in game_status_1.current_map.entities:
                    entity.combatant.move_intent = []
                    entity.combatant.ss_intent = []

                game_status_1.game_state = GameStates.RESOLVE_TURN
                game_status_1.fov_recompute = True
                print('RESOLVE TURN')

        if game_status_1.game_state == GameStates.RESOLVE_TURN:
            sorted_timing = sorted(timing, key=attrgetter('time'))
            print('there are ' + str(len(sorted_timing)) + ' actions')
            for action in sorted_timing:
                results = action.execute()
                if results:
                    for result in results:
                        game_status_1.message_log.add_message((result.get('message')))


            else:
                game_status_1.game_state = GameStates.PLAYERS_TURN
                game_status_1.fov_recompute = True
                print('TO PLAYER TURN')












if __name__ == '__main__':
    main()