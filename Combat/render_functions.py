import constants


def render_message_panel(game_status, con, root_console, colors):

    con.clear(fg=colors.get('white'), bg=colors.get('black'))
    con.draw_frame(0, 0, constants.LOWER_PANEL_WIDTH, constants.LOWER_PANEL_HEIGHT, None,
                           bg=colors.get('light_gray'))

    # Print the game messages, one line at a time
    y = 2
    for message in game_status.message_log.messages:
        con.draw_str(2, y, message.text, bg=None, fg=message.color)
        y += 1

    root_console.blit(con, constants.LOWER_PANEL_X, constants.LOWER_PANEL_Y, constants.LOWER_PANEL_WIDTH,
                      constants.LOWER_PANEL_HEIGHT, 0, 0)


def display_skills(game_status, right_panel, colors):

    str_pos_y = 10
    right_panel.draw_str(3, str_pos_y, 'Skills', fg=colors.get('white'), bg=None)

    str_pos_y += 2
    skill_number = 1

    for skill in game_status.player.combatant.sword_skills_list:
        right_panel.draw_str(3, str_pos_y, str(skill_number) + " - ", fg=colors.get('white'), bg=None)
        right_panel.draw_str(7, str_pos_y, skill, fg=colors.get('white'), bg=None)
        skill_number += 1
        str_pos_y += 1


def render_right_panel(game_status, right_panel, root_console, colors):

    right_panel.draw_frame(0, 0, constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT, None,
                           bg=colors.get('light_gray'))
    right_panel.draw_frame(0, 8, constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT - 8, None,
                           bg=colors.get('light_gray'))
    if True:
        display_skills(game_status, right_panel, colors)
    root_console.blit(right_panel, constants.RIGHT_UI_X, 0, constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT, 0, 0)



def render_map(game_status, con, root_console, colors):
    if game_status.active_panel == 'map':
        con.draw_frame(0, 0, constants.MAP_WINDOW_WIDTH, constants.MAP_WINDOW_HEIGHT, None,
                       bg=colors.get('light_gray'))
    else:
        con.draw_frame(0, 0, constants.MAP_WINDOW_WIDTH, constants.MAP_WINDOW_HEIGHT, None,
                       bg=colors.get('gray'))

    if game_status.fov_recompute: # TODO this is currently drawing over the frame, causing the frame to flash

        camera_offset_x = find_camera_x(game_status)
        camera_offset_y = find_camera_y(game_status)

        for x, y in game_status.current_map.tcod_map:
            wall = not game_status.current_map.tcod_map.transparent[x, y]

            if game_status.current_map.tcod_map.fov[x, y]:
                if wall:
                    con.draw_char(x + camera_offset_x, y + camera_offset_y,
                                  None, fg=None, bg=colors.get('light_wall'))
                else:
                    con.draw_char(x + camera_offset_x, y + camera_offset_y,
                                  None, fg=None, bg=colors.get('light_ground'))

                game_status.current_map.explored[x][y] = True
            elif game_status.current_map.explored[x][y]:
                if wall:
                    con.draw_char(x + camera_offset_x, y + camera_offset_y,
                                  None, fg=None, bg=colors.get('dark_wall'))
                else:
                    con.draw_char(x + camera_offset_x, y + camera_offset_y,
                                  None, fg=None, bg=colors.get('dark_ground'))

    # Draw all entities in the list
    entities_in_render_order = sorted(game_status.current_map.entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(game_status, con, entity)

    draw_entity(game_status, con, game_status.player)

    root_console.blit(con, 0, 0, constants.MAP_WINDOW_WIDTH, constants.MAP_WINDOW_HEIGHT, 0, 0)

def draw_entity(game_status, con, entity):
    if game_status.current_map.tcod_map.fov[entity.x, entity.y]:
        con.draw_char(entity.x + find_camera_x(game_status), entity.y + find_camera_y(game_status),
                      entity.char, entity.color, bg=None)


def find_camera_x(game_status):
    if game_status.current_map.tcod_map.width < constants.MAP_WINDOW_WIDTH:  # if the map is smaller than the window
        return (constants.MAP_WINDOW_WIDTH - game_status.current_map.tcod_map.width) // 2  # display map centered
    elif game_status.player.x < (constants.MAP_WINDOW_WIDTH / 2):  # if the player is near left edge of the map
        return 0  # display up to left edge of map
    elif game_status.player.x >= game_status.current_map.tcod_map.width - (constants.MAP_WINDOW_WIDTH / 2):
        # when player is near right edge of map
        return game_status.current_map.tcod_map.width - constants.MAP_WINDOW_WIDTH  # display up to right edge of map
    else:  # this means player is not near edge of map
        return 0 - (game_status.player.x - (constants.MAP_WINDOW_WIDTH // 2))  # display player in center of window


def find_camera_y(game_status):
    if game_status.current_map.tcod_map.height < constants.MAP_WINDOW_HEIGHT:
        return (constants.MAP_WINDOW_HEIGHT - game_status.current_map.tcod_map.height) // 2
    elif game_status.player.y < (constants.MAP_WINDOW_HEIGHT / 2):
        return 0
    elif game_status.player.y >= game_status.current_map.tcod_map.height - (constants.MAP_WINDOW_HEIGHT / 2):
        return game_status.current_map.tcod_map.height - constants.MAP_WINDOW_HEIGHT
    else:
        return 0 - (game_status.player.y - (constants.MAP_WINDOW_HEIGHT // 2))


def render_all(game_status, con, left_panel, lower_panel, right_panel, root_console, colors):

    render_map(game_status, con, root_console, colors)
    render_message_panel(game_status, lower_panel, root_console, colors)
    render_right_panel(game_status, right_panel, root_console, colors)


def clear_entity(con, entity, game_status):
    # erase the character that represents this object
    con.draw_char(entity.x + find_camera_x(game_status), entity.y+ find_camera_y(game_status),
                  ' ', entity.color, bg=None)


def clear_all(con, game_status):
    for entity in game_status.current_map.entities:
        clear_entity(con, entity, game_status)
    clear_entity(con, game_status.player, game_status)