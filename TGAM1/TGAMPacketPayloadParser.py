
class TGAMPacketPayloadParser:
    
    POOR_SIGNAL = 0x02
    ATTENTION = 0x04
    MEDITATION = 0x05
    BLINK_STRENGTH = 0x16 #???
    RAW = 0x80
    ASIC_EEG_POWER = 0x83
    EXCODE = 0x55
    

    def parseBigEndian(self, payload, idx, byteCount):
        value = 0
        mul = 256**(byteCount - 1)
        for byte in range(0, byteCount):
            value += payload[byte + idx] * mul
            mul /= 256
        return value

    def parseSingleByteCode(self, code, payload, idx):
        if code == self.POOR_SIGNAL:
            self.poorSignal = payload[idx]
        elif code == self.ATTENTION:
            self.attention = payload[idx]
        elif code == self.MEDITATION:
            self.meditation = payload[idx]
        elif code == self.BLINK_STRENGTH:
            self.blinkStrength = payload[idx]

    def parseMultiByteCode(self, code, payload, idx):
        if code == self.RAW:
            self.parseRaw(payload, idx)
        elif code == self.ASIC_EEG_POWER:
            self.parseEegPower(payload, idx)

    def parseEegPower(self, payload, idx):
        for band in range(0, 8):
            self.eggPower[band] = self.parseBigEndian(payload, idx, 3)
            idx += 3
    
    def parseRaw(self, payload, idx):
        self.raw = self.parseBigEndian(payload, idx, 2)

    def parsePayload(self, payload):
        self.poorSignal = -1
        self.attention = -1
        self.meditation = -1
        self.blinkStrength = -1
        self.raw = -1
        self.eggPower = [-1] * 8

        idx = 0
        while idx < len(payload):

            excodeCount = 0
            while payload[idx] == self.EXCODE:
                idx += 1
                excodeCount += 1

            code = payload[idx]
            idx += 1

            byteCount = 1
            if code >= 0x80:
                byteCount = payload[idx]
                idx += 1
                self.parseMultiByteCode(code, payload, idx)
            else:
                self.parseSingleByteCode(code, payload, idx)
            idx += byteCount
