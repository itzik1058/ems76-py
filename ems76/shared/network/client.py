from random import randint
from ems76.shared.network.security.aes import MapleAes
from ems76.shared.network.security.iv import MapleIV
from ems76.shared.network.security.shanda import Shanda
from ems76.shared.network.protocol.message import Message
from ems76.shared.network.protocol.server import ServerMessage
from ems76.shared.util.config import *


class Client:
    def __init__(self, loop, socket):
        self._loop = loop
        self._socket = socket
        self._buffer = b''
        self._riv = MapleIV(randint(0, 2 ** 31 - 1))
        self._siv = MapleIV(randint(0, 2 ** 31 - 1))

    async def run(self):
        await self.send(Message(
            ServerMessage.HELLO,
            ('u16', SERVER_VERSION),
            ('str', SERVER_SUBVERSION),
            ('i32', self._riv.value),
            ('i32', self._siv.value),
            ('i8', SERVER_LOCALE)
        ), aes=False)
        while True:
            fragment = await self._loop.sock_recv(self._socket, 4096)
            if not fragment:
                # TODO disconnect event
                pass
            self._buffer += fragment
            if len(self._buffer) < 4:
                continue
            length = MapleAes.get_length(self._buffer)
            if len(self._buffer) < 4 + length:
                continue
            payload = Shanda.decode(MapleAes.transform(bytearray(self._buffer[4:4 + length]), self._riv))
            self._buffer = self._buffer[4 + length:]
            print(f"Received {' '.join([payload.hex()[i:i + 2].upper() for i in range(0, len(payload.hex()), 2)])}")

    async def send(self, payload, aes=True):
        data = bytearray(payload.getvalue())
        print(f"Sending {' '.join([data.hex()[i:i + 2].upper() for i in range(0, len(data.hex()), 2)])}")
        if aes:
            message = bytearray(len(data) + 4)
            MapleAes.get_header(message, self._siv, len(data), SERVER_VERSION)
            message[4:] = MapleAes.transform(Shanda.encode(data), self._siv)
        else:
            message = data
        await self._loop.sock_sendall(self._socket, message)
