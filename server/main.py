from dataclasses import asdict, dataclass
import json
from http import server
from random import randint, randrange
from typing import Final, Literal


def weighted_bag(weights, values):
    total_weight = sum(weights)
    target = randrange(total_weight)
    for w, v in zip(weights, values):
        if target < w:
            return v
        target -= w

    raise Exception("Random weight {0} out of range {1}", target, total_weight)


# Refresh Request /play/refresh {"id": number, "request": {}}
# Refresh Response {"player": {"balance": number}, "settings": {"winPayout": 1.95, "minWager": 10, "maxWager": 200}, "game": {"totalWager": number, "totalPayout": number, "result":  "heads"|"tails"}}

# Flip Request /play/flip {"id": number, "request": {"wager": number}}
# Flip Response {"game": {"totalWager": number, "totalPayout": number, "result": "heads"|"tails"} }


class Player:
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

    def validate_wager_size(self, player: Player, wager) -> int:
        """
        Validates the player's requested wager size

        Raises an exception if not valid

        :param self: Description
        :param player: Description
        :type player: Player
        :param wager: Description
        :type wager: int
        """
        if not isinstance(wager, int):
            raise Exception("Wager {} must be an integer", wager)

        wager = int(wager)

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

    def flip(self, player: Player):
        player.balance -= player.total_wager

        player.result = weighted_bag([1, 1], ["heads", "tails"])

        player.total_payout = 0

        if player.result == "heads":
            player.total_payout = player.total_wager * self.win_payout

        player.balance += player.total_payout


class DB:
    player = Player()

    def __init__(self):
        DB.player.balance = 1000

    def get_player(self, id):
        return DB.player


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


def build_player(player: Player):
    return PlayerDTO(player.balance)

def build_game(player: Player):
    return GameDTO(player.total_wager, player.total_payout, player.result)

def build_settings(game: CoinFlipGame):
    return SettingsDTO(game.win_payout, game.min_wager, game.max_wager)

def build_flip(player: Player):
    return FlipResponse(
        build_player(player), build_game(player)
    )

def build_refresh(game: CoinFlipGame, player: Player):
    return RefreshResponse(
        build_player(player),
        build_settings(game),
        build_game(player),
    )

class BaseHandler:
    def handle(request: dict, game: CoinFlipGame, player: Player):
        pass

class RefreshHandler(BaseHandler):
    def handle(request: dict, game: CoinFlipGame, player: Player):
        match request:
            case {}:
                pass
            case _:
                raise Exception()

        return build_refresh(game, player)


class FlipHandler:
    def handle(request: dict, game: CoinFlipGame, player: Player):
        match request:
            case {"wager": wager}:
                pass
            case _:
                raise Exception()

        wager = game.validate_wager_size(player, request["wager"])
        player.total_wager = wager

        game.flip(player)

        return build_flip(player)


class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        db: DB = self.server.context["db"]

        base = "/play"
        if not self.path.startswith(base):
            self.send_error(
                500,
                "Incorrect Request",
                "Only requests via the 'play' route are allowed",
            )
            return

        content_length = self.headers.get("Content-Length")
        content = self.rfile.read(int(content_length))
        request_dict = json.loads(content)

        player: Player
        match request_dict:
            case {"id": id, "packet": packet}:
                player = db.get_player(id)
            case _:
                self.send_error(500, "Incorrect Request", "Request packet is malformed")
                return

        verb = self.path[len(base) :]

        handler: BaseHandler

        match verb:
            case "/refresh":
                handler = RefreshHandler
            case "/flip":
                handler = FlipHandler
            case _:
                self.send_error(500, "Unknown verb {0}".format(verb))
                return

        response = handler.handle(packet, CoinFlipGame(), player)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(asdict(response)), "utf-8"))


def main():
    s = server.HTTPServer(("localhost", 3000), HTTPRequestHandler)
    s.context = {"db": DB()}
    s.serve_forever()
    s.server_close()


if __name__ == "__main__":
    main()
