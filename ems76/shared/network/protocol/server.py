from enum import Enum


class ServerMessage(Enum):
    HELLO = 0xE
    LOGIN_BACKGROUND = 0x16
