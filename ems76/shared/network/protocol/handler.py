from ems76.shared.network.protocol.client import ClientMessage


class MessageHandler:
    def __init__(self, message_type: ClientMessage, handler):
        self.message_type = message_type
        self.handler = handler


def message_handler(message_type):
    return lambda f: MessageHandler(message_type, f)
