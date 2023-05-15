from interaction import *
import player1
import player2

print("Initializing game...")
game1 = Game_play(player2, player1)
game2 = Game_play(player1, player2)

print("Game running...")
game1.start_game()
game2.start_game()

print("Saving replay...")
game1.save_log('replay1.json')
game2.save_log('replay2.json')
print("Done")
print(game1.log_data)
print(game2.log_data)
