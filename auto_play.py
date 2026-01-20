from subprocess import Popen, PIPE
from threading  import Thread
from queue import Queue
import atexit
from pathlib import Path
from time import time, sleep
import random
import numpy as np
import pandas as pd
import sys
random.seed(int(1000000000*(time()%1))) # truly random start - need this to run parallel games

games = 10000 # nombre de jeux

write_logs = True # write the two game log files

agent_process1 = None
agent_process2 = None
t1 = None
q1 = None
t2 = None
q2 = None

def cleanup_process1():
    global agent_process1
    if agent_process1 is not None:
        agent_process1.kill()

def cleanup_process2():
    global agent_process2
    if agent_process2 is not None:
        agent_process2.kill()

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


# nouvelle evaluation
command_1_list = ["./engine_1/build/Release/Roxane", "-h", "20", "-t", "1", "-mode", "IOStd"]
# --- 1. Isoler le chemin de l'exécutable ---
# L'exécutable est toujours le premier élément de la liste (index 0)
engine_1_name = command_1_list[0]

# Utiliser Pathlib pour gérer les chemins de manière sûre et moderne
engine_1_path = Path(engine_1_name)

# --- 2. Définir le répertoire de travail courant (CWD) comme le dossier de l'exécutable
# C'est l'endroit où les chemins relatifs de l'exécutable C++ fonctionneront.
build_1_directory = (engine_1_path.parent.resolve()).parent.resolve()

# --- 3. Remplacer le chemin relatif par le chemin absolu dans la commande
# (Ceci est une bonne pratique pour éviter toute ambiguïté)
command_1_list[0] = str(engine_1_path.resolve())


# evaluation de reference :
command_2_list = ["./engine_2/build/Release/Roxane", "-h", "20", "-t", "1", "-mode", "IOStd"]
engine_2_name = command_2_list[0]
engine_2_path = Path(engine_2_name)
build_2_directory = (engine_2_path.parent.resolve()).parent.resolve()
command_2_list[0] = str(engine_2_path.resolve())





# make move function *****************************************************

# parametres :
# move : index coup [0, 63]
# b : l'othellier tableau numpy b[x, y]
# player : int (-1, 1) player (black/white]

# retour
# b1 : nouveau othellier
# legit : int (0, 1) legal == 1

def make_move(move, b, player):
    b1 = b.copy()
    legit = 0
    if move > 63:
        return b, legit
    x = move % 8
    y = move // 8
    x0, y0 = x, y
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            x, y = x0, y0
            x += dx
            y += dy
            if x >= 0 and x < 8 and y >= 0 and y < 8 and b1[y, x] == -player:
                x += dx
                y += dy
                if not (x >= 0 and x < 8 and y >= 0 and y < 8):
                    continue
                while b1[y, x] == -player:
                    x += dx
                    y += dy
                    if not (x >= 0 and x < 8 and y >= 0 and y < 8):
                        break
                if not (x >= 0 and x < 8 and y >= 0 and y < 8):
                    continue
                if b1[y, x] == player:
                    #print('legit!', x + 8 * y)
                    legit = 1
                    while True:
                        x -= dx
                        y -= dy
                        b1[y, x] = player # change
                        if x == x0 and y == y0:
                            break
    return b1, legit

# get moves function *****************************************************
# return un tableau numpy contenant tous les coups legaux pour le player
def get_moves(b, player):
    moves = []
    for x in range(8):
        for y in range(8):
            if b[y,x] == 0:
                b0 = b.copy() # save
                _, legit = make_move(y * 8 + x, b0, player)
                if legit:
                    moves.append(y * 8 + x)
    return moves


# create random starting board
def starting_board(n): # get random starting board with n pieces on it
    while True: # loop until it comes out right
        b = np.zeros([8,8], dtype=np.int32)
        b[3,3] = b[4,4] = 1
        b[3,4] = b[4,3] = -1
        player = -1
        # loop over random moves
        for i in range(n-4):
            # get all moves
            moves = get_moves(b, player) # what if there are no moves?
            if len(moves) == 0: # pass
                # skip this one and try again
                break
            # select one
            move = random.choice(moves)
            # make it
            b, legit = make_move(move, b, player)
            player = -player
            moves = get_moves(b, player) # what if there are no moves?
            if len(moves) == 0: # pass; skip this one and try again
                b = np.zeros([8,8], dtype=np.int32)
                break
        if np.abs(b).sum() == n:
            return b, player

