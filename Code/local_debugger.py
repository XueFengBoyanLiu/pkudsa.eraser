from interaction import *
import player1
import player2

game = Game_runner(player1.Plaser(), player2.Plaser())
game.start_games()
game.save_game_log('replay1.json', 'replay2.json')
