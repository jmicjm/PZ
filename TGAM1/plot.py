from TGAMPacketParser import *
from TGAMPacketPayloadParser import *

import serial
import matplotlib.pyplot as plt

BAND_COUNT = 8
SERIAL_PORT = "COM4"
LOG_FILENAME = "log.csv"
PLOT_RANGE_SEC = 30

class Plot:
    def __init__(self):
        self.attention_data = []
        self.meditation_data = []
        self.bands_data = [[] for x in range(0,BAND_COUNT)]
        self.fig, self.ax = plt.subplots(10)
        self.ax[0].set_title("attention")
        self.ax[1].set_title("meditation")

    def update(self, payloadParser):
        self.attention_data.append(payloadParser.attention)
        self.meditation_data.append(payloadParser.meditation)
        for i in range(0,BAND_COUNT):
                self.bands_data[i].append(payloadParser.eggPower[i])
        if len(self.attention_data) > PLOT_RANGE_SEC:
            self.attention_data.pop(0)
            self.meditation_data.pop(0)
            for i in range(0,BAND_COUNT):
                self.bands_data[i].pop(0)
            for i in range(0,BAND_COUNT+2):
                self.ax[i].cla()

        self.ax[0].plot(self.attention_data)
        self.ax[1].plot(self.meditation_data)
        for i in range(0,BAND_COUNT):
            self.ax[i+2].plot(self.bands_data[i])
        plt.pause(0.1)


if __name__ == '__main__':
    parser = TGAMPacketParser()
    plot = Plot()  

    with serial.Serial(SERIAL_PORT, 9600, timeout=10) as ser:
        with open(LOG_FILENAME, "w") as log_file:
            log_file.write(f'attention;meditation;0;1;2;3;4;5;6;7;poor_signal\n')
            while True:
                byte = int.from_bytes(ser.read(1), "little")
                isValid, payload = parser.parseByte(byte)

                if isValid:
                    payloadParser = TGAMPacketPayloadParser()
                    payloadParser.parsePayload(payload)

                    plot.update(payloadParser)

                    def bandsToCSV():
                        str = ""
                        for i in range(0,BAND_COUNT):
                            str += f'{payloadParser.eggPower[i]};'
                        return str

                    log_file.write(f'{payloadParser.attention};{payloadParser.meditation};{bandsToCSV()}{payloadParser.poorSignal}\n')

                    if payloadParser.poorSignal > 0:
                        print(f'poor_signal: {payloadParser.poorSignal}')
            