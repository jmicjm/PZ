from TGAMPacketParser import *
from TGAMPacketPayloadParser import *

import serial
import matplotlib.pyplot as plt

BAND_COUNT = 8
SERIAL_PORT = "COM4"
LOG_FILENAME = "log.csv"
PLOT_RANGE_SEC = 30

parser = TGAMPacketParser()

attention_data = []
meditation_data = []
bands_data = [[] for x in range(0,BAND_COUNT)]
fig, ax = plt.subplots(10)
ax[0].set_title("attention")
ax[1].set_title("meditation")

with serial.Serial(SERIAL_PORT, 9600, timeout=10) as ser:
    with open(LOG_FILENAME, "w") as log_file:
        log_file.write(f'attention;meditation;0;1;2;3;4;5;6;7;poor_signal\n')
        while True:
            byte = int.from_bytes(ser.read(1), "little")
            isValid, payload = parser.parseByte(byte)

            if isValid:
                payloadParser = TGAMPacketPayloadParser()
                payloadParser.parsePayload(payload)

                def bandsToCSV():
                    str = ""
                    for i in range(0,BAND_COUNT):
                        str += f'{payloadParser.eggPower[i]};'
                    return str

                log_file.write(f'{payloadParser.attention};{payloadParser.meditation};{bandsToCSV()}{payloadParser.poorSignal}\n')

                if payloadParser.poorSignal > 0:
                    print(f'poor_signal: {payloadParser.poorSignal}')


                attention_data.append(payloadParser.attention)
                meditation_data.append(payloadParser.meditation)
                for i in range(0,BAND_COUNT):
                        bands_data[i].append(payloadParser.eggPower[i])
                if len(attention_data) > PLOT_RANGE_SEC:
                    attention_data.pop(0)
                    meditation_data.pop(0)
                    for i in range(0,BAND_COUNT):
                        bands_data[i].pop(0)
                    for i in range(0,BAND_COUNT+2):
                        ax[i].cla()

                ax[0].plot(attention_data)
                ax[1].plot(meditation_data)
                for i in range(0,BAND_COUNT):
                    ax[i+2].plot(bands_data[i])
                plt.pause(0.05)
