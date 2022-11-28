import logging
from ems76.shared.network.client import Client
from ems76.shared.network.protocol.message import Message
from ems76.shared.network.protocol.handler import message_handler
from ems76.shared.network.protocol.client import ClientMessage
from ems76.shared.network.protocol.server import ServerMessage


@message_handler(ClientMessage.X1F)
async def on_1f(client: Client, message: Message):
    await client.send_message(
        ServerMessage.LOGIN_BACKGROUND,
        ('str', 'MapLogin')
    )
