import tdl


import constants
import map_utils
from death_functions import kill_monster, kill_player
from game_states import GameStates
from game_status import GameStatus
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from mob_spawner import InitialSpawns


def main():

    game_status_1 = GameStatus()

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title='Roguelike Tutorial Revised')
    con = tdl.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    left_panel = tdl.Console(constants.LEFT_PANEL_WIDTH, constants.LEFT_PANEL_HEIGHT)
    lower_panel = tdl.Console(constants.LOWER_PANEL_WIDTH, constants.LOWER_PANEL_HEIGHT)
    right_panel = tdl.Console(constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT)

    map_interface_one = map_utils.MapInterface()
    map_interface_one.load_xp('TestOne')
    map_interface_one.convert_xp_to_game_map()
    map_interface_one.load_stair_data()
    map_interface_one.initialize_game_map(game_status_1)

    map_interface_one.initial_spawns = InitialSpawns()
    map_interface_one.initial_spawns.owner = map_interface_one
    map_interface_one.initial_spawns.load_spawn_data()
    map_interface_one.initial_spawns.populate()


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
        fullscreen = action.get('fullscreen')
        if action.get('change panel') is not None:
            game_status_1.change_panel(action.get('change panel'))

        player_turn_results = []

        if move and game_status_1.game_state == GameStates.PLAYERS_TURN and game_status_1.active_panel == 'map':
            dx, dy = move

            player_turn_results, game_status_1.game_state =\
                game_status_1.player.movable.move_or_interact(dx, dy, game_status_1)

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                game_status_1.message_log.add_message(message)

            if dead_entity:
                if dead_entity == game_status_1.player:
                    message, game_status_1.game_state = kill_player(dead_entity, constants.colors)
                else:
                    message = kill_monster(dead_entity, constants.colors)

                    game_status_1.message_log.add_message(message)
        else:
            game_status_1.game_state = GameStates.ENEMY_TURN

        if game_status_1.game_state == GameStates.ENEMY_TURN:
            for entity in game_status_1.entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(game_status_1)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            game_status_1.message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == game_status_1.player:
                                message, game_status_1.game_state = kill_player(dead_entity, constants.colors)
                            else:
                                message = kill_monster(dead_entity, constants.colors)

                                game_status_1.message_log.add_message(message)

                            if game_status_1.game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_status_1.game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_status_1.game_state = GameStates.PLAYERS_TURN




if __name__ == '__main__':
    main()
