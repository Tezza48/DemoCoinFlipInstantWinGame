
from random import randrange
from typing import Final, Literal

def weighted_bag(weights, values):
    total_weight = sum(weights)
    target = randrange(total_weight)
    for w, v in zip(weights, values):
        if target < w:
            return v
        target -= w

    raise Exception("Random weight {0} out of range {1}", target, total_weight)

class CoinFlipPlayer:
    def __init__(self):
        self.balance = 0
        self.total_wager = 0
        self.total_payout = 0
        self.result: Literal["heads", "tails"] = "heads"


class CoinFlipGame:
    def __init__(self):
        """
        Docstring for __init__

        :param self: Description
        """
        self.win_payout: Final[float] = 1.95
        self.min_wager: Final[int] = 20
        self.max_wager: Final[int] = 2000

    def validate_wager_size(self, player: CoinFlipPlayer, wager: int):
        """
        Validates the player's requested wager size

        Raises an exception if not valid

        :param self: Description
        :param player: Description
        :type player: Player
        :param wager: Description
        :type wager: int
        """
        if wager < self.min_wager:
            raise Exception("Wager {} must be > min_wager {}", wager, self.min_wager)
        if wager > self.max_wager:
            raise Exception("Wager {} must be < max_wager {}", wager, self.max_wager)
        if wager % self.min_wager:
            raise Exception(
                "Wager {} must be a multiple of min_wager {}", wager, self.min_wager
            )
        if player.balance < wager:
            raise Exception("Not enough balance to play game with wager")

        return wager

    def flip(self, player: CoinFlipPlayer):
        player.balance -= player.total_wager

        player.result = weighted_bag([1, 1], ["heads", "tails"])

        player.total_payout = 0

        if player.result == "heads":
            player.total_payout = player.total_wager * self.win_payout

        player.balance += player.total_payout