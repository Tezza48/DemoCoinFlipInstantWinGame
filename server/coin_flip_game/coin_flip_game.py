from framework.framework import BasePlugin
from .transport import RefreshHandler, FlipHandler
from .domain import CoinFlipGame

class CoinFlipPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

        self.game = CoinFlipGame()
        self.add_route("/refresh", RefreshHandler(self.game))
        self.add_route("/flip", FlipHandler(self.game))