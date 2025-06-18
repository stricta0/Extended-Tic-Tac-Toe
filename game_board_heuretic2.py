class HistoryElement:
    """
    This class is used for saving history of moves
    """
    def __init__(self):
        self.direction = None
        self.prev_val = None
        self.is_accessable_for_me = None
        self.is_accessable_for_enemy = None
        self.best_line_for_me = None
        self.best_line_for_enemy = None


class BoardElement:
    """
    This class is a single board element, one square on the game board
    """
    def __init__(self, pos):
        self.pos = pos
        self.is_taken = False
        self.is_taken_by_me = False



        self.is_accessable_for_me = True
        self.is_accessable_for_enemy = True
        self.points = 0
        self.line_high_score_for_me = 0
        self.line_high_score_for_enemy = 0


        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.up_right = 0
        self.up_left = 0
        self.down_right = 0
        self.down_left = 0

        self.direction_map = {
            (1, 1): 'down_right',
            (1, 0): 'down',
            (1, -1): 'down_left',
            (0, 1): 'right',
            (0, -1): 'left',
            (-1, 1): 'up_right',
            (-1, 0): 'up',
            (-1, -1): 'up_left'
        }

        self.line_direction_map = {
            (1, 1): 'up_left_line',
            (1, 0): 'up_down_line',
            (1, -1): 'up_right_line',
            (0, 1): 'left_right_line',
            (0, -1): 'left_right_line',
            (-1, 1): 'up_right_line',
            (-1, 0): 'up_down_line',
            (-1, -1): 'up_left_line'
        }


        self.up_down_line = 0
        self.left_right_line = 0
        self.up_right_line = 0
        self.up_left_line = 0

        self.history = []





    def get_best_sums_of_opposite_directions(self, direction_horizontally, direction_vertically):
        """
            take direction, lets take up, we take one up and one in opposite (down) and
            a = in direction
            b = in opposite direciotn
            sum = a + b
            we find best for me and best for enemy so max(a, b, sum) and min(a, b, sum)
        :param direction_horizontally: 1 up, -1 down, 0 in place
        :param direction_vertically: 1 right, -1 left, 0 in place
        :return: max(a, b, sum), min(a, b, sum)
        """
        direction = self.direction_map[(direction_horizontally, direction_vertically)]
        opposite_direction = self.direction_map[(-direction_horizontally, -direction_vertically)]
        if not direction or not opposite_direction:
            raise RuntimeError("Invalid directions in get_best_sums_of_opposite_directions")

        a = getattr(self, direction)
        b = getattr(self, opposite_direction)
        total = a + b

        best = a
        if b > best:
            best = b
        if total > best:
            best = total

        worst = a
        if b < worst:
            worst = b
        if total < worst:
            worst = total

        return best, worst


    def evaluate_point_on_line(self, line):
        # print(f"evaluating point: {self.pos} on line: {line}")
        """
        takes line and calculate new points score, also checks for 3rd symbol in witch case we change
        accessibility of BoardElement
        :param line: tuple with 2 arguments with direction horizontal and direction vertical

        Function sets all the local variables to its new values, line scores, accessibility and tringles
        """
        self.is_accessable_for_me = True
        self.is_accessable_for_enemy = True
        if self.is_taken:
            self.is_accessable_for_me = False
            self.is_accessable_for_enemy = False
            self.points = 0
            return

        points_sum = self.points

        points = self.get_best_sums_of_opposite_directions(line[0], line[1])


        is_dead_direction_for_me = 0 #we can have a dead line
        if points[0] == 2: #its a tringle, now question is -> can i use this tringle in the future or is it just dead
            if self.line_high_score_for_me != 3:
                self.is_accessable_for_me = False
            is_dead_direction_for_me = 1
            in_direction = self.get_in_direction(line[0], line[1])
            in_opposite_direction = self.get_in_opposite_direction(line[0], line[1])
            if in_direction == 0:
                #in_oposite_direction = 2
                i = self.pos // 10
                j = self.pos % 10
                if 4 >= i + line[0] >= 0 and 4 >= j + line[1] >= 0: #if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_me = 0
            if in_opposite_direction == 0:
                #in_direction = 2
                i = self.pos // 10
                j = self.pos % 10
                if 4 >= i - line[0] >= 0 and 4 >= j - line[1] >= 0:  # if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_me = 0
            if in_direction == 1:
                i = self.pos // 10
                j = self.pos % 10
                if 4 >= i - line[0] >= 0 and 4 >= j - line[1] >= 0:  # if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_me = 0
                if 4 >= i + line[0] >= 0 and 4 >= j + line[1] >= 0: #if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_me = 0

        is_dead_direction_for_enemy = 0
        if points[1] == -2:  # its a tringle, now question is -> can i use this tringle in the future or is it just dead
            if self.line_high_score_for_enemy != -3:
                self.is_accessable_for_enemy = False
            is_dead_direction_for_enemy = 1
            in_direction = self.get_in_direction(line[0], line[1])
            in_opposite_direction = self.get_in_opposite_direction(line[0], line[1])
            if in_direction == 0:
                # in_oposite_direction = -2
                i = self.pos // 10
                j = self.pos % 10
                if 4 >= i + line[0] >= 0 and 4 >= j + line[1] >= 0:  # if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_enemy = 0
            if in_opposite_direction == 0:
                # in_direction = -2
                i = self.pos // 10
                j = self.pos % 10
                if 4 >= i - line[0] >= 0 and 4 >= j - line[1] >= 0:  # if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_enemy = 0
            if in_direction == -1:
                i = self.pos // 10
                j = self.pos % 10
                if 4 >= i - line[0] >= 0 and 4 >= j - line[1] >= 0:  # if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_enemy = 0
                if 4 >= i + line[0] >= 0 and 4 >= j + line[1] >= 0: #if there is something up, and its score is 0 -> we still can in the future use this
                    is_dead_direction_for_enemy = 0

        #TODO its a high score, it wont go down in undo!
        if points[0] > self.line_high_score_for_me:
            self.line_high_score_for_me = points[0]
        if points[1] < self.line_high_score_for_enemy:
            self.line_high_score_for_enemy = points[1]

        line_value = 0
        if points[0] > 0:
            val = points[0] * points[0] * (1 - is_dead_direction_for_me)
            line_value += val
        if points[1] < 0:
            val = -(points[1] * points[1]) * (1 - is_dead_direction_for_enemy)
            line_value += val

        old_points = getattr(self, self.line_direction_map[line])  # take old points from this line
        setattr(self, self.line_direction_map[line], line_value) #save new points to this line

        points_sum = points_sum - old_points + line_value #take prev value of points, subtruckt ammount of poinst in prev line, and add new value -> update value of points
        self.points = points_sum



    def set_in_direction(self, direction_horizontally, direction_vertically, value):
        """
        This point has variables that keep amount of lined up players symbols on each line see: BoardElement.__init__
        This function is designed to set value in a particular direction

        :param direction_horizontally: +1 up, 0 stay, -1 down
        :param direction_vertically: +1 right, 0 stay, -1 left
        :param value: value to assign to the line in said direction
        """
        direction = self.direction_map[(direction_horizontally, direction_vertically)]
        if direction:
            prev_val = getattr(self, direction)
            history_el = HistoryElement()
            history_el.best_line_for_me = self.line_high_score_for_me
            history_el.best_line_for_enemy = self.line_high_score_for_enemy
            history_el.direction = (direction_horizontally, direction_vertically)
            history_el.prev_val = prev_val
            history_el.is_accessable_for_me = self.is_accessable_for_me
            history_el.is_accessable_for_enemy = self.is_accessable_for_enemy
            self.history.append(history_el) #get value from string variable name
            setattr(self, direction, value)  # we set value
        #UPDATE VALUATION ON THIS DIRECTION
        self.evaluate_point_on_line((direction_horizontally, direction_vertically))

    def set_in_opposite_direction(self, direction_horizontally, direction_vertically, value):
        self.set_in_direction(-direction_horizontally, -direction_vertically, value)

    def undo_set(self):
        """
        Undo set operation, we just reverse every operation done in set
        """
        if self.history:
            history_el = self.history.pop()

            direction_points = history_el.direction
            direction_name = self.direction_map[(direction_points[0], direction_points[1])]
            old_value = history_el.prev_val
            setattr(self, direction_name, old_value)
            self.line_high_score_for_me = history_el.best_line_for_me
            self.line_high_score_for_enemy = history_el.best_line_for_enemy
            self.evaluate_point_on_line(direction_points)

            self.is_accessable_for_me = history_el.is_accessable_for_me
            self.is_accessable_for_enemy = history_el.is_accessable_for_enemy

    def get_in_direction(self, direction_horizontally, direction_vertically):
        """
        :param direction_horizontally: +1 up, 0 stay, -1 down
        :param direction_vertically: +1 right, 0 stay, -1 left
        :return: amount of connected player symbols in given direction, or -amount of enemy symbols
        """
        direction = self.direction_map[(direction_horizontally, direction_vertically)] #get variable name as string
        if direction:
            return getattr(self, direction)  # get value from string variable name

    def get_in_opposite_direction(self, direction_horizontally, direction_vertically):
        return self.get_in_direction(-direction_horizontally, -direction_vertically)


    def get_bord_element_info_as_string(self, length):
        """
        :param length -> minilam length of returned string
        :return BordeElement points, accessibility for me and for the enemy and advances it with
        symbols "|" and then "-", if only one symbol remains we add space at the end,
        This is designed to represent points and accessibility in the same length string every time
        """
        res = f"({self.points} {1 if self.is_accessable_for_me else 0} {1 if self.is_accessable_for_enemy else 0})"
        while len(res) + 4 <= length:
            res = "-" + res + "-"
        if len(res) + 2 <= length:
            res = "|" + res + "|"
        while len(res) < length:
            res = res + " "
        return res

