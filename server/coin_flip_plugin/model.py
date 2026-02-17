from .domain import CoinFlipPlayer

class DB:
    player = CoinFlipPlayer()

    def __init__(self):
        DB.player.balance = 1000

    def get_player(self, id):
        return DB.player