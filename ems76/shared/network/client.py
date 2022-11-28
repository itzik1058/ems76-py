import logging
from random import randint
from ems76.shared.network.security.aes import MapleAes
from ems76.shared.network.security.iv import MapleIV
from ems76.shared.network.security.shanda import Shanda
from ems76.shared.network.protocol.message import Message
from ems76.shared.network.protocol.server import ServerMessage
from ems76.shared.util.config import *


class Client:
    def __init__(self, loop, socket, callback):
        self._loop = loop
        self._socket = socket
        self._callback = callback
        self._buffer = b''
        self._riv = MapleIV(randint(0, 2 ** 31 - 1))
        self._siv = MapleIV(randint(0, 2 ** 31 - 1))

    async def run(self):
        await self.send_message(
            ServerMessage.HELLO,
            ('u16', SERVER_VERSION),
            ('str', SERVER_SUBVERSION),
            ('i32', self._riv.value),
            ('i32', self._siv.value),
            ('i8', SERVER_LOCALE),
            aes=False
        )
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
            message = Message(initial_bytes=payload)
            logging.debug(f'Received {message}')
            await self._callback(self, message)

    async def send(self, payload: Message, aes=True):
        logging.debug(f'Sending {payload}')
        data = bytearray(payload.getvalue())
        if aes:
            message = bytearray(len(data) + 4)
            MapleAes.get_header(message, self._siv, len(data), SERVER_VERSION)
            message[4:] = MapleAes.transform(Shanda.encode(data), self._siv)
        else:
            message = data
        await self._loop.sock_sendall(self._socket, message)

    async def send_message(self, message_type: ServerMessage, *argv, aes=True):
        await self.send(Message(message_type, *argv), aes=aes)
