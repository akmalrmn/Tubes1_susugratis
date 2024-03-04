from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class RandomLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def GetPointsbyCoordinate (self, X, Y, Boards):
        for i in range (len(Boards.diamonds)):
            if(Boards.diamonds[i].position.x == X and Boards.diamonds[i].position.y == Y):
                return Boards.diamonds[i].properties.points
        return 0

    def DiamondBersebelahan(self, board_bot, Boards):
        current_positionX = board_bot.position.x
        current_positionY = board_bot.position.y
        Value1 = self.GetPointsbyCoordinate(current_positionX+1,current_positionY,Boards)
        Value2 = self.GetPointsbyCoordinate(current_positionX-1,current_positionY,Boards)
        Value3 = self.GetPointsbyCoordinate(current_positionX,current_positionY+1,Boards)
        Value4 = self.GetPointsbyCoordinate(current_positionX,current_positionY-1,Boards)
        maksimum = max(Value1,Value2,Value3,Value4)
        if maksimum == 0 :
            return False, current_positionX, current_positionY
        else:
            if maksimum == Value1:
                return True, current_positionX+1, current_positionY
            elif maksimum == Value2:
                return True, current_positionX-1, current_positionY
            elif maksimum == Value3:
                return True, current_positionX, current_positionY+1
            elif maksimum == Value4:
                return True, current_positionX, current_positionX-1



    def hitung_diamonds_berdekatan_recursively(self, x, y, Boards, visited):
        koordinat = (x,y)
        # Jika koordinat sudah pernah dikunjungi atau berada di luar kotak, kembalikan 0
        if koordinat in visited or x < 0 or x >= 15 or y < 0 or y >= 15:
            return 0
        
        # Tandai koordinat sebagai sudah dikunjungi
        visited.add(koordinat)
        
        # Jika koordinat ini merupakan diamond
        if self.GetPointsbyCoordinate(x,y,Boards) == 0:
            # Jika diamond berwarna merah, tambahkan 1, jika berwarna biru, tambahkan 2
            return 0
        
        # Jumlah diamonds berdekatan dari koordinat sekitarnya
        return self.GetPointsbyCoordinate(x,y,Boards) + self.hitung_diamonds_berdekatan_recursively(x, y+1, Boards, visited) + self.hitung_diamonds_berdekatan_recursively(x, y - 1, Boards, visited) + self.hitung_diamonds_berdekatan_recursively(x + 1, y, Boards, visited) + self.hitung_diamonds_berdekatan_recursively(x - 1, y, Boards, visited)


    def getNearestDiamonds(self, Board_bot, Boards):
        maksimumpoints = 0
        maksimumindeks = -999
        for i in range (len(Boards.diamonds)):
            visited = set()
            value = self.hitung_diamonds_berdekatan_recursively(Boards.diamonds[i].position.x, Boards.diamonds[i].position.y, Boards, visited)
            distance = abs(Boards.diamonds[i].position.x-Board_bot.position.x) + abs(Boards.diamonds[i].position.y-Board_bot.position.y)
            if value > 0 and distance > 0:
                worth = value/distance
                if worth > maksimumpoints:
                    maksimumpoints = worth
                    maksimumindeks = i
        return maksimumindeks

    def next_move_antara(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        maks_indeks = self.getNearestDiamonds(board_bot, board)
        jarak = abs(board.diamonds[maks_indeks].position.x-board_bot.position.x) + abs(board.diamonds[maks_indeks].position.y-board_bot.position.y)
        if props.diamonds == 5 or (props.diamonds == 4 and board.diamonds[maks_indeks].properties.points == 2) or (props.milliseconds_left < 20000 and jarak > props.milliseconds_left/1000):
            current_position = board_bot.position
            base = board_bot.properties.base
            self.goal_position = base
        elif (len(board.diamonds) <= 7):
            self.goal_position = board.game_objects[2].position    
        else:
            self.goal_position = board.diamonds[maks_indeks].position
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y, self.goal_position
    
    def next_move(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        delta_x, delta_y, goal_position = self.next_move_antara(board_bot, board)
        next_coordinate = (current_position.x + delta_x, current_position.y + delta_y)
        if (next_coordinate == board.game_objects[0].position or next_coordinate == board.game_objects[1].position):
            if delta_x != 0:
                if goal_position.y > current_position.y:
                    delta_x = 0
                    delta_y = 1
                else:
                    delta_x = 0
                    delta_y = -1
            else:
                if goal_position.x > current_position.x:
                    delta_x = 1
                    delta_y = 0
                else:
                    delta_x = -1
                    delta_y = 0
        return delta_x, delta_y