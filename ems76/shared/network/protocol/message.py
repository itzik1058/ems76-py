from io import BytesIO
from struct import pack, unpack
from enum import Enum


class Message(BytesIO):
    def __init__(self, message_type=None, *argv, initial_bytes=b''):
        super(Message, self).__init__(initial_bytes)
        if message_type:
            self.encode('u16', message_type)
            for arg in argv:
                self.encode(*arg)

    def __repr__(self):
        value = self.getvalue()
        return ' '.join([value.hex()[i:i + 2].upper() for i in range(0, len(value.hex()), 2)])

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
            case 'bool': self.encode('i8', int(value))
            case 'str':
                self.encode('u16', len(value))
                for c in value:
                    self.write(c.encode())
            case _: raise Exception('invalid type')

    def decode(self, t):
        match t:
            case 'i8': return unpack('b', self.read(1))[0]
            case 'i16': return unpack('h', self.read(2))[0]
            case 'i32': return unpack('i', self.read(4))[0]
            case 'i64': return unpack('l', self.read(8))[0]
            case 'u8': return unpack('B', self.read(1))[0]
            case 'u16': return unpack('H', self.read(2))[0]
            case 'u32': return unpack('I', self.read(4))[0]
            case 'u64': return unpack('L', self.read(8))[0]
            case 'bool': return bool(self.decode('i8'))
            case 'str': return ''.join(chr(self.decode('u8')) for _ in range(self.decode('u16')))
            case _: raise Exception('invalid type')
