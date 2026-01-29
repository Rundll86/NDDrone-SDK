import os

from psychopy import visual


class MonitorWindow(visual.Window):
    frames: list[visual.ImageStim] = []
    backgroundStim: visual.ImageStim
    promptStim: visual.ImageStim

    def __init__(
        self,
        size: tuple[int, int],
    ):
        super().__init__(
            size,
            monitor="testMonitor",
            units="pix",
            fullscr=False,
            waitBlanking=True,
            color=(0, 0, 0),
            colorSpace="rgb255",
            screen=0,
            allowGUI=True,
        )

    def coverText(self, text: str, draw: bool):
        stim = visual.TextStim(
            self,
            pos=[0, 0],
            text=text,
            color=(255, 255, 255),
            colorSpace="rgb255",
        )
        if draw:
            stim.draw()
            self.flip()
        return stim

    def coverImage(self, imagePath: str, draw: bool):
        stim = visual.ImageStim(
            self,
            image=imagePath,
            pos=[0, 0],
            size=self.size,
            units="pix",
            flipVert=False,
        )
        if draw:
            stim.draw()
            self.flip()
        return stim

    def loadFlickerFrames(self, picturePath: str):
        result: list[visual.ImageStim] = []
        for frameIndex in range(180):
            result.append(
                self.coverImage(
                    os.path.join(picturePath, f"{frameIndex}.png"),
                    False,
                )
            )
        self.frames = result
        return result

    def loadDynamicFrames(
        self,
        backgroundPath: str,
        promptPath: str,
    ):
        self.backgroundStim = self.coverImage(backgroundPath, False)
        self.promptStim = self.coverImage(promptPath, False)

    def flicker(self):
        for frame in self.frames:
            # 画背景图和当前帧，并且等待垂直同步渲染一帧
            self.backgroundStim.draw()
            frame.draw()
            self.flip()
        # 闪烁完了，展示提示帧
        self.prompt()

    def prompt(self):
        self.promptStim.draw()
        self.flip()
