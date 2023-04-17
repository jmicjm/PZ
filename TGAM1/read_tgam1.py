from TGAMPacketParser import *
from TGAMPacketPayloadParser import *

import serial

parser = TGAMPacketParser()

with serial.Serial('COM4', 9600, timeout=10) as ser:
    while True:
        byte = int.from_bytes(ser.read(1), "little")
        isValid, payload = parser.parseByte(byte)

        if isValid:
            payloadParser = TGAMPacketPayloadParser()
            payloadParser.parsePayload(payload)
            print(f'poor_signal: {payloadParser.poorSignal}')
            print(f'attention: {payloadParser.attention}')
            print(f'meditation: {payloadParser.meditation}')
            print(f'blink strength: {payloadParser.blinkStrength}')
            print(f'raw: {payloadParser.raw}')
            print(f'bands: {payloadParser.eggPower}')