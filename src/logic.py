import random
from ..util import get_direction, position_equals
from typing import List

class RandomDiamondLogic(object):
    def __init__(self):
        self.max_distance_base = 0
        self.goal_position = None
        self.max_distance_bot = 0

    def recursive_search(self, diamonds, x, y, base, bot_position, visited):
        if x > 14 or y > 14 or x < 0 or y < 0 or (x, y) in visited:
            return 0, visited

        visited.append((x, y))
        points = 0
        ada = False
        for diamond in diamonds:
            if (diamond.position.x == x and diamond.position.y == y):
                ada = True
                points += diamond.properties.points
                self.max_distance_base = max(self.max_distance_base, abs(
                    base.x - x) + abs(base.y - y))
                self.max_distance_bot = max(self.max_distance_bot, abs(
                    bot_position.x - x) + abs(bot_position.y - y))
                break

        if ada:
            if (x + 1, y) not in visited and x + 1 < 15:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x - 1, y) not in visited and x - 1 >= 0:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x, y + 1) not in visited and y + 1 < 15:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x, y - 1) not in visited and y - 1 >= 0: 
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x - 1, y - 1) not in visited and x - 1 >= 0 and y - 1 >= 0:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x + 1, y - 1) not in visited and x + 1 < 15 and y - 1 >= 0:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x - 1, y + 1) not in visited and x - 1 >= 0 and y + 1 < 15:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]
            if (x + 1, y + 1) not in visited and x + 1 < 15 and y + 1 < 15:
                points += self.recursive_search(
                    diamonds, x, y, base, bot_position, visited)[0]

        return points, visited

    def next_move(self, board_bot, board):
        teleport1 = board.game_objects[0]
        teleport2 = board.game_objects[1]
        restart_button = board.game_objects[2]

        visited = []
        props = board_bot.properties
        current_position = board_bot.position
        base = props.base
        if props.diamonds == 5:
            self.goal_position = base
        else:
            diamonds = board.diamonds
            worth = 0
            for diamond in diamonds:
                if props.diamonds == 4 and diamond.properties.points == 2:
                    continue
                point, visited = self.recursive_search(
                    diamonds, diamond.position.x, diamond.position.y, base, current_position, visited)
                jarak = self.max_distance_base + self.max_distance_bot
                if jarak != 0:
                    jarak_reset = abs(restart_button.position.x - current_position.x) + abs(restart_button.position.y - current_position.y) + abs(restart_button.position.x - base.x) + abs(restart_button.position.y - base.y)

                    worth = max(worth, point / jarak)
                    worth_restart = 0.5 / jarak_reset

                    if worth == point / jarak:
                        self.goal_position = diamond.position
                        if props.milliseconds_left < 20000 and jarak > props.milliseconds_left / 1000:
                            self.goal_position = base
                        elif worth < worth_restart:
                            print("worth restart")
                            self.goal_position = restart_button.position
                self.max_distance_base = 0
                self.max_distance_bot = 0
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        return delta_x, delta_y
