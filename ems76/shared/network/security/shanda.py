class Shanda:
    @staticmethod
    def encode(data):
        for i in range(3):
            a = 0
            for j in range(len(data), 0, -1):
                x = data[len(data) - j]
                x = Shanda._roll_left(x, 3)
                x = (x + j) & 0xFF
                x ^= a
                a = x
                x = Shanda._roll_right(a, j)
                x ^= 0xFF
                x = (x + 0x48) & 0xFF
                data[len(data) - j] = x
            a = 0
            for j in range(len(data), 0, -1):
                x = data[j - 1]
                x = Shanda._roll_left(x, 4)
                x = (x + j) & 0xFF
                x ^= a
                a = x
                x ^= 0x13
                x = Shanda._roll_right(x, 3)
                data[j - 1] = x
        return data

    @staticmethod
    def decode(data):
        for i in range(3):
            b = 0
            for j in range(len(data), 0, -1):
                x = data[j - 1]
                x = Shanda._roll_left(x, 3)
                x ^= 0x13
                a = x
                x ^= b
                x = (x - j) & 0xFF
                x = Shanda._roll_right(x, 4)
                b = a
                data[j - 1] = x
            b = 0
            for j in range(len(data), 0, -1):
                x = data[len(data) - j]
                x = (x - 0x48) & 0xFF
                x ^= 0xFF
                x = Shanda._roll_left(x, j)
                a = x
                x ^= b
                x = (x - j) & 0xFF
                x = Shanda._roll_right(x, 3)
                b = a
                data[len(data) - j] = x
        return data

    @staticmethod
    def _roll_left(value, shift):
        value = (value << (shift % 8))
        value = (value & 0xFF) | (value >> 8)
        return value & 0xFF

    @staticmethod
    def _roll_right(value, shift):
        value = ((value << 8) >> (shift % 8))
        value = (value & 0xFF) | (value >> 8)
        return value & 0xFF
