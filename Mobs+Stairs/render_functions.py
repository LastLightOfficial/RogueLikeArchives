from entity_structure.enemy import Enemy
import constants



def get_names_under_mouse(mouse_coordinates, entities, game_status):
    camera_offset_x = find_camera_x(game_status)
    camera_offset_y = find_camera_y(game_status)
    x, y = mouse_coordinates

    if game_status.player.x + camera_offset_x == x and game_status.player.y + camera_offset_y == y:
        return game_status.player.name

    names = [entity.name for entity in entities
             if entity.x + camera_offset_x == x and entity.y + camera_offset_y == y and\
             game_status.current_map.tcod_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()


def get_entity_under_mouse(mouse_coordinates, entities, game_status):
    camera_offset_x = find_camera_x(game_status)
    camera_offset_y = find_camera_y(game_status)
    x, y = mouse_coordinates

    if game_status.player.x + camera_offset_x == x and game_status.player.y + camera_offset_y == y:
        return game_status.player

    for entity in entities:
        if entity.x + camera_offset_x == x and entity.y + camera_offset_y == y and\
                game_status.current_map.tcod_map.fov[entity.x, entity.y]:
            return entity


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)


def render_enemy_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)


def render_tab(panel, x, y, w, h, string, frame_color, back_color, string_color):

    panel.draw_rect(x, y, w, h, None, bg=back_color)
    text = string
    if string is not None:
        x_centered = x + int((w - len(text)) / 2)
        panel.draw_str(x_centered, h - (h / 2 - 1), text, fg=string_color, bg=None)


