import pytest
from unittest.mock import patch, MagicMock
import person as p


class TestPerson:
    def test_set_move_target(self):
        pass

    @patch('person.Person.set_move_target')
    def test_move_main_at_move_target(self, mock_set_move_target):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (50, 50)

        test_person.move()
        assert mock_set_move_target.called_once()

    @patch('person.Person.set_move_target')
    def test_move_main_close_to_move_target_top_right(self, mock_set_move_target):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (52, 52)

        test_person.move()
        assert mock_set_move_target.called_once()

    @patch('person.Person.set_move_target')
    def test_move_main_close_to_move_target_top_left(self, mock_set_move_target):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (48, 52)

        test_person.move()
        assert mock_set_move_target.called_once()

    @patch('person.Person.set_move_target')
    def test_move_main_close_to_move_target_bottom_right(self, mock_set_move_target):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (52, 48)

        test_person.move()
        assert mock_set_move_target.called_once()

    @patch('person.Person.set_move_target')
    def test_move_main_close_to_move_target_bottom_left(self, mock_set_move_target):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (48, 48)

        test_person.move()
        assert mock_set_move_target.called_once()

    @patch('person.Person.set_move_target')
    def test_move_main_new_move_target_not_needed(self, mock_set_move_target):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (80, 80)

        test_person.move()
        assert mock_set_move_target.not_called()

    def test_move_right(self):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (80, 80)

        test_person.move()
        assert test_person.x_position == 52

    def test_move_left(self):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 50
        test_person.y_position = 50
        test_person.move_target = (20, 80)

        test_person.move()
        assert test_person.x_position == 48

    def test_move_up(self):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 51
        test_person.y_position = 50
        test_person.move_target = (80, 80)

        test_person.move()
        assert test_person.y_position == 52

    def test_move_down(self):
        test_person = p.Person((0, 100), (0, 100), 0.99, 0.01, 0.01, 0.001)
        test_person.speed = 2
        test_person.x_position = 51
        test_person.y_position = 50
        test_person.move_target = (80, 20)

        test_person.move()
        assert test_person.y_position == 48


