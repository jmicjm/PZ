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