def render_map(game_status, con, root_console, colors):
    if game_status.active_panel == 'map':
        con.draw_frame(0, 0, constants.MAP_WINDOW_WIDTH, constants.MAP_WINDOW_HEIGHT, None,
                       bg=colors.get('light_gray'))
    else:
        con.draw_frame(0, 0, constants.MAP_WINDOW_WIDTH, constants.MAP_WINDOW_HEIGHT, None,
                       bg=colors.get('gray'))

    if game_status.fov_recompute:

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

        for stair_entity in game_status.current_map.stairs:
            if game_status.current_map.tcod_map.fov[stair_entity.x, stair_entity.y]:
                con.draw_char(stair_entity.x + camera_offset_x,
                              stair_entity.y + camera_offset_y, stair_entity.char,
                              fg=stair_entity.color, bg=colors.get('light_ground'))
                game_status.current_map.explored[stair_entity.x][stair_entity.y] = True
            elif game_status.current_map.explored[stair_entity.x][stair_entity.y]:
                con.draw_char(stair_entity.x + camera_offset_x,
                              stair_entity.y + camera_offset_y, stair_entity.char,
                              fg=stair_entity.color, bg=colors.get('dark_ground'))

    # Draw all entities in the list
    entities_in_render_order = sorted(game_status.current_map.entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(game_status, con, entity)

    draw_entity(game_status, con, game_status.player)

    root_console.blit(con, 0, 0, constants.MAP_WINDOW_WIDTH, constants.MAP_WINDOW_HEIGHT, 0, 0)


def render_right_panel(game_status, right_panel, root_console, colors):

    if game_status.active_panel == 'map':
        panel_status = game_status.active_panel + game_status.last_active_tab
    elif game_status.active_panel == 'inventory' or game_status.active_panel == 'two' or game_status.active_panel ==\
            'three' or game_status.active_panel == 'four' or game_status.active_panel == 'five':
        panel_status = game_status.active_panel

    if panel_status == 'mapinventory':
        render_tab(right_panel, 0, constants.TAB_HEIGHT + 3, constants.RIGHT_UI_WIDTH,
                   constants.RIGHT_UI_HEIGHT - constants.TAB_HEIGHT -1,
                   None, colors.get('light_gray'), colors.get('gray'), colors.get('white'))
        right_panel.draw_frame(0, constants.TAB_HEIGHT + 3, constants.RIGHT_UI_WIDTH,
                               constants.RIGHT_UI_HEIGHT - constants.TAB_HEIGHT - 1,
                               None,  bg=colors.get('light_gray'))
        render_tab(right_panel, constants.TAB_ONE_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'one',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_TWO_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'two',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_THREE_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'three',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_FOUR_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'four',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_FIVE_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'five',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        display_inventory(game_status, right_panel, colors.get('white'), colors)
    elif panel_status == 'inventory':
        render_tab(right_panel, 0, constants.TAB_HEIGHT + 3, constants.RIGHT_UI_WIDTH,
                   constants.RIGHT_UI_HEIGHT - constants.TAB_HEIGHT - 1,
                   None, colors.get('light_gray'), colors.get('gray'), colors.get('white'))
        right_panel.draw_frame(0, constants.TAB_HEIGHT + 3, constants.RIGHT_UI_WIDTH,
                               constants.RIGHT_UI_HEIGHT - constants.TAB_HEIGHT - 1,
                               None, bg=colors.get('light_gray'))  # TODO this probably extends below the screen
        right_panel.draw_frame(1, constants.TAB_HEIGHT + 4, constants.RIGHT_UI_WIDTH - 2,
                               constants.RIGHT_UI_HEIGHT - constants.TAB_HEIGHT - 5,
                               None, bg=colors.get('lighter_gray'))
        render_tab(right_panel, constants.TAB_ONE_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'one',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_TWO_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'two',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_THREE_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'three',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_FOUR_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'four',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        render_tab(right_panel, constants.TAB_FIVE_X, 2, constants.TAB_WIDTH, constants.TAB_HEIGHT, 'five',
                   colors.get('lighter_gray'), colors.get('light_gray'), colors.get('white'))
        display_inventory(game_status, right_panel, colors.get('white'), colors)


def display_inventory(game_status, right_panel, string_color, colors):

    str_pos_y = constants.INVENTORY_STR_Y
    right_panel.draw_str(constants.INVENTORY_STR_X - 1, str_pos_y, 'Inventory', fg=string_color, bg=None)
    right_panel.draw_frame(0, str_pos_y + 1, constants.RIGHT_UI_WIDTH,
                           constants.RIGHT_UI_HEIGHT - constants.TAB_HEIGHT - 1,
                           None, bg=colors.get('light_gray'))
    str_pos_y += 3
    for thing in game_status.player.inventory:
        text = thing.name.capitalize()
        right_panel.draw_str(constants.INVENTORY_STR_X, str_pos_y, text, fg=string_color, bg=None)
        str_pos_y += 1



def render_all(game_status, con, left_panel, lower_panel, right_panel, root_console, colors):

    render_map(game_status, con, root_console, colors)

    right_panel.clear(fg=colors.get('white'), bg=colors.get('lighter_gray'))

    render_right_panel(game_status, right_panel, root_console, colors)

    right_panel.draw_frame(0, 0, constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT, None,
                           fg=colors.get('lighter_gray'), bg=colors.get('light_gray'))
    root_console.blit(right_panel, constants.RIGHT_UI_X, 0, constants.RIGHT_UI_WIDTH, constants.RIGHT_UI_HEIGHT, 0, 0)

    lower_panel.clear(fg=colors.get('white'), bg=colors.get('black'))
    lower_panel.draw_frame(0, 0, constants.LOWER_PANEL_WIDTH, constants.LOWER_PANEL_HEIGHT, None,
                           bg=colors.get('light_gray'))

    # Print the game messages, one line at a time
    y = 1
    for message in game_status.message_log.messages:
        lower_panel.draw_str(1, y, message.text, bg=None, fg=message.color)
        y += 1

    root_console.blit(lower_panel, constants.LOWER_PANEL_X, constants.LOWER_PANEL_Y, constants.LOWER_PANEL_WIDTH,
                      constants.LOWER_PANEL_HEIGHT, 0, 0)

    # Left Panel

    left_panel.clear(fg=colors.get('white'), bg=colors.get('black'))

    left_panel.draw_rect(0, 0, constants.LEFT_PANEL_WIDTH, constants.LEFT_PANEL_HEIGHT,
                         None, bg=colors.get('light_gray'))
    left_panel.draw_rect(1, 1, constants.LEFT_PANEL_WIDTH - 2, constants.LEFT_PANEL_HEIGHT - 2,
                         None, bg=colors.get('lighter_gray'))

    left_panel.draw_str(1, 1, game_status.player.name)

    render_bar(left_panel, 1, 2, constants.bar_width, 'HP', game_status.player.health,
               game_status.player.max_health, colors.get('light_red'), colors.get('darker_red'),
               colors.get('white'))


    left_panel.draw_str(1, 3, get_names_under_mouse(game_status.mouse_coordinates,
                                                    game_status.current_map.entities, game_status))

    entity_under_mouse = get_entity_under_mouse(game_status.mouse_coordinates,
                                                game_status.current_map.entities, game_status)

    if isinstance(entity_under_mouse, Enemy):
        render_enemy_bar(left_panel, 1, 4, constants.bar_width, 'HP',
                         get_entity_under_mouse(game_status.mouse_coordinates, game_status.current_map.entities,
                                                game_status).health,
                         get_entity_under_mouse(game_status.mouse_coordinates, game_status.current_map.entities,
                                                game_status).max_health,
                         colors.get('light_red'), colors.get('darker_red'),
                         colors.get('white'))

    root_console.blit(left_panel, 0, constants.LEFT_PANEL_Y, constants.LEFT_PANEL_WIDTH, constants.LEFT_PANEL_HEIGHT,
                      0, 0)


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
    elif game_status.player.y < constants.MAP_WINDOW_HEIGHT / 2:
        return 0
    elif game_status.player.y >= game_status.current_map.tcod_map.height - constants.MAP_WINDOW_HEIGHT / 2:
        return game_status.current_map.tcod_map.height - constants.MAP_WINDOW_HEIGHT
    else:
        return 0 - (game_status.player.y - (constants.MAP_WINDOW_HEIGHT // 2))


def clear_all(con, game_status):
    for entity in game_status.current_map.entities:
        clear_entity(con, entity)
    clear_entity(con, game_status.player)


def draw_entity(game_status, con, entity):
    if game_status.current_map.tcod_map.fov[entity.x, entity.y]:
        con.draw_char(entity.x + find_camera_x(game_status), entity.y + find_camera_y(game_status),
                      entity.char, entity.color, bg=None)


def clear_entity(con, entity):
    # erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
