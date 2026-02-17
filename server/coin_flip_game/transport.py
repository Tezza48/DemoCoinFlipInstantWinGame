from framework.framework import BaseHandler
from .domain import CoinFlipGame, CoinFlipPlayer
from .dto import build_refresh, build_flip


class RefreshHandler(BaseHandler):
    def __init__(self, game: CoinFlipGame):
        self.game = game

    def handle(self, request: dict, player: CoinFlipPlayer):
        match request:
            case {}:
                pass
            case _:
                raise Exception()

        return build_refresh(self.game, player)


class FlipHandler(BaseHandler):
    def __init__(self, game: CoinFlipGame):
        self.game = game

    def handle(self, request: dict, player: CoinFlipPlayer):
        match request:
            case {"wager": wager} if isinstance(wager, int):
                pass
            case _:
                raise Exception()

        wager = self.game.validate_wager_size(player, wager)
        player.total_wager = wager

        self.game.flip(player)

        return build_flip(player)