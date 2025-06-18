import random
from game_board_heuretic2 import CombsBord

class MoveMaker:
    def __init__(self, depth, board: CombsBord):
        self.depth = depth
        self.board = board
        self.ammount_of_checks = 0
        self.ammount_of_cuts = 0
        self.visited = {}

    def set_board(self, board, my_id, enemy_id):
        self.board.set_board(board, my_id, enemy_id)


    def get_best_move(self):
        best_score = -float('inf')
        best_moves = []
        possible_moves = self.board.get_points_in_order(is_me=True)
        print(possible_moves)
        self.board.print_all_data()
        if not possible_moves:
            return None
        for move in possible_moves:
            finished = self.board.place_one(move, mine_move=True)

            if finished:
                score = float('inf') if self.board.player_won else -float('inf')
            else:
                score = self.minimax(self.depth - 1, is_maximizing=False, alpha=-float("inf"), beta=float("inf"))

            self.board.undo_place_one()
            print(move, score)
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves) if best_moves else None

    def minimax(self, depth, is_maximizing, alpha, beta):
        # print(f"MIN MAX ON DEPTH {depth}")
        self.ammount_of_checks += 1
        if self.board.player_won or self.board.enemy_won:
            return float('inf') if self.board.player_won else -float('inf')
            # else:
            #     return -float('inf') if self.board.player_won else float('inf')

        if depth == 0:
            score = self.board.get_whole_board_sore()
            return score #if is_maximizing else -score

        key = (self.board.board_hash.decode('ascii'), is_maximizing)
        if key in self.visited:
            stored_score, stored_depth = self.visited[key]
            if stored_depth >= depth:
                return stored_score

        current_player = is_maximizing

        possible_moves = self.board.get_points_in_order(is_me=current_player)
        if not possible_moves: #if its empty then there is no move to make, so its a draw
            return 0
        if is_maximizing:
            best = -float('inf')
            for move in possible_moves:
                self.board.place_one(move, mine_move=current_player)
                val = self.minimax(depth - 1, False, alpha, beta)

                self.board.undo_place_one()

                best = max(best, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    self.ammount_of_cuts += 1
                    break
        else:
            best = float('inf')
            for move in possible_moves:

                self.board.place_one(move, mine_move=current_player)
                val = self.minimax(depth - 1, True, alpha, beta)

                self.board.undo_place_one()
                best = min(best, val)
                beta = min(beta, val)
                if beta <= alpha:
                    self.ammount_of_cuts += 1
                    break

        self.visited[key] = (best, depth)
        return best


# --------------------------
if __name__ == "__main__":
    board = CombsBord()

    # optionally, initialize with preset board state
    # for example, fill a few fields manually:

    bot = MoveMaker(depth=6, board=board)
    my_id = 1
    enemy_id = 2
                      #  0  1  2  3  4
    game_board_to_ser = [
                        [1, 0, 0, 0, 0],  # 0
                        [1, 0, 0, 0, 0],  # 1
                        [0, 0, 0, 0, 0],  # 2 #TODO: zakładam że nie moge położyć 3 i oceniam je za 0, a przeiceż 3 mi dużo dają - proawdopodobnie
                        [0, 0, 0, 0, 0],  # 3
                        [0, 0, 0, 0, 0]   # 4
                        ]
    bot.set_board(game_board_to_ser, my_id, enemy_id)
    bot.board.print_all_data()
    best_move = bot.get_best_move()
    print(f"Best move: {best_move}")
    print(f"States evaluated: {bot.ammount_of_checks}")
    print(f"Cuts made: {bot.ammount_of_cuts}")
