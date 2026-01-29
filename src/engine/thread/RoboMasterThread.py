import socket
import threading
import time
from datetime import datetime
from threading import Thread
from typing import Callable

from flymode import mainLogger


class RoboMasterThread(Thread):
    _roboAddress: tuple[str, int]
    _sock: socket.socket
    _get_info_last_time = datetime.now()
    recb: Callable

    def __init__(self, roboAddress):
        super().__init__()
        self._roboAddress = roboAddress
        self._is_running = True
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recb = lambda x: None
        self.repeat(3)

    def run(self):
        while self._is_running:
            try:
                response, ip = self._sock.recvfrom(128)
                response = response.decode(encoding="utf-8")
                if response == "ok" or response == "error":
                    mainLogger.info("RoboMaster Received  message: " + response)
                else:
                    mainLogger.info("Received message: " + response)
                self.recb(response)
                time.sleep(0.01)
            except Exception as e:
                mainLogger.error(e)
                time.sleep(1)

    def send(self, message: str):
        try:
            mainLogger.info("Send message: " + message)
            self._sock.sendto(message.encode(encoding="utf-8"), self._roboAddress)
        except Exception as e:
            mainLogger.error("RoboMaster Error sending: " + str(e))

    def close(self):
        self._is_running = False
        self._sock.close()
        mainLogger.info("Drone disconnected.")

    def requestDroneState(self):
        now = datetime.now()
        if now.second % 2 == 0:
            self.send("battery?")
        else:
            self.send("wifi?")

    def repeat(self, interval):
        self.requestDroneState()
        threading.Timer(interval, self.repeat, [interval]).start()
