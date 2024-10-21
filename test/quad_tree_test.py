import pytest
from unittest.mock import patch, MagicMock
import quad_tree as qt


class TestNode:
    def test_node_update_quads_add_first_quad(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_node.update_quads(test_quad)
        assert test_node.quads == [test_quad]

    def test_node_update_quads_add_sub_quads(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        test_parent_quad = qt.Quad((0, 100), (100, 0), 5)
        test_parent_quad.split_quad()

        test_tl_sub_quad = test_parent_quad.top_left_quad
        test_tr_sub_quad = test_parent_quad.top_right_quad
        test_bl_sub_quad = test_parent_quad.bottom_left_quad
        test_br_sub_quad = test_parent_quad.bottom_right_quad

        test_node.update_quads(test_parent_quad)
        test_node.update_quads(test_tl_sub_quad)
        test_node.update_quads(test_tr_sub_quad)
        test_node.update_quads(test_bl_sub_quad)
        test_node.update_quads(test_br_sub_quad)

        assert test_node.quads == [test_tl_sub_quad, test_tr_sub_quad, test_bl_sub_quad, test_br_sub_quad]

    def test_node_test_collision_tl(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        collision_node = qt.Node([[0, 10], [5, 5]], 'content')
        assert test_node.test_collision(collision_node)

    def test_node_test_collision_tr(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        collision_node = qt.Node([[10, 15], [15, 10]], 'content')
        assert test_node.test_collision(collision_node)

    def test_node_test_collision_bl(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        collision_node = qt.Node([[0, 5], [5, 0]], 'content')
        assert test_node.test_collision(collision_node)

    def test_node_test_collision_br(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        collision_node = qt.Node([[10, 5], [15, 0]], 'content')
        assert test_node.test_collision(collision_node)

    def test_node_test_collision_same(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        collision_node = qt.Node([[5, 10], [10, 5]], 'content')
        assert test_node.test_collision(collision_node)

    @pytest.mark.skip
    def test_node_find_collisions(self):
        test_node = qt.Node([[5, 10], [10, 5]], 'content')


class TestQuad:
    @patch('quad_tree.Node.update_quads')
    def test_quad_place_node_one_node(self, mock_update_quads):
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        test_quad.place_node(test_node)

        assert test_quad.nodes == [test_node]
        mock_update_quads.assert_called_once()

    @patch('quad_tree.Node.update_quads')
    @patch('quad_tree.Quad.split_quad')
    def test_quad_place_node_split_quad(self, mock_split_quad, mock_update_quads):
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_nodes = [qt.Node([[5, 10], [10, 5]], 'content'),
                      qt.Node([[10, 15], [15, 10]], 'content'),
                      qt.Node([[25, 20], [20, 15]], 'content'),
                      qt.Node([[20, 25], [25, 20]], 'content'),
                      qt.Node([[25, 30], [30, 25]], 'content'),
                      qt.Node([[30, 35], [25, 30]], 'content')]
        for test_node in test_nodes:
            test_quad.place_node(test_node)

        assert test_quad.nodes == test_nodes
        mock_split_quad.assert_called_once()
        assert mock_update_quads.call_count == 6

    @patch('quad_tree.Quad.place_node_in_sub_quad')
    def test_quad_place_node_quad_already_split(self, mock_place_node_in_sub_quad):
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_quad.split = True
        test_node = qt.Node([[5, 10], [10, 5]], 'content')
        test_quad.place_node(test_node)

        assert test_quad.nodes == [test_node]
        mock_place_node_in_sub_quad.assert_called_once()

    @patch('quad_tree.Quad.split_quad')
    def test_quad_place_node_quad_too_small(self, mock_split_quad):
        test_quad = qt.Quad((0, 9), (9, 0), 5)
        test_nodes = [qt.Node([[4, 9], [4, 9]], 'content'),
                      qt.Node([[4, 9], [4, 9]], 'content'),
                      qt.Node([[4, 9], [4, 9]], 'content'),
                      qt.Node([[4, 9], [4, 9]], 'content'),
                      qt.Node([[4, 9], [4, 9]], 'content'),
                      qt.Node([[4, 9], [4, 9]], 'content')]
        for test_node in test_nodes:
            test_quad.place_node(test_node)

        assert test_quad.nodes == test_nodes
        mock_split_quad.assert_not_called()

    def test_quad_split_quad_check_sub_quads(self):
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_quad.nodes = [qt.Node([[5, 10], [10, 5]], 'content'),
                           qt.Node([[10, 15], [15, 10]], 'content'),
                           qt.Node([[25, 20], [20, 15]], 'content'),
                           qt.Node([[20, 25], [25, 20]], 'content'),
                           qt.Node([[25, 30], [30, 25]], 'content'),
                           qt.Node([[30, 35], [25, 30]], 'content')]
        test_quad.split_quad()

        assert test_quad.top_left_quad.top_left == (0, 100)
        assert test_quad.top_left_quad.bottom_right == (50, 50)
        assert test_quad.top_right_quad.top_left == (50, 100)
        assert test_quad.top_right_quad.bottom_right == (100, 50)
        assert test_quad.bottom_left_quad.top_left == (0, 50)
        assert test_quad.bottom_left_quad.bottom_right == (50, 0)
        assert test_quad.bottom_right_quad.top_left == (50, 50)
        assert test_quad.bottom_right_quad.bottom_right == (100, 0)

    @patch('quad_tree.Quad.place_node_in_sub_quad')
    def test_quad_split_quad_check_nodes_placed_in_sub_quad(self, mock_place_node_in_sub_quad):
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_quad.nodes = [qt.Node([[5, 10], [10, 5]], 'content'),
                           qt.Node([[10, 15], [15, 10]], 'content'),
                           qt.Node([[25, 20], [20, 15]], 'content'),
                           qt.Node([[20, 25], [25, 20]], 'content'),
                           qt.Node([[25, 30], [30, 25]], 'content'),
                           qt.Node([[30, 35], [25, 30]], 'content')]
        test_quad.split_quad()

        assert mock_place_node_in_sub_quad.call_count == 6

    def test_quad_place_node_in_sub_quad(self):
        test_quad = qt.Quad((0, 100), (100, 0), 5)
        test_quad.split_quad()
        test_node = qt.Node([[5, 10], [10, 5]], 'content')