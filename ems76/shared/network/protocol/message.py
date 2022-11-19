from io import BytesIO
from struct import pack
from enum import Enum


class Message(BytesIO):
    def __init__(self, message_type, *argv, initial_bytes=b''):
        super(Message, self).__init__(initial_bytes)
        self.encode('u16', message_type)
        for arg in argv:
            self.encode(*arg)

    def encode(self, t, value):
        if isinstance(value, Enum):
            value = value.value
        match t:
            case 'i8': self.write(pack('b', value))
            case 'i16': self.write(pack('h', value))
            case 'i32': self.write(pack('i', value))
            case 'i64': self.write(pack('l', value))
            case 'u8': self.write(pack('B', value))
            case 'u16': self.write(pack('H', value))
            case 'u32': self.write(pack('I', value))
            case 'u64': self.write(pack('L', value))
            case 'str':
                self.encode('u16', len(value))
                for c in value:
                    self.write(c.encode())
            case _: raise Exception('invalid type')
