import abc
from abc import ABC
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from ems76.shared.network.client import Client
from ems76.shared.network.protocol.message import Message


class Server(ABC):
    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.setblocking(False)
        self._socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    async def run(self, loop):
        self._socket.bind(self._address)
        self._socket.listen(0)
        loop.create_task(self.accept(loop))

    async def accept(self, loop):
        while True:
            client, _ = await loop.sock_accept(self._socket)
            client.setblocking(False)
            client.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
            loop.create_task(self.accept_client(loop, client))

    async def accept_client(self, loop, client_socket):
        client = Client(loop, client_socket, self.on_message_received)
        print(f'accepted socket {client_socket}')
        try:
            await self.on_client_accepted(client)
            await client.run()
        except ConnectionResetError as e:
            print(f'client disconnected: {e}')

    @abc.abstractmethod
    async def on_client_accepted(self, client: Client): ...

    @abc.abstractmethod
    async def on_message_received(self, client: Client, message: Message): ...
