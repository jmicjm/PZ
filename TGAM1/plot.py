from TGAMPacketParser import *
from TGAMPacketPayloadParser import *

import serial
import matplotlib.pyplot as plt

parser = TGAMPacketParser()

attention_data = []
meditation_data = []
bands_data = [[] for x in range(0,8)]
fig, ax = plt.subplots(10)
ax[0].set_title("attention")
ax[1].set_title("meditation")

with serial.Serial('COM3', 9600, timeout=10) as ser:
    while True:
        byte = int.from_bytes(ser.read(1), "little")
        isValid, payload = parser.parseByte(byte)

        if isValid:
            payloadParser = TGAMPacketPayloadParser()
            payloadParser.parsePayload(payload)
            if payloadParser.poorSignal > 0:
                print(f'poor_signal: {payloadParser.poorSignal}')


            attention_data.append(payloadParser.attention)
            meditation_data.append(payloadParser.meditation)
            for i in range(0,8):
                    bands_data[i].append(payloadParser.eggPower[i])
            if len(attention_data) > 30:
                attention_data.pop(0)
                meditation_data.pop(0)
                for i in range(0,8):
                    bands_data[i].pop(0)
                for i in range(0,10):
                    ax[i].cla()

            ax[0].plot(attention_data)
            ax[1].plot(meditation_data)
            for i in range(0,8):
                ax[i+2].plot(bands_data[i])
            plt.pause(0.05)
