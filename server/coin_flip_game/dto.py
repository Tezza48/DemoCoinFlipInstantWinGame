
from dataclasses import dataclass
from typing import Literal
from .domain import CoinFlipGame, CoinFlipPlayer


@dataclass
class PlayerDTO:
    balance: int


@dataclass
class GameDTO:
    totalWager: int
    totalPayout: int
    result: Literal["heads", "tails"]


@dataclass
class SettingsDTO:
    winPayout: float
    minWager: int
    maxWager: int


@dataclass
class RefreshResponse:
    player: PlayerDTO
    settings: SettingsDTO
    game: GameDTO


@dataclass
class FlipResponse:
    player: PlayerDTO
    game: GameDTO


def build_player(player: CoinFlipPlayer):
    return PlayerDTO(player.balance)

def build_game(player: CoinFlipPlayer):
    return GameDTO(player.total_wager, player.total_payout, player.result)

def build_settings(game: CoinFlipGame):
    return SettingsDTO(game.win_payout, game.min_wager, game.max_wager)

def build_flip(player: CoinFlipPlayer):
    return FlipResponse(
        build_player(player), build_game(player)
    )

def build_refresh(game: CoinFlipGame, player: CoinFlipPlayer):
    return RefreshResponse(
        build_player(player),
        build_settings(game),
        build_game(player),
    )