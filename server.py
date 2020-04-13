import socket
import threading

PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send_board(state,pconn):
    string_state = ' '.join(map(str,state)) #converts list to string for sending
    pconn.send(string_state.encode('utf-8'))


def check(input_list):
    
    if (input_list[1] == input_list[2] == input_list[3]):
        return True
    elif (input_list[4] == input_list[5] == input_list[6]):
        return True
    elif (input_list[7] == input_list[8] == input_list[9]):
        return True
    elif (input_list[1] == input_list[4] == input_list[7]):
        return True
    elif (input_list[2] == input_list[5] == input_list[8]):
        return True
    elif (input_list[3] == input_list[6] == input_list[9]):
        return True
    elif (input_list[1] == input_list[5] == input_list[9]):
        return True
    elif (input_list[3] == input_list[5] == input_list[7]):
        return True
    else:
        return False


def close_game(pconn1, pconn2):
    pconn1.recv(64).decode('utf-8')
    pconn1.close()
    pconn2.recv(64).decode('utf-8')
    pconn2.close()


def play_game(conn1, addr1, conn2, addr2):
    
    PLAYER_1 = (conn1, 'O')
    PLAYER_2 = (conn2, 'X')
    board_state = ['-1','1','2','3','4','5','6','7','8','9']
    TURN_LIST = [PLAYER_1, PLAYER_2, PLAYER_1, PLAYER_2 ,PLAYER_1, PLAYER_2, PLAYER_1, PLAYER_2, PLAYER_1]

    for i in TURN_LIST:
        send_board(board_state, i[0])
        player_move = i[0].recv(64).decode('utf-8')
        board_state[int(player_move)] = i[1]
        if(check(board_state)):
            board_state[0] = '1'
            send_board(board_state,i[0])
            board_state[0] = '0'
            if (i[0] is PLAYER_1[0]):
                send_board(board_state, PLAYER_2[0])
                close_game(PLAYER_1[0],PLAYER_2[0])
                
            else:
                send_board(board_state, PLAYER_1[0])
                close_game(PLAYER_1[0],PLAYER_2[0])
    
    board_state[0] = '3'
    send_board(board_state,PLAYER_1[0])
    send_board(board_state,PLAYER_2[0])
    close_game(PLAYER_1[0],PLAYER_2[0])



def start_server():
    
    print('[SERVER] server starting...')
    player_num = 0
    conn1, addr1, conn2, addr2 = None, None, None, None
    server.listen()
    print(f'server is listening on {SERVER}')

    while True:
        if(conn1 == None and addr1 == None):
            conn1, addr1 = server.accept()
        else:
            conn2, addr2 = server.accept()
            thread = threading.Thread(target=play_game, args = (conn1, addr1, conn2, addr2))
            thread.start()
            conn1, addr1, conn2, addr2 = None, None, None, None
    
    
start_server()
            

        




