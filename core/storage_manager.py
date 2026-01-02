import pickle
import os


class StorageManager:
    def __init__(self, game):
        self.game = game

    def save_game(self, filename="savegame.pkl"):
        data = {
            'board': self.game.board,
            'players': self.game.players,
            'idx': self.game.current_player_idx,
            'turn': self.game.dice_rolled_this_turn,
            'phase': self.game.game_phase
        }
        try:
            with open(filename, "wb") as f:
                pickle.dump(data, f)
            self.game.set_message("Game Saved!", 2000)
        except Exception as e:
            print(f"Error saving game: {e}")
            self.game.set_message("Error Saving!", 2000)

    def load_game(self, filename="savegame.pkl"):
        if not os.path.exists(filename):
            self.game.set_message("No save file!", 2000)
            return

        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)

            self.game.board = data['board']
            self.game.players = data['players']
            self.game.current_player_idx = data['idx']
            self.game.dice_rolled_this_turn = data['turn']
            self.game.game_phase = data.get('phase', 'MAIN')

            self.game.reinit_controllers()

            self.game.set_message("Game Loaded!", 2000)
        except Exception as e:
            print(f"Error loading game: {e}")
            self.game.set_message("Error Loading!", 2000)