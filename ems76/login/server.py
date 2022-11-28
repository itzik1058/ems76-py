import inspect
from ems76.shared.network.server import Server
from ems76.shared.network.client import Client
from ems76.shared.network.protocol.message import Message
from ems76.shared.network.protocol.handler import MessageHandler
from ems76.login import handler


class LoginServer(Server):
    def __init__(self, address):
        super(LoginServer, self).__init__(address)
        self.handlers = {}
        for _, member in inspect.getmembers(handler):
            if isinstance(member, MessageHandler):
                self.handlers[member.message_type.value] = member.handler

    async def on_client_accepted(self, client: Client):
        pass

    async def on_message_received(self, client: Client, message: Message):
        message_type = message.decode('u16')
        if message_type in self.handlers:
            await self.handlers[message_type](client, message)
