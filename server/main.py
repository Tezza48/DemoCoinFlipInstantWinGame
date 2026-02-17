import json
from dataclasses import asdict
from http import server
from operator import itemgetter

from coin_flip_game.coin_flip_game import CoinFlipPlugin
from coin_flip_game.domain import CoinFlipPlayer
from coin_flip_game.model import DB
from framework.framework import BasePlugin

# Refresh Request /play/refresh {"id": number, "request": {}}
# Refresh Response {"player": {"balance": number}, "settings": {"winPayout": 1.95, "minWager": 10, "maxWager": 200}, "game": {"totalWager": number, "totalPayout": number, "result":  "heads"|"tails"}}

# Flip Request /play/flip {"id": number, "request": {"wager": number}}
# Flip Response {"game": {"totalWager": number, "totalPayout": number, "result": "heads"|"tails"} }


class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """
    Hosts the hard coded game plugin "CoinFlipPlugin", proceses the generic base request info,
    fetches the correct player from the DB (Dummy playar instance) and handles the request
    """

    def do_GET(self):
        db: DB
        plugin: BasePlugin
        db, plugin = itemgetter("db", "plugin")(self.server.context)

        base = "/play"
        if not self.path.startswith(base):
            self.send_error(
                500,
                "Incorrect Request",
                "Only requests via the 'play' route are allowed",
            )
            return

        content_length = self.headers.get("Content-Length")
        if content_length is None:
            self.send_error(500)
            return

        content = self.rfile.read(int(content_length))
        request_dict = json.loads(content)

        player: CoinFlipPlayer
        match request_dict:
            case {"id": id, "packet": packet}:
                player = db.get_player(id)
            case _:
                self.send_error(500, "Incorrect Request", "Request packet is malformed")
                return

        verb = self.path[len(base) :]

        try:
            response = plugin.handle_request(verb, packet, player)
        except Exception:
            self.send_error(500)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(asdict(response)), "utf-8"))


def main():
    s = server.HTTPServer(("localhost", 3000), HTTPRequestHandler)
    s.context = {"db": DB(), "plugin": CoinFlipPlugin()}
    s.serve_forever()
    s.server_close()


if __name__ == "__main__":
    main()
