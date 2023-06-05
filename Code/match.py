from interaction import *
import time
import numpy as np
import sys
import os
import importlib

n1 = sys.argv[1]
n2 = sys.argv[2]
total_games = int(sys.argv[3])
if total_games % 2 != 0:
    raise RuntimeError('Total rounds must be even')
names = [n1, n2]
p1 = importlib.import_module(n1)
p2 = importlib.import_module(n2)

cn = {'Reach the maximum turn number': 'CMPL',
        'No eraserable moves': 'KO',
        'Run out of blocks': 'CMPL',
        ' Time limit exceeded.': 'TLE'}

def print_stats(game, game_n, order):
    log = game.log_data
    if order == -1:
        log['winner'] = 1 - log['winner']
    reason = log['reason'].split(':')[-1]
    if reason in cn.keys():
        reason = cn[reason]
    else:
        reason = 'ERROR'
    print('{0:^12s} | '.format(names[log['winner']]), end='')
    print('{0:^12s} | '.format(names[(order+1)//2]), end='')
    print('{0:^6s} | '.format(reason), end='')
    print('{0:^3d} | '.format(log['length']), end='')
    print('{0:>4d} - {1:<4d} | '.format(*game.score[::order]), end='')

gamescore = [0, 0]
total_score = np.array([0, 0])
time_consumed = np.array([0, 0], dtype=float)
game_n = 0
path = './{}_VS_{}/'.format(*names)
os.makedirs(path)

print('{0:^12s} | {4:^12s} | {1:^6s} |{2:5s}| {3:^11s} | total scores  |'.format('winner', 'reason', 'turns', 'scores', "who's first"))
while game_n < total_games:
    seed = int(time.time() * 1000) % 1000007
    game_n += 1
    game = Game_play(p1, p2, seed=seed)
    game.start_game()
    print_stats(game, game_n, order=1)
    winner = game.replay['winner']
    gamescore[winner] += 1
    if game.replay['errorStatus'] == -1:
        total_score += np.array(game.score)
    else:
        total_score[winner] += 500
    time_consumed += game.replay['time']
    print('{0:>5d} - {1:<5d} | '.format(*total_score), end='')
    print('{0}:{1}'.format(*gamescore))
    # save replay?
    game.save_log(path + '{0}_VS_{1}_Game{2}.json'.format(*names, game_n))
    ## repeat this
    game_n += 1
    game = Game_play(p2, p1, seed=seed)
    game.start_game()
    print_stats(game, game_n, order=-1)
    winner = 1 - game.replay['winner']
    gamescore[winner] += 1
    if game.replay['errorStatus'] == -1:
        total_score += np.array(game.score[::-1])
    else:
        total_score[winner] += 500
    time_consumed += game.replay['time'][::-1]
    print('{0:>5d} - {1:<5d} | '.format(*total_score), end='')
    print('{0}:{1}'.format(*gamescore))
    game.save_log(path + '{0}_VS_{1}_Game{2}.json'.format(*names, game_n))

## decide the winner
if gamescore[0] > gamescore[1]:
    winner = 0
if gamescore[1] > gamescore[0]:
    winner = 1
if gamescore[0] == gamescore[1]:
    if total_score[0] > total_score[1]:
        winner = 0
    if total_score[1] > total_score[0]:
        winner = 1
    if total_score[0] == total_score[1]:
        winner = np.argmin(time_consumed)

print("=============================================")
print('{2:>10s} {0} - {1} {3:<10s}'.format(*gamescore, *names))
print('total score : {0} - {1}'.format(*total_score))
print('total time  : {0:.3f} - {1:.3f}'.format(*time_consumed))
print('Winner      : {}'.format(names[winner]))
