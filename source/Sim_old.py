import sys

import pygame as pg

from quad_tree import Node, Quad
from person import Person


def draw_screen(screen, groups: list[list[Person]], person_size: int, node_size: int) -> None:
    screen.fill('#303030')

    for draw_group in groups:
        # declare all draw variables
        x_start, x_end = draw_group[0].x_range
        y_start, y_end = draw_group[0].y_range
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(x_start, y_start, x_end - x_start, y_end - y_start), 2)
        node_offset = node_size // 2

        # draw each node in group
        for draw_person in draw_group:
            # find draw center based on person position and node size
            person_center = (draw_person.x_position + node_offset, draw_person.y_position + node_offset)

            # draw nodes based on test result
            if draw_person.test_result == 'h':
                pg.draw.circle(screen, '#29a3a3', person_center, person_size // 2)
                # pg.draw.rect(screen, (255, 0, 0), pg.Rect(person.move_target[0], person.move_target[1], 2, 2))
            elif draw_person.test_result == 's':
                pg.draw.circle(screen, '#F17163', person_center, person_size // 2)
                # pg.draw.rect(screen, (255, 0, 0), pg.Rect(person.move_target[0], person.move_target[1], 2, 2))
            elif draw_person.test_result == 'i':
                pg.draw.circle(screen, '#8C8C8C', person_center, person_size // 2)
                # pg.draw.rect(screen, (255, 0, 0), pg.Rect(person.move_target[0], person.move_target[1], 2, 2))


def draw_quads(screen, draw_quad: Quad) -> None:
    if draw_quad.split:
        draw_quads(screen, draw_quad.top_left_quad)
        draw_quads(screen, draw_quad.top_right_quad)
        draw_quads(screen, draw_quad.bottom_left_quad)
        draw_quads(screen, draw_quad.bottom_right_quad)
    else:
        starting_x = draw_quad.top_left[0]
        starting_y = draw_quad.top_left[1]
        quad_width = draw_quad.bottom_right[0] - starting_x
        quad_height = starting_y - draw_quad.bottom_right[1]
        pg.draw.rect(screen, (130, 130, 130), pg.Rect(starting_x, starting_y - quad_height, quad_width, quad_height), 1)


def draw_graph(screen, display_graph: list[list[int]], people_number: int,
               starting_x: int, starting_y: int, width: int, height: int) -> None:
    # define colors
    healthy_color = '#29a3a3'
    sick_color = '#F17163'
    immune_color = '#8C8C8C'

    # draw healthy graph
    pg.draw.rect(screen, healthy_color, pg.Rect(starting_x, starting_y, width, height))

    if len(display_graph) >= 3:
        # define variables based on number of data points
        section_length = width / len(display_graph)
        height_scalar = height / people_number

        # define lists
        sick_poly = []
        immune_poly = []

        for section_number, section in enumerate(display_graph):
            sick_number = section[0]
            immune_number = section[1]

            # add data points
            immune_poly.append((starting_x + section_number*section_length,
                                starting_y + (height - (immune_number + sick_number)*height_scalar)))
            sick_poly.append((starting_x + section_number*section_length,
                              starting_y + (height - sick_number*height_scalar)))

        # add points to create correct shape
        sick_poly.append((starting_x + width, sick_poly[-1][1]))
        immune_poly.append((starting_x + width, immune_poly[-1][1]))
        sick_poly.append((starting_x + width, starting_y + height))
        immune_poly.append((starting_x + width, starting_y + height))

        # draw both graphs
        pg.draw.polygon(screen, immune_color, immune_poly)
        pg.draw.polygon(screen, sick_color, sick_poly)

        # draw outline
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(starting_x, starting_y, width, height), 2)


def update_graph(graph_to_update: list[list[int]], person_list: list[Person]) -> list[list[int]]:
    # define variables
    sick_number = 0
    immune_number = 0
    updated_graph = graph_to_update.copy()

    # count number of sick and immune people
    for graph_person in person_list:
        if graph_person.test_result == 's':
            sick_number += 1
        elif graph_person.test_result == 'i':
            immune_number += 1

    # update and return graph
    updated_graph.append([sick_number, immune_number])
    return updated_graph


def check_all_collisions(check_collision_nodes: list[Node], test_for: str) -> None:
    if test_for == 's':
        for check_node in check_collision_nodes:
            # only test sick people
            if check_node.content.test_result == 's':
                collision_list = check_node.find_collisions()
                for collision_node in collision_list:
                    collision_node.content.collision()
    else:
        for check_node in check_collision_nodes:
            # only test healthy people
            if check_node.content.test_result == 'h':
                collision_list = check_node.find_collisions()
                for collision_node in collision_list:
                    if collision_node.content.test_result == 's':
                        check_node.content.collision()
                        break


def get_highest_test_result(test_nodes: list[Node]) -> str:
    healthy_count = 0
    sick_count = 0

    for test_node in test_nodes:
        test_result = test_node.content.test_result
        if test_result == 'h':
            healthy_count += 1
        elif test_result == 's':
            sick_count += 1

        if sick_count < healthy_count:
            return 's'
        else:
            return 'h'


def update_node_positions(update_node_list: list[Node], size: int) -> list[Node]:
    for update_node in update_node_list:
        update_node.quads = []
        tl = [update_node.content.x_position, update_node.content.y_position]
        br = [tl[0] + size, tl[1] - size]
        update_node.corners = [tl, br]

    return update_node_list


def update_quad(node_update_list: list[Node], node_size: int) -> Quad:
    main_update_quad = Quad((700, 700), (1400, 100), node_size)
    for update_node in node_update_list:
        main_update_quad.place_node(update_node)

    return main_update_quad


if __name__ == '__main__':
    # create all simulation variables
    POPULATION_COUNT = 1000
    INFECTION_RADIUS = 15
    HEALTHY_START_PERCENT = 0.99
    SICK_START_PERCENT = 0.01
    INFECTION_CHANCE = 0.01
    IMMUNE_CHANCE = 0.001
    PERSON_DISPLAY_SIZE = 5
    SHOW_QUADS = False
    GROUP_COUNT = 1

    GROUP_CORDS = {1: [[(700, 750), (1400, 50)]],
                   2: [[(700, 750), (1400, 425)], [(700, 475), (1400, 50)]],
                   3: [[(700, 750), (1025, 425)], [(1050, 750), (1400, 435)], [(875, 475), (1225, 50)]],
                   4: [[(700, 750), (1025, 425)], [(1050, 750), (1400, 435)], [(700, 475), (1025, 50)], [(1050, 475), (1400, 50)]]
                   }

    # initialize Pygame
    pg.init()

    # set up display
    WIDTH, HEIGHT = 1500, 800
    main_display = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Pandemic Simulation')

    # create variables
    FPS = 60
    clock = pg.time.Clock()
    running = True
    group_list = []
    graph = [[0, 0]]

    # testing code
    quad_cords = GROUP_CORDS[GROUP_COUNT]
    population_per_group = POPULATION_COUNT // GROUP_COUNT

    for group_number in range(0, GROUP_COUNT):
        group = []
        for _ in range(population_per_group):
            group.append(Person((quad_cords[group_number][0][0], quad_cords[group_number][1][0]), (quad_cords[group_number][1][1], quad_cords[group_number][0][1]), HEALTHY_START_PERCENT,
                                SICK_START_PERCENT, INFECTION_CHANCE, IMMUNE_CHANCE))
        group_list.append(group)

    # group1 = []
    # for _ in range(POPULATION_COUNT):
    #     group1.append(
    #             Person((700, 1400), (100, 700), HEALTHY_START_PERCENT, SICK_START_PERCENT,
    #                    INFECTION_CHANCE, IMMUNE_CHANCE))
    # group_list.append(group1)

    # create node_lists
    node_list = []
    for person in group_list[0]:
        node = Node([[person.x_position, person.y_position],
                     [person.x_position + INFECTION_RADIUS, person.y_position - INFECTION_RADIUS]], person)
        node_list.append(node)

    while running:
        # handle events
        for event in pg.event.get():
            # close game
            if event.type == pg.QUIT:
                running = False

        # move people
        for group in group_list:
            for person in group:
                person.move()
                person.tick()

        # update nodes to reflect people moving
        node_list = update_node_positions(node_list.copy(), INFECTION_RADIUS)

        # update quad with new node positions
        main_quad = update_quad(node_list, INFECTION_RADIUS)

        # handle collisions
        tr = get_highest_test_result(node_list)
        check_all_collisions(node_list, tr)

        # create graph
        w = len(graph)
        graph = update_graph(graph, group_list[0])

        # display content
        draw_screen(main_display, group_list, PERSON_DISPLAY_SIZE, INFECTION_RADIUS)
        if SHOW_QUADS:
            draw_quads(main_display, main_quad)
        draw_graph(main_display, graph, len(group_list[0]), 100, 150, 500, 500)
        pg.display.flip()

        # control the frame rate
        clock.tick(FPS)

    # quit Pygame
    pg.quit()
    sys.exit()
