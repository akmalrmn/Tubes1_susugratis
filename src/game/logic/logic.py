import random
from ..util import get_direction, position_equals
from typing import List


class RandomDiamondLogic(object):
    def recursive_search(self, board, current_position, visited):
        if current_position in visited:
            return False
        visited.append(current_position)
        if current_position in board.diamonds:
            return True
        if current_position in board.obstacles:
            return False
        if current_position.x < 0 or current_position.x > 15 or current_position.y < 0 or current_position.y > 15:
            return False
        return self.recursive_search(board, (current_position.x + 1, current_position.y), visited) or self.recursive_search(board, (current_position.x - 1, current_position.y), visited) or self.recursive_search(board, (current_position.x, current_position.y + 1), visited) or self.recursive_search(board, (current_position.x, current_position.y - 1), visited)

    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1

    def next_move(self, board_bot, board):
        print(board.game_objects)
        return 0, 0
        # props = board_bot.properties
        # current_position = board_bot.position
        # if props.diamonds == 5 and current_position != props.base:
        #     base = props.base
        #     self.goal_position = base
        # elif self.goal_position is None or position_equals(
        #     current_position, self.goal_position
        # ):
        #     total_diamonds = len(board.diamonds)
        #     worth = 0
        #     for i in range(total_diamonds):
        #         diamond = board.diamonds[i]
        #         point = diamond.properties.points
        #         delta_x = diamond.position.x - current_position.x
        #         delta_y = diamond.position.y - current_position.y
        #         distance = abs(delta_x) + abs(delta_y)
        #         if current_position == props.base:
        #             base_distance = 0
        #             worth = max(worth, point / distance)
        #         else:
        #             base_distance = abs(
        #                 props.base.x - diamond.position.x) + abs(props.base.y - diamond.position.y)
        #             worth = max(worth, point / (distance + base_distance))
        #         if worth == point / (distance + base_distance) and diamond.position not in [(15, 0), (0, 15), (0, 0), (15, 15)]:
        #             if props.diamonds == 4 and point == 2:
        #                 continue
        #             self.goal_position = diamond.position
        # #     base_distance = abs(props.base.x - current_position.x) + \
        # #         abs(props.base.y - current_position.y)
        # #     goal_distance = abs(self.goal_position.x - current_position.x) + \
        # #         abs(self.goal_position.y - current_position.y)
        # #     if goal_distance > base_distance and current_position != props.base:
        # #         self.goal_position = props.base
        # # Calculate move according to goal position
        # delta_x, delta_y = get_direction(
        #     current_position.x,
        #     current_position.y,
        #     self.goal_position.x,
        #     self.goal_position.y,
        # )
        # self.previous_position = (current_position.x, current_position.y)

        # return delta_x, delta_y
