import threading
import time

from engine.thread.RoboMasterThread import RoboMasterThread
from flymode import mainLogger


class TaskQueue(threading.Thread):
    stack: list[str] = []
    currentState: bool = False
    currentAction: str = ""
    lastAction: str = ""
    drone: RoboMasterThread
    paused: bool = False
    msg: str
    pauseAfterActions: list[str]

    def __init__(self, drone: RoboMasterThread) -> None:
        super().__init__()
        drone.recb = self.setMsg
        self.msg = ""
        self.drone = drone
        self.pauseAfterActions = []

    def setMsg(self, msg: str):
        self.msg = msg

    def getMsg(self):
        result = self.msg
        self.msg = ""
        return result

    def setAction(self, newAction: str):
        self.lastAction = self.currentAction
        self.currentAction = newAction

    def run(self):
        while True:
            if not self.currentState:
                self.next()
            response = self.getMsg()
            if response:
                mainLogger.info(f"task queue recv: {repr(response)}")
                while self.paused:
                    time.sleep(0.1)
                if response == "ok":
                    self.currentState = False
                elif response.startswith("error"):
                    self.restore()
                    self.next()
            time.sleep(0.01)

    def add(self, *command: str):
        self.stack.extend(command)

    def next(self):
        if len(self.stack) > 0:
            action = self.stack.pop(0)
            mainLogger.info(f"task queue sent msg: {action}")
            self.drone._sock.sendto(action.encode("utf8"), self.drone._roboAddress)
            self.setAction(action)
            self.currentState = True
            if action in self.pauseAfterActions:
                self.paused = True

    def restore(self):
        self.currentState = not self.currentState
        self.stack.insert(0, self.lastAction)
        mainLogger.info("restore")
