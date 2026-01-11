import os

import numpy as np


class Config:
    distance: int = 0

    def __init__(self) -> None:
        self.defaultConfig()

    def defaultConfig(
        self,
    ):
        self.displayINFO()
        self.expINFO()
        self.connectINFO()

    def displayINFO(self, refreshRate=60, window_size=(1920, 1080)):
        self.refreshRate = refreshRate
        self.windowSize = window_size

    def expINFO(
        self,
        srate=250,
        recordRate=1000,
        winLEN=3,
        lag=0.14,
        frequency=np.arange(8, 17, 1),
        distance=20,
    ):
        self.srate = srate
        self.record_srate = recordRate
        self.winLEN = winLEN
        self.lag = lag
        self.frequency = frequency
        self.distance = 0
        path = os.path.join(os.getcwd(), "readme.txt")
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            try:
                if line[:8] == "distance":
                    self.distance = int(line[10:])
            except:
                pass
        if self.distance is 0:
            self.distance = distance

    def connectINFO(
        self,
        droneAddress=("192.168.10.1", 8889),
        deviceAddress=("127.0.0.1", 8899),
        neuroApiAddress=("127.0.0.1", 11000),
    ):
        self.roboAddress = droneAddress
        self.deviceAddress = deviceAddress
        self.neuroApiAddress = neuroApiAddress


if __name__ == "__main__":
    config = Config()
