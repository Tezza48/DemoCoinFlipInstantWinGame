import datetime
from enum import Enum
import sys
import time

from coin_flip_plugin import CoinFlipPlugin, CoinFlipPlayer
from coin_flip_plugin.dto import FlipResponse

class Stats:
    def __init__(self):
        self.total_plays = 0
        self.total_wager = 0
        self.total_payout = 0

def print_stats(stats: Stats, round: int):
    print(
        "Round {} | total_plays: {}, total_wager: {}, total_payout: {}, RTP: {}%".format(
            round, stats.total_plays,
            stats.total_wager,
            stats.total_payout,
            ((stats.total_payout / stats.total_wager) * 100) if stats.total_payout != 0 else 0
        )
    )

def test(spins: int):
    stats = Stats()
    plugin = CoinFlipPlugin()

    seconds = time.time()

    for i in range(spins):
        player = CoinFlipPlayer()
        player.balance = 1000
        wager = 20
        response: FlipResponse = plugin.handle_request("/flip", {"wager": wager}, player)
        stats.total_plays += 1
        stats.total_payout += response.game.totalPayout
        stats.total_wager += wager

        if (i == 0) or (i == spins - 1) or (time.time() > seconds):
            seconds = time.time() + 1
            print_stats(stats, i)

if __name__ == "__main__":
    spins = int(sys.argv[1])
    if not isinstance(spins, int):
        raise Exception("First argument 'spins' must be an integer: {}".format(spins))
    test(spins)