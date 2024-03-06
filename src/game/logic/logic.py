import random
from ..util import position_equals, clamp
from typing import List

class Move: # kelas untuk membuat objek baru di luar kelas Logic
        def __init__(self):
            self.future_move_x = 0
            self.future_move_y = 0
            self.initiating = False

        def initialize(self, board): # inisiasi teleport dan reset button
            for i in range(len(board.game_objects)):
                if board.game_objects[i].type == "TeleportGameObject":
                    self.teleport2 = i
                elif board.game_objects[i].type == "DiamondButtonGameObject":
                    self.restart_button = i
            self.teleport1 = self.teleport2 - 1
            print(self.teleport1, self.teleport2, self.restart_button, "\n\n")

class Logic(object):
    def __init__(self): # inisiasi objek
        self.max_distance_base = 0
        self.goal_position = None
        self.max_distance_bot = 0
        self.move = Move()
    
    def get_direction(self, current_x, current_y, dest_x, dest_y, teleport1_x, teleport1_y, teleport2_x, teleport2_y, base): # fungsi untuk mencari arah gerak bot
        delta_x = clamp(dest_x - current_x, -1, 1)
        delta_y = clamp(dest_y - current_y, -1, 1)
        self.move.future_move_x = 0
        self.move.future_move_y = 0

        # algoritma untuk menghindar dari teleport
        if delta_x != 0 and delta_y != 0: # jika delta_x dan delta_y tidak sama dengan 0
            if (current_x + delta_x, current_y) not in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:  # jika posisi bot tidak sama dengan posisi teleport
                delta_y = 0
            else: # jika posisi bot sama dengan posisi teleport
                delta_x = 0
        elif delta_x != 0 and delta_y == 0:
            if (current_x + delta_x, current_y) in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
                self.move.future_move_x = delta_x
                delta_x = 0
                if current_y == 14: # jika posisi bot di ujung bawah
                    delta_y = 1
                else:
                    delta_y = 1
        elif delta_x == 0 and delta_y != 0:
            if (current_x, current_y + delta_y) in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
                self.move.future_move_y = delta_y
                delta_y = 0
                if current_x == 14: # jika posisi bot di ujung kanan
                    delta_x = -1
                else:
                    delta_x = 1

        return delta_x, delta_y

    # fungsi untuk mencari posisi diamond yang paling dekat dengan bot dan base
    # mencari diamond di sekeliling diamond yang ditemukan 
    def recursive_search(self, diamonds, x, y, base, bot_position, visited):
        if x > 14 or y > 14 or x < 0 or y < 0: # jika posisi diamond di luar papan
            return 0, visited
        if (x, y) in visited: # jika posisi diamond sudah dikunjungi
            return 0, visited

        visited.add((x, y)) # menambahkan posisi diamond ke dalam set visited
        points = 0
        ada = False

        for diamond in diamonds: # mencari diamond yang posisinya sama dengan x dan y
            if (diamond.position.x == x and diamond.position.y == y):
                ada = True
                points += diamond.properties.points
                self.max_distance_base = max(self.max_distance_base, abs(
                    base.x - x) + abs(base.y - y))
                self.max_distance_bot = max(self.max_distance_bot, abs(
                    bot_position.x - x) + abs(bot_position.y - y))
                break
        
        # mencari diamond di sekeliling diamond yang ditemukan
        if ada: # jika diamond ditemukan
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
        if self.move.initiating == False: # jika move belum diinisiasi
            self.move.initialize(board)

        if self.move.future_move_x != 0 or self.move.future_move_y != 0: # jika future_move_x atau future_move_y tidak sama dengan 0
            delta_x = self.move.future_move_x
            delta_y = self.move.future_move_y
            self.move.future_move_x = 0
            self.move.future_move_y = 0
            return delta_x, delta_y
        else: # jika future_move_x dan future_move_y sama dengan 0
            teleport1 = board.game_objects[self.move.teleport1]
            teleport2 = board.game_objects[self.move.teleport2]
            restart_button = board.game_objects[self.move.restart_button]
            visited = set()
            props = board_bot.properties
            current_position = board_bot.position
            base = props.base

            if props.diamonds == 5: # jika diamond yang ditemukan sudah 5
                self.goal_position = base
            else: # jika diamond yang ditemukan belum 5
                diamonds = board.diamonds
                worth = 0
                calculated_diamonds = []
                for diamond in diamonds: # mencari diamond yang paling dekat dengan bot dan base
                    if props.diamonds == 4 and diamond.properties.points == 2: # jika diamond yang ditemukan sudah 4 dan point diamond yang ditemukan adalah 2
                        continue
                    if diamond.position in calculated_diamonds: # jika diamond sudah dihitung
                        continue
                    elif (current_position.x, current_position.y, teleport1.position.x, teleport2.position.y) in [(0, 0, 1, 1), (0, 14, 1, 13), (14, 0, 13, 1), (14, 14, 13, 13)]: # jika posisi bot di salah satu sudut papan dan terdapat teleport di sekitar bot
                        continue
                    point, visited = self.recursive_search(
                        diamonds, diamond.position.x, diamond.position.y, base, current_position, visited)
                    calculated_diamonds.append(diamond.position) 
                    jarak = self.max_distance_base + self.max_distance_bot
                    if jarak != 0:
                        jarak_reset = abs(restart_button.position.x - current_position.x) + abs(restart_button.position.y - current_position.y) + abs(restart_button.position.x - base.x) + abs(restart_button.position.y - base.y)

                        value = point / jarak
                        worth = max(worth, value)

                        if worth == value: # jika worth sama dengan value
                            self.goal_position = diamond.position
                            if props.milliseconds_left < 20000 and jarak > props.milliseconds_left / 1000: # jika waktu yang tersisa kurang dari 20 detik dan jarak lebih besar dari waktu yang tersisa dibagi 1000
                                self.goal_position = base
                            elif jarak_reset != 0: # jika jarak_reset tidak sama dengan 0
                                worth_restart = 0.75 / jarak_reset
                                if worth < worth_restart and restart_button.position != current_position: # jika worth kurang dari worth_restart dan posisi restart_button tidak sama dengan posisi bot
                                    print("worth restart")
                                    self.goal_position = restart_button.position
                    self.max_distance_base = 0
                    self.max_distance_bot = 0
            delta_x, delta_y = self.get_direction( # mencari arah gerak bot
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
                teleport1.position.x,
                teleport1.position.y,
                teleport2.position.x,
                teleport2.position.y,
                base,
            )

            return delta_x, delta_y