# retourne une representation ffo_test de l'othellier
def get_fen(b, player):
    f = []
    for i in range(64):
        if b.ravel()[i] == 0:
            f.append('-')
        elif b.ravel()[i] == 1:
            f.append('O')
        else:
            f.append('*')
    f.append(' ')
    if player == 1:
        f.append('O')
    else:
        f.append('*')
    f = ''.join(f)
    return f

#fonction inverse
def board_from_fen(f, b):
    b = b.ravel()
    if f[-1] == 'O':
        player = 1
    else:
        player = -1
    for i in range(64):
        if f[i] == '-':
            b[i] = 0
        elif f[i] == 'O':
            b[i] = 1
        else:
            b[i] = -1
    b = b.reshape(8,8)
    return b, player

def calc_score(scores):
    s = np.minimum(.99, np.maximum(.01, (scores[0] + scores[1] / 2) / max(.1, scores.sum()))) # score
    e = -400 * np.log10(1 / s - 1) # ELO
    s2 = scores / max(.1, scores.sum())
    es = np.sqrt((s2[0] + s2[2] - (s2[0] - s2[2])**2) / max(.1, scores.sum())) # std of score
    es *= 174 / s / (1 - s) # std of ELO
    return np.round(e, 0).astype(np.int32), np.round(es, 0).astype(np.int32)


# start the engines
# 1
agent_process1 = Popen(command_1_list, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=build_1_directory.as_posix()) # 1
atexit.register(cleanup_process1) # 1

q1 = Queue() # modif
t1 = Thread(target=enqueue_output, args=(agent_process1.stderr, q1)) # 1
t1.daemon = True # 1
t1.start() # 1

# 2
agent_process2 = Popen(command_2_list, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=build_2_directory.as_posix()) # 2
atexit.register(cleanup_process2) # 2

q2 = Queue() # modif
t2 = Thread(target=enqueue_output, args=(agent_process2.stderr, q2)) # 2
t2.daemon = True # 2
t2.start() # 2

sleep(1) # wait N seconds - for engines to initialize


# loop over game sets
scores = np.array([0,0,0]) # w/d/l for player engine_1 (new)

rr = [] # result list of game pairs
#tt = [] # list of time left

time_start = time()

