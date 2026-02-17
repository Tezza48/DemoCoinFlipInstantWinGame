
from abc import ABC, abstractmethod
from typing import Any, TypedDict


class BaseHandler(ABC):
    @abstractmethod
    def handle(request: dict, player) -> dict:
        pass

class BasePlugin:
    def __init__(self):
        self.routes: dict = {}

    def add_route(self, verb, handler: BaseHandler):
        self.routes[verb] = handler

    def handle_request(self, verb: str, request: dict, player) -> dict:
        handler: BaseHandler = self.routes[verb]
        if handler is not None:
            return handler.handle(request, player)
        else:
            raise Exception("Unknown route '{}'".format(verb))
