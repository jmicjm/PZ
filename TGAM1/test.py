from TGAMPacketParser import *
from TGAMPacketPayloadParser import *

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
    print(parser.state)

    if isValid:
        print("success\npayload:")
        print([hex(byte) for byte in payload])

        payloadParser = TGAMPacketPayloadParser()
        payloadParser.parsePayload(payload)
        print(f'poor_signal: {payloadParser.poorSignal}')
        print(f'attention: {payloadParser.attention}')
        print(f'meditation: {payloadParser.meditation}')
        print(f'blink strength: {payloadParser.blinkStrength}')
        print(f'raw: {payloadParser.raw}')
        print(f'bands: {payloadParser.eggPower}')

