import socket
from os import system, name
import sys

PORT = 8080
SERVER = '192.168.1.10'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def board(inputlist):
    clear()
    print(f'     |     |     ')
    print(f'  {inputlist[1]}  |  {inputlist[2]}  |  {inputlist[3]}     ')
    print(f'_____|_____|_____')
    print(f'     |     |     ')
    print(f'  {inputlist[4]}  |  {inputlist[5]}  |  {inputlist[6]}     ')
    print(f'_____|_____|_____')
    print(f'     |     |     ')
    print(f'  {inputlist[7]}  |  {inputlist[8]}  |  {inputlist[9]}     ')
    print(f'     |     |     ')
    print('')


def check_moves(input_list, move):
    if any([move == '1',move == '2', move == '3', move == '4', move == '5', move == '6', move == '7', move == '8', move == '9']):
        if(input_list[int(move)] == 'O' or input_list[int(move)] == 'X' ):
            return False
        else:
            return True
    else:
        return False


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def send_move(move):
    client.send(move.encode('utf-8'))


def start():
    board_state = []

    while True:
        string_state = client.recv(64).decode('utf-8')
        board_state = list(string_state.split(' '))
        if(board_state[0] == '0'):
            board(board_state)
            print('You Lose')
            send_move(' ')
            input()
            sys.exit()
        elif(board_state[0] == '1'):
            board(board_state)
            print('You Win')
            send_move(' ')
            input()
            sys.exit()
        elif(board_state[0] == '3'):
            board(board_state)
            print('Tie')
            send_move(' ')
            input()
            sys.exit()
        else:
            board(board_state)
            move = input('Please enter your move: ')
            while(not(check_moves(board_state, move))):
                board(board_state)
                move = input('Wrong move! Please enter again: ')
            send_move(move)


start()



