import struct

class ReadPacket:  # lit un packet tcp
    def __init__(self, client):
        self.client = client.get_client_socket()[0]

    def read_string(self):
        size = int.from_bytes(self.client.recv(4), "big")
        ret = self.client.recv(size).decode("UTF-8")
        return ret

    def read_int(self):
        ret = self.client.recv(4)
        return int.from_bytes(ret, "big", signed=True)

    def read_float(self):
        return struct.unpack(">f", self.client.recv(4))[0]

    def read_byte(self):
        ret = self.client.recv(1)
        return int.from_bytes(ret, "big", signed=True)

class ReadUdpPacket:  # lit un packet udp
    def __init__(self, data):
        self.data = data
        self.index = 0

    def read_string(self):
        size = self.read_int()
        ret = self.data[self.index:self.index+size]
        self.index += size
        return ret

    def read_int(self):
        ret = self.data[self.index:self.index+4]
        self.index += 4
        return int.from_bytes(ret, "big")

    def read_byte(self):

        ret = self.data[self.index]
        self.index += 1
        return ret

    def read_float(self):
        ret = struct.unpack(">f", self.data[self.index:self.index+4])[0]
        self.index += 4
        return ret

class WritePacket:  # écrit un packet
    def __init__(self, type_: int):
        self.bytes = []
        self.type = type_
        self.bytes.append(self.type.to_bytes(1, "big"))

    def write_string(self, string: str):
        self.bytes.append(len(string.encode("UTF-8")).to_bytes(4, "big"))
        self.bytes.append(string.encode("UTF-8"))

    def write_int(self, int_: int):
        self.bytes.append(int_.to_bytes(4, "big", signed=True))

    def write_byte(self, byte: int):
        self.bytes.append(byte.to_bytes(1, "big"))

    def write_bytes(self, bytes_):
        self.write_int(len(bytes_))
        for byte in bytes_:
            self.write_byte(byte)

    def write_float(self, float_):
        self.bytes.append(struct.pack(">f", float_))

    def get_bytes(self):
        return b"".join(self.bytes)
