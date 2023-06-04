from interaction import *
import time
import numpy as np
import sys
import importlib

n1 = sys.argv[1]
n2 = sys.argv[2]
total_games = int(sys.argv[3])
if total_games % 2 != 0:
    raise RuntimeError('Total rounds must be even')
names = [n1, n2]
p1 = importlib.import_module(n1)
p2 = importlib.import_module(n2)

def print_stats(game, game_n, order):
    log = game.log_data
    if order == -1:
        log['winner'] = 1 - log['winner']
    print("-------------Game {}-------------".format(game_n))
    print('{0:12s}: {1}'.format('winner', names[log['winner']]))
    print('{0:12s}: {1}'.format('reason', log['reason']))
    print('{0:12s}: {1}'.format('turn number', log['length']))
    print('{0:12s}: {1} - {2}'.format('score', *game.score[::order]))
    print('{0:12s}: {1}'.format('time', log['time'][::order]))
#    print('{0:12s}: {1}'.format('tags', log['tag']))

gamescore = [0, 0]
total_score = np.array([0, 0])
time_consumed = np.array([0, 0], dtype=float)
game_n = 0
path = ''
while game_n < total_games:
    seed = int(time.time() * 1000) % 1000007
    game_n += 1
    game = Game_play(p1, p2, seed=seed)
    game.start_game()
    print_stats(game, game_n, order=1)
    winner = game.replay['winner']
    gamescore[winner] += 1
    total_score += np.array(game.score)
    time_consumed += game.replay['time']
    print('total score : {0} - {1}'.format(*total_score))
    # save replay?
    game.save_log('{0}-VS-{1}_Game{2}.json'.format(*names, game_n))
    ## repeat this
    game_n += 1
    game = Game_play(p2, p1, seed=seed)
    game.start_game()
    print_stats(game, game_n, order=-1)
    winner = 1 - game.replay['winner']
    gamescore[winner] += 1
    total_score += np.array(game.score[::-1])
    time_consumed += game.replay['time'][::-1]
    print('total score : {0} - {1}'.format(*total_score))
    game.save_log('{0}-VS-{1}_Game{2}.json'.format(*names, game_n))

## decide the winner
if gamescore[0] > gamescore[1]:
    winner = 0
if gamescore[1] > gamescore[0]:
    winner = 1
if gamescore[0] == gamescore[1]:
    if relative[0] > relative[1]:
        winner = 0
    if relative[1] > relative[0]:
        winner = 1
    if relative[0] == relative[1]:
        winner = np.argmin(time_consumed)

print("==========************==========")
print('              {0:5d} - {1}'.format(*gamescore))
print('total score : {0:5d} - {1}'.format(*total_score))
print('total time  : {0:.3f} - {1:.3f}'.format(*time_consumed))
print('Winner      : {}'.format(names[winner]))
