from abc import ABC
from asyncio import create_task
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from ems76.shared.network.client import Client


class Server(ABC):
    def __init__(self, address):
        self._address = address
        self._listener = None
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.setblocking(False)
        self._socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    async def run(self, loop):
        self._socket.bind(self._address)
        self._socket.listen(0)
        self._listener = loop.create_task(self.listener(loop))

    async def listener(self, loop):
        while True:
            client, _ = await loop.sock_accept(self._socket)
            client.setblocking(False)
            client.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
            create_task(self.on_client_accepted(loop, client))

    async def on_client_accepted(self, loop, client_socket):
        client = Client(loop, client_socket)
        print(f'accepted socket {client_socket}')
        try:
            await client.run()
        except ConnectionResetError as e:
            print(f'client disconnected: {e}')