for game in range(games): # at 50 sec, 20 game pairs in 1 hour
    
    if game % 100 == 0:
        e, es = calc_score(scores)
        print('results for new evaluation after : ', game, ' games ', scores, ' ELO ', e, ' +/- ', es)
        
    start_b, start_player = starting_board(14)
    
    fen_start = get_fen(start_b, start_player)
    start_player_after_variation = start_player
    
    moves_list = [[], []]
    
    # play two games, with board flipped after the first one
    symm_scores = np.array([0,0]) # 2 games. Scores are always for engine 1
    
    for symm_game in [0, 1]:
        
        b = start_b.copy()
        player = start_player
        
        # --- SWAP DES AGENTS ---
        if symm_game == 0:
            # Match Aller : Engine 1 est Black (-1), Engine 2 est white (1)
            black_ag = agent_process1
            white_ag = agent_process2
            variation_swap = True
        else:
            # Match Retour : Engine 1 est white (1), Engine 2 est black (-1)
            black_ag = agent_process2
            white_ag = agent_process1
            variation_swap = False
        
        # init the engines clear hastables
        c = "IOStd init\n"
        agent_process1.stdin.write(c.encode())
        agent_process1.stdin.flush()
        
        agent_process2.stdin.write(c.encode())
        agent_process2.stdin.flush()
        
        
        # time - N sec per game ******************************************************
        # time1 = 50000 # 50 -> 20 game pairs in 1 hour
        # time2 = 50000
                    
                
        # loop over moves
        i = 0
        while True:
            # check if pass
            moves = get_moves(b, player)
            if len(moves) == 0:
                # pass
                if symm_game == 1 and not variation_swap:
                    # verification que le coup est different
                    if moves_list[0][i] != "PA":
                        variation_swap = True
                        fen_start = get_fen(b, player)
                        start_player_after_variation = player
                                        
                if write_logs and variation_swap:
                    moves_list[symm_game].append("PA")
                                
                player = -player
                moves = get_moves(b, player)
                if len(moves) == 0:
                    # end of game
                    s_black = (b==-1).sum()
                    s_white = (b== 1).sum()
                    s_empty = 64-(s_black+s_white)
                    
                     # On calcule le score relatif à l'Engine 1
                    if symm_game == 0: # Engine 1 était Black
                        r = s_black - s_white
                    else: # Engine 1 était white
                        r = s_white - s_black
                        
                    if r < 0:
                        r -= s_empty
                    elif r > 0:
                        r += s_empty
 
                                       
                    if write_logs and variation_swap:
                        r_2 = r
                        if symm_game == 1 and start_player == start_player_after_variation:
                            r_2 *= -1

                        with open('game_log_detailed.txt', 'a') as f:
                            f.write(f"{r_2:3d} ")
                            f.write(fen_start)
                            f.write(" ")
                            f.write("".join(moves_list[symm_game][:-1]))
                            f.write("\n")
                                                
                    # update score of symm set. Always from POV of engine 1 (new)
                    symm_scores[symm_game] = r
                    if symm_game == 1:
                        r = symm_scores.sum() 
                        rr.append(r/2) # type GGS
                        if r == 0: # draw
                            scores[1] += 1
                        elif r > 0: # win
                            scores[0] += 1
                        else: # loss
                            scores[2] += 1
                    break
                    
            #get fen
            fen = get_fen(b, player)
            t1 = time()
                        
            # start the calc **********************************************
            # --- SELECTION DE L'AGENT ---
            ag = white_ag if player == 1 else black_ag
                            
            #switch midgame-endgame
            depth = 9 # endgame at 14 empty
            n_empty = fen.count('-')
            if n_empty < 15:
                depth = n_empty
                            
            c = f'IOStd search {fen} {depth} 100\n'
            ag.stdin.write(c.encode())
            ag.stdin.flush()
                            
            # get responce
            while True:
                response = (ag.stdout.readline()).decode()
                            
                # Vérification préventive pour éviter l'IndexError si le processus se termine
                if not response:
                    print("ERREUR FATALE: Le moteur a terminé la communication de manière inattendue.")
                    break
                            
                # Tokenisation unique
                tokens = response.split()
                            
                # Vérification pour l'affichage (utilise 'tokens' pour la sécurité)
                if len(tokens) > 0 and tokens[0] == 'move':
                    if symm_game == 1 and not variation_swap:
                        # verification que le coup est different
                        if moves_list[0][i] != tokens[1]:
                            variation_swap = True
                            fen_start = get_fen(b, player)
                            start_player_after_variation = player
                                            
                    if write_logs and variation_swap:
                        moves_list[symm_game].append(tokens[1])
                                    
                    # Condition de sortie (utilise 'tokens' pour la sécurité)
                    if len(tokens) >= 2 and (tokens[0] == "bestmove" or tokens[0] == "move"):
                        break
                            
            # Si vous atteignez ce point sans 'break', la boucle continue de lire la ligne suivante.
                    
            # ... Suite du code après le break
            coord = tokens[1]
                    
            # process the responce
                    
            di = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
            move = di[coord[0].upper()] + 8 * (int(coord[1]) - 1)
                            
            '''
            # adjust time
            t2 = time()
            if player == 1:
                time1 = int(time1 + 1000 * (t1 - t2))
            else:
                time2 = int(time2 + 1000 * (t1 - t2))
            '''
                    
            # make the move
            b, legit = make_move(move, b, player)
            if legit == 0:
                print('illegal move!')
                sys.exit() # Arrête proprement le programme
            player = -player

            i+= 1

print('finished', games, 'games. Time elapsed', int(time()-time_start), 'sec.', int(.5 + games * 3600 / (time()-time_start)), 'games per hour')
e, es = calc_score(scores)
print('results for  new evaluation: ', scores, ' ELO ', e, ' +/- ', es)
print(pd.Series(rr).value_counts().sort_index())
