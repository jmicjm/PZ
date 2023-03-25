from enum import Enum


class TGAMPacketParser:

    class State(Enum):
        WAITING_FOR_SYNC = 0
        READING_PLENGTH = 1
        READING_PAYLOAD = 2
        READING_CHECKSUM = 3
    
    SYNC = 0xAA
    PLENGTH_MAX_SIZE = 170

    def __init__(self):
        self.state = self.State.WAITING_FOR_SYNC
        self.syncCount = 0
        self.plength = 0
        self.payloadByteSum = 0
        self.payload = []
        self.isPayloadValid = False
        self.stateHandlers = {
            self.State.WAITING_FOR_SYNC : self.waitingForSyncStateHandler,
            self.State.READING_PLENGTH : self.readingPlengthStateHandler,
            self.State.READING_PAYLOAD : self.readingPayloadStateHandler,
            self.State.READING_CHECKSUM : self.readingChecksumStateHandler
        }

    def waitingForSyncStateHandler(self, byte):
        if byte == self.SYNC:
            self.syncCount = self.syncCount + 1
            if self.syncCount == 2:
                self.state = self.State.READING_PLENGTH
                self.syncCount = 0
        else:
            self.syncCount = 0
        return False

    def readingPlengthStateHandler(self, byte):
        if byte == self.PLENGTH_MAX_SIZE:
            return False
        if byte > self.PLENGTH_MAX_SIZE:
            self.state = self.State.WAITING_FOR_SYNC
            return False
        self.state = self.State.READING_PAYLOAD
        self.plength = byte
        self.payloadByteSum = 0
        self.payload = []
        return False

    def readingPayloadStateHandler(self, byte):
        self.payload.append(byte)
        self.payloadByteSum += byte
        self.plength = self.plength - 1
        if self.plength == 0:
            self.state = self.State.READING_CHECKSUM
        return False

    def readingChecksumStateHandler(self, byte):
        self.state = self.State.WAITING_FOR_SYNC
        checksum = self.payloadByteSum & 0xFF
        checksum = ~checksum & 0xFF
        if checksum == byte:
            return True
        return False
               

    def parseByte(self, byte):
        return (self.stateHandlers[self.state](byte), self.payload)



##########################################TEST
parser = TGAMPacketParser()

testPacket = [
    0xAA, # [SYNC]
    0xAA, # [SYNC]
    0x20, # [PLENGTH] (payload length) of 32 bytes
    0x02, # [POOR_SIGNAL] Quality
    0x00, # No poor signal detected (0/200)
    0x83, # [ASIC_EEG_POWER_INT]
    0x18, # [VLENGTH] 24 bytes
    0x00, # (1/3) Begin Delta bytes
    0x00, # (2/3)
    0x94, # (3/3) End Delta bytes
    0x00, # (1/3) Begin Theta bytes
    0x00, # (2/3)
    0x42, # (3/3) End Theta bytes
    0x00, # (1/3) Begin Low-alpha bytes
    0x00, # (2/3)
    0x0B, # (3/3) End Low-alpha bytes
    0x00, # (1/3) Begin High-alpha bytes
    0x00, # (2/3)
    0x64, # (3/3) End High-alpha bytes
    0x00, # (1/3) Begin Low-beta bytes
    0x00, # (2/3)
    0x4D, # (3/3) End Low-beta bytes
    0x00, # (1/3) Begin High-beta bytes
    0x00, # (2/3)
    0x3D, # (3/3) End High-beta bytes
    0x00, # (1/3) Begin Low-gamma bytes
    0x00, # (2/3)
    0x07, # (3/3) End Low-gamma bytes
    0x00, # (1/3) Begin Mid-gamma bytes
    0x00, # (2/3)
    0x05, # (3/3) End Mid-gamma bytes
    0x04, # [ATTENTION] eSense
    0x0D, # eSense Attention level of 13
    0x05, # [MEDITATION] eSense
    0x3D, # eSense Meditation level of 61
    0x34 # [CHKSUM] (1's comp inverse of 8-bit Payload sum of 0xCB)
]

for byte in testPacket:
    isValid, payload = parser.parseByte(byte)

    if isValid:
        print("success")
        print([hex(byte) for byte in payload])
    print(parser.state)
