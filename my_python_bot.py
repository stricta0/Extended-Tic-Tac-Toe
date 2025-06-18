#!/usr/bin/env python3

import socket
import sys
import random
import time
from game_board_heuretic2 import CombsBord
from move_maker_copy import MoveMaker

# Plansza 5x5
board = [[0 for _ in range(5)] for _ in range(5)]
my_board = CombsBord()
bot = MoveMaker(depth=10, board=my_board)


def set_board(my_id, enemy_id):
    my_board.set_board(board, my_id, enemy_id)

def set_move(move, player, my_id):
    i = (move // 10) - 1
    j = (move % 10) - 1
    if i < 0 or i > 4 or j < 0 or j > 4:
        return False
    if board[i][j] != 0:
        return False
    board[i][j] = player
    my_board.place_one(move - 11, player==my_id)
    return True



def get_move():
    return bot.get_best_move() + 11

def main():
    #inital setup
    if len(sys.argv) != 6:
        print("Wrong number of arguments")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    player = int(sys.argv[3])
    nick = sys.argv[4]
    depth = int(sys.argv[5])
    bot.depth = depth

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((ip, port))
    except:
        print("Unable to connect")
        sys.exit(1)

    print("Connected with server successfully")

    # Odbierz "700"
    msg = sock.recv(16).decode()
    print(f"Server message: {msg.strip()}")

    # Send initial info to servew
    ident = f"{player} {nick}"
    sock.sendall(ident.encode())

    end_game = False

    # Run game
    while not end_game:
        msg = sock.recv(16).decode().strip()
        if not msg:
            continue
        print(f"Server message: {msg}")
        try:
            msg_int = int(msg)
        except:
            continue
        print(msg)
        move = msg_int % 100
        code = msg_int // 100

        if move != 0:
            set_move(move, 3 - player, player)

        if code == 0 or code == 6:
            move = get_move() 
            set_move(move, player, player)
            sock.sendall(str(move).encode())
        else:
            end_game = True
            if code == 1:
                print("You won.")
            elif code == 2:
                print("You lost.")
            elif code == 3:
                print("Draw.")
            elif code == 4:
                print("You won. Opponent error.")
            elif code == 5:
                print("You lost. Your error.")

    sock.close()

if __name__ == "__main__":
    main()
