from interaction import *
import player1
import player2
import time

print("Initializing game...")
seed=int(time.time()*1000)%1000
game1 = Game_play(player1, player2,order=0,seed=seed)
game2 = Game_play(player2, player1,order=1,seed=seed)

print("Game running...")
game1.start_game()
game2.start_game()

print("Saving replay...")
game1.save_log('replay1.json')
game2.save_log('replay2.json')
print("Done")
