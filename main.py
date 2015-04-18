#!/usr/bin/env python

from engine import Player, Game, GridSpace, Ship, AlreadyAttacked


def create_fleet_view(player):
    view = [['_'] * player.grid_dimension[0]
            for _ in xrange(player.grid_dimension[1])]

    for coord in player.grid.keys():
        grid_space = player.grid[coord]
        coord_tuple = player.split_coord(coord)
        index_tuple = player.coord_tuple_to_index_tuple(coord_tuple)

        (x, y) = index_tuple

        if grid_space.is_miss():
            view[x][y] = 'O'
        elif grid_space.is_hit():
            view[x][y] = 'X'
        elif grid_space.ship:
            view[x][y] = 'S'

    return view


def create_target_view(player):
    view = [['_'] * player.grid_dimension[0]
            for _ in xrange(player.grid_dimension[1])]

    for coord in player.grid.keys():
        grid_space = player.grid[coord]
        coord_tuple = player.split_coord(coord)
        index_tuple = player.coord_tuple_to_index_tuple(coord_tuple)

        (x, y) = index_tuple

        if grid_space.is_miss():
            view[x][y] = 'O'

        if grid_space.is_hit():
            view[x][y] = 'X'

    return view


def convert_index_to_label(index):
    return chr(index + 65)


def print_view(view, grid_dimension):
    (x, y) = grid_dimension

    lines = []

    column_headers = ['{0}'.format(i + 1) for i in range(y)]

    column_header_left_padding = ' ' * 5
    column_header_right_padding = ' ' * 3

    lines.append(column_header_left_padding +
                 '  '.join(column_headers) + column_header_right_padding)

    lines.append('  +--------------------------+')

    row_number = 0
    for row in view:
        row_text = '{0} |  '.format(convert_index_to_label(row_number))
        row_text += '  '.join(row)
        row_text += '  |'

        lines.append(row_text)
        row_number += 1

    lines.append('  +--------------------------+')

    return lines


def render_fleet_view(player):
    return print_view(create_fleet_view(player), player.grid_dimension)


def render_target_view(player):
    return print_view(create_target_view(player), player.grid_dimension)


def render_views(game):
    fleet_view = render_fleet_view(game.current_player)
    target_view = render_target_view(game.current_opponent)

    print '\n'

    for view_tuple in zip(fleet_view, target_view):
        print '          '.join(view_tuple)


if __name__ == '__main__':
    p1_carrier = Ship.carrier()
    p1 = Player('Player One')
    p1.place_ship(p1_carrier, ['D4', 'E4', 'F4', 'G4', 'H4'])

    p2_destroyer = Ship.destroyer()

    p2 = Player('Player Two')
    p2.place_ship(p2_destroyer, ['A1', 'A2'])

    game = Game(p1, p2)

    playing = True
    render_views(game)
    while playing:

        valid_coord = False
        while playing and not valid_coord:
            command = raw_input(
                '\nYour turn, ' + game.current_player.name + ': ').strip().upper()

            if command == 'QUIT':
                playing = False
            elif command == 'SHOW':
                render_views(game)
            elif (not p1.valid_coord(command)):
                print '\nPlease enter a valid co-ordinate (e.g. C7), "show" to view the board, or quit" to end game.'
            else:
                valid_coord = True

        if playing:
            try:
                outcome = game.take_turn(command)
            except AlreadyAttacked:
                print ('\n{0} has already been attacked.'.format(command))
            else:
                print '\n{0}: {1}'.format(command, outcome)
                playing = not outcome.is_game_over()
                render_views(game)

    print('\n')