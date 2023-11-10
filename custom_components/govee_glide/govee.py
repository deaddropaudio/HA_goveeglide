import socket
import json
import logging

logger = logging.getLogger("govee")


class Wandlicht:
    def __init__(self, host) -> None:
        self.ip = host
        self.port = 4003
        self.name = "Govee Glide"
        self._is_on = None
        self._brightness = None
        self._color = None

    async def sendMessage(self, message):
        MESSAGE = json.dumps(message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(MESSAGE.encode(), (self.ip, self.port))

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    async def set_on_off(self, state: int):
        message = {}
        message["msg"] = {}
        message["msg"]["cmd"] = "turn"
        message["msg"]["data"] = {}
        message["msg"]["data"]["value"] = state
        await self.sendMessage(message)
        self._is_on = True if state == 1 else False

    async def set_brightness(self, state: int):
        state_scaled = (state / 255) * 100
        message = {}
        message["msg"] = {}
        message["msg"]["cmd"] = "brightness"
        message["msg"]["data"] = {}
        message["msg"]["data"]["value"] = state_scaled
        await self.sendMessage(message)
        self._brightness = state

    async def set_color(self, rgb: tuple) -> None:
        message = {}
        message["msg"] = {}
        message["msg"]["cmd"] = "colorwc"
        message["msg"]["data"] = {}
        message["msg"]["data"]["color"] = {}
        message["msg"]["data"]["color"]["r"] = rgb[0]
        message["msg"]["data"]["color"]["g"] = rgb[1]
        message["msg"]["data"]["color"]["b"] = rgb[2]
        await self.sendMessage(message)
        self._color = rgb
