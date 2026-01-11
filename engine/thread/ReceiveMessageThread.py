import threading, socket, time
from RoboMasterThread import RoboMasterThread
from typing import Callable


class ReceiveMessaageThread(threading.Thread):
    clientSocket: socket.socket
    drone: RoboMasterThread
    step: int
    stopFlag: Callable[..., bool]

    def __init__(
        self,
        clientSocket: socket.socket,
        drone: RoboMasterThread,
        step: int,
        stopFlag: Callable[..., bool],
    ) -> None:
        super().__init__()
        self.clientSocket = clientSocket
        self.drone = drone
        self.step = step
        self.stopFlag = stopFlag

    def run(self) -> None:
        self.clientSocket.settimeout(20000)
        while self.isRunning():
            consumeMsg = self.clientSocket.recv(1024)
            if consumeMsg:
                message = str(consumeMsg)[2:-1]
                if len(message) > 5:
                    pass
            time.sleep(0.1)

    def isRunning(self):
        return not self.stopFlag()