class CombsBord:
    def __init__(self):
        self.Board = [[BoardElement(i + j * 10) for i in range(5)] for j in range(5)]
        self.changes_in_move = []
        self.directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        self.directions.remove((0,0))
        self.move_history = []
        self.board_hash = bytearray(b"_" * 25)

        self.player_won = False
        self.enemy_won = False

    def set_board(self, board, my_id, enemy_id):
        self.Board = [[BoardElement(i + j * 10) for i in range(5)] for j in range(5)]
        self.changes_in_move = []
        self.board_hash = bytearray(b"_" * 25)
        self.move_history = []
        self.player_won = False
        self.enemy_won = False
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == my_id:
                    self.place_one(i*10+j, True)
                elif board[i][j]== enemy_id:
                    self.place_one(i*10+j, False)


    def propagate_in_direction(self, pos, direction_horizontally, direction_vertically, is_my_move, moves=3):
        """
        This is a helper function used when symbol was placed on pos, this function is used to update one line, in given direction

        :param pos: position of starting element
        :param direction_horizontally: +1 up, 0 stay, -1 down
        :param direction_vertically: +1 right, 0 stay, -1 left
        :param is_my_move: True if its player move, False otherwise
        :param moves: max amount to moves in given direction

        Function assigns appropriate values to every element in board game
        starting from pos we make moves amount of moves in given direction, for example we start from 0
        and go 3 squares right, and we adjust squares that were effected by player (or enemy) move
        """
        i = pos // 10
        j = pos % 10

        prev_val = self.Board[i][j].get_in_opposite_direction(direction_horizontally, direction_vertically)#if im going up, how many elements are down from me
        if is_my_move and prev_val < 0:
            prev_val = 0
        if not is_my_move and prev_val > 0:
            prev_val = 0
        i = i + direction_horizontally
        j = j + direction_vertically
        to_add = 1
        if not is_my_move:
            to_add = -1
        while i != -1 and i != 5 and j != -1 and j != 5 and moves != 0:
            if self.Board[i][j].is_taken and self.Board[i][j].is_taken_by_me != is_my_move:
                self.Board[i][j].set_in_opposite_direction(direction_horizontally, direction_vertically, to_add)
                break
            self.Board[i][j].set_in_opposite_direction(direction_horizontally, direction_vertically, prev_val + to_add)
            is_taken_by_moving_player = self.Board[i][j].is_taken_by_me == is_my_move and self.Board[i][j].is_taken
            if not is_taken_by_moving_player:
                break

            i += direction_horizontally
            j += direction_vertically
            moves -= 1
            prev_val += to_add

    def undo_propagate_in_direction(self, pos, direction_horizontally, direction_vertically, is_my_move, moves=3):
        """
        Undo propagate in direction, we just reverse every operation done by propagate in direction
        """
        i = pos // 10
        j = pos % 10

        # in direction
        i = i + direction_horizontally
        j = j + direction_vertically
        while i != -1 and i != 5 and j != -1 and j != 5 and moves != 0:
            self.Board[i][j].undo_set()
            if self.Board[i][j].is_taken and self.Board[i][j].is_taken_by_me != is_my_move:
                break
            is_taken_by_moving_player = self.Board[i][j].is_taken_by_me == is_my_move and self.Board[i][j].is_taken
            if not is_taken_by_moving_player:
                break
            i += direction_horizontally
            j += direction_vertically
            moves -= 1



    def undo_propagate_in_all_directions(self, pos, is_my_move):
        """
        Undo propagate in all direction
        """
        for direction in self.directions:
            self.undo_propagate_in_direction(pos, direction[0], direction[1], is_my_move)

    def propagate_in_all_directions(self, pos, is_my_move):
        """
        This is helper function for place_one, when we place one this function is responsible for updating
        every effected square
        :param pos: position on game bord where symbol was placed
        :param is_my_move: True if its my move False otherwise
        """
        for direction in self.directions:
            self.propagate_in_direction(pos, direction[0], direction[1], is_my_move)


    def check_if_won_los(self, pos, mine_move):
        if mine_move:
            best_line_val = self.Board[pos//10][pos%10].line_high_score_for_me
            if best_line_val == 2:
                self.enemy_won = True
                # print(pos, mine_move, "first", best_line_val)
                return True
            if best_line_val == 3:
                # print(pos, mine_move, "second")
                self.player_won = True
                return True
        else:
            best_line_val = self.Board[pos // 10][pos % 10].line_high_score_for_enemy
            if best_line_val == -2:
                # print(pos, mine_move, "third")
                self.player_won = True
                return True
            if best_line_val == -3:
                # print(pos, mine_move, "forth")
                self.enemy_won = True
                return True




    def place_one(self, pos, mine_move=True):
        """
        Function makes single move in the game (mine or enemy)
        :param pos: position of symbol on the gameboard
        :param mine_move: is this move done by player, True if it is and False otherwise
        """


        i = pos // 10
        j = pos % 10
        index = i * 5 + j
        self.board_hash[index] = ord("X") if mine_move else ord("O")
        was_accessable_for_me = self.Board[i][j].is_accessable_for_me
        was_accessable_for_enemy = self.Board[i][j].is_accessable_for_enemy

        self.Board[i][j].is_taken = True
        self.Board[i][j].is_taken_by_me = mine_move
        self.Board[i][j].is_accessable_for_me = False
        self.Board[i][j].is_accessable_for_enemy = False

        prev_points = self.Board[i][j].points
        self.Board[i][j].points = 0
        # print(f"place one, pos:{pos}, high score save {self.Board[i][j].line_high_score_for_me, self.Board[i][j].line_high_score_for_enemy}")
        self.move_history.append((pos, mine_move, was_accessable_for_me, was_accessable_for_enemy, prev_points, self.Board[i][j].line_high_score_for_me, self.Board[i][j].line_high_score_for_enemy))
        self.propagate_in_all_directions(pos, mine_move)
        if self.check_if_won_los(pos, mine_move):
            return True
        return False


    def undo_place_one(self):
        """
        Undo previous move, raises Error if there is no move to be undone
        """
        if not self.move_history:
            raise RuntimeError("Tried to reverse move but move_history is empty")

        self.player_won = False
        self.enemy_won = False

        pos, mine_move, was_accessable_for_me, was_accessable_for_enemy, prev_points, me_line_hs, enemy_line_hs = self.move_history.pop()
        i = pos // 10
        j = pos % 10
        self.Board[i][j].line_high_score_for_me, self.Board[i][j].line_high_score_for_enemy = me_line_hs, enemy_line_hs
        index = i * 5 + j
        self.board_hash[index] = ord('_')

        self.Board[i][j].is_taken = False
        self.Board[i][j].is_taken_by_me = False
        self.Board[i][j].is_accessable_for_me = was_accessable_for_me
        self.Board[i][j].is_accessable_for_enemy = was_accessable_for_enemy
        self.Board[i][j].points = prev_points
        self.undo_propagate_in_all_directions(pos, mine_move)


    #TODO: this could be done on the side, but its only 25 operations
    def get_whole_board_sore(self):
        """
        :return: returns heuristic value of this board, by adding points from all board elements
        single board element can be a part of 4 lines 
        for eatch line we take best scenario for a player and enemy (see: get_best_sums_of_opposite_directions)
        then any line gives 2, we give it 2 points if we can make 4th in the future (for exampl xx-__, point - gets points) and 0 if it cant be used (-xx=_ point - dosnt get any points (cant be usefull, point = gets 4 point))
        then we square points of eatch line, if its enemy line we also multiply by -1
        sum of all those line points is heuretic value
        """
        value = 0
        for i in range(5):
            for j in range(5):
                value += self.Board[i][j].points
        return value

    #TODO: this also can bo done much better
    def get_points_in_order(self, is_me):
        some_point = None
        if not self.move_history:
            return [22, 11, 13, 31, 33, 12, 21, 23, 32, 0, 1, 2, 3, 4, 10, 20, 30, 40, 41, 42, 43, 44, 34, 24, 14]
        else:
            res = []
            for i in range(5):
                for j in range(5):
                    pos = i * 10 + j
                    if self.Board[i][j].is_taken:
                        continue #not walid point
                    if is_me:
                        if not self.Board[i][j].is_accessable_for_me:
                            if not res and some_point is None: #there is no need to concidre multiple points like that, and there is no need to 
                                some_point = (-999999999, pos)
                                #res.append((-999999999, pos)) #point valid, but only if we have absolotly no other optnion (i will louse)
                            continue
                    else:
                        if not self.Board[i][j].is_accessable_for_enemy:
                            if not res and some_point is None:
                                some_point = (-999999999, pos)
                                #res.append((999999999, pos))
                            continue
                    res.append((abs(self.Board[i][j].points), pos))
            if not res and some_point is not None:
                res.append(some_point)
            res.sort(reverse=is_me)
            return [pos for (_, pos) in res]

    def print_val_helper(self, element):
        """
        :param element: numeric value:
        :return adds space before number if the number is positive:
        """
        return " " + str(element) if element>= 0 else str(element)

    def print_all_data(self):
        """
        Prints whole gameboard in 5 X 5 grid, every square look like this;
        |-(0 0 0)-|
        |  0  0  0 |
        |  0  O  0 |
        |  0  0  0 |
        |----------|
        Where value in the middle is player symbol
        Values around middle element represent how many of player (+1) or enemy (-1) symbols are in this lane
        3 Values at the top mean respectively: overall amount of points, accessibility for player, accessibility for enemy
        :return:
        """
        for i in range(5):
            print(f"{self.Board[i][0].get_bord_element_info_as_string(12)}    {self.Board[i][1].get_bord_element_info_as_string(12)}    {self.Board[i][2].get_bord_element_info_as_string(12)}    {self.Board[i][3].get_bord_element_info_as_string(12)}    {self.Board[i][4].get_bord_element_info_as_string(12)}")
            for line_no in range(3):
                for j in range(5):
                    current_element = self.Board[i][j]
                    symbol = "_" if not current_element.is_taken else "X" if current_element.is_taken_by_me else "O"

                    if line_no == 0:
                        print(f"| {self.print_val_helper(current_element.up_left)} {self.print_val_helper(current_element.up)} {self.print_val_helper(current_element.up_right)} |", end="    ")
                    elif line_no == 1:
                        print(f"| {self.print_val_helper(current_element.left)}  {symbol} {self.print_val_helper(current_element.right)} |", end="    ")
                    else:
                        print(f"| {self.print_val_helper(current_element.down_left)} {self.print_val_helper(current_element.down)} {self.print_val_helper(current_element.down_right)} |", end="    ")
                print()
            print("|----------|    |----------|    |----------|    |----------|    |----------|")
        print(f"\nWhole Board Score: {self.get_whole_board_sore()}\n\n")
if __name__ == "__main__":
    game_board = CombsBord()
    # my_id = 1
    # enemy_id = 2
    #                   #  0  1  2  3  4
    # game_board_to_ser = [
    #                     [1, 0, 0, 0, 0],  # 0
    #                     [0, 0, 0, 0, 0],  # 1
    #                     [1, 0, 0, 0, 0],  # 2 #TODO: zakładam że nie moge położyć 3 i oceniam je za 0, a przeiceż 3 mi dużo dają - proawdopodobnie
    #                     [0, 0, 0, 0, 0],  # 3
    #                     [0, 0, 0, 0, 0]   # 4
    #                     ]
    # game_board.set_board(game_board_to_ser, my_id, enemy_id)
    # game_board.print_all_data()
    game_board.place_one(10, True)
    game_board.place_one(20, True)
    game_board.print_all_data()
    # # game_board.undo_place_one()
    # print(game_board.place_one(42, True))
    # # game_board.undo_place_one()
    # # game_board.place_one(42, True)
    # game_board.print_all_data()

