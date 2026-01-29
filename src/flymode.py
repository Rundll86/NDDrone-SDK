import os
import time

from psychopy import core, event

from engine.api.logging import mainLogger
from engine.core.configCore import Config
from engine.thread.ReceiveMessageThread import ReceiveMessaageThread
from engine.thread.RoboMasterThread import RoboMasterThread
from engine.util.connection import connectSocket
from engine.util.workdir import fromInternal
from engine.window.monitor import MonitorWindow


def main():
    mainLogger.info("loading")
    config = Config()

    # 配置一些路径常量
    picturePath = fromInternal("pics2")
    backgroundPath = fromInternal("background.jpg")
    promptPath = os.path.join(picturePath, "display_frame.png")
    # 飞控运行状态 & NeuroAI客户端
    stopFlag = False
    neuroApiSocket = connectSocket(config.neuroApiAddress, 5)

    # region 无人机线程
    # 无人机发送指令
    drone = RoboMasterThread(("192.168.10.1", 8889))
    drone.start()
    drone.send("command")
    time.sleep(1)
    drone.send("motoron")
    # 无人机接收指令
    messageReceiver = ReceiveMessaageThread(
        neuroApiSocket,
        drone,
        config.distance,
        lambda: stopFlag,
    )
    messageReceiver.start()

    # region 初始化闪烁窗口
    win = MonitorWindow(config.windowSize)
    win.coverText("Loading...", True)
    win.loadFlickerFrames(picturePath)
    win.loadDynamicFrames(backgroundPath, promptPath)

    # 第一帧，先把提示帧展示出来，等按空格开始
    win.prompt()
    event.waitKeys(keyList=["space"])

    while not stopFlag:
        # 给NeuroAI发消息准备开始接收识别结果
        currentTime = int(time.time() * 1000)
        neuroApiSocket.send(f"TIME:{currentTime}".encode("utf8"))
        # 开始闪烁
        win.flicker()
        while True:
            keys = event.getKeys()
            if "escape" in keys:
                stopFlag = True
                # 按了esc退出，先关窗口
                win.close()
                # 给无人机发降落，3秒后起桨降温
                drone.send("land")
                time.sleep(3)
                drone.send("motoron")
                break
            elif "space" in keys:
                break
            # 不需要每0.1秒扫一次键盘，只需要大概每2帧一次就行，也能让cpu休息
            # （软件计时器不精确，1帧可能不够休息）
            time.sleep(2 / 60)

    drone.close()
    neuroApiSocket.send(b"STOP")
    win.close()
    core.quit()


if __name__ == "__main__":
    main()
