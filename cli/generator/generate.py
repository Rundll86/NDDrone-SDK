import os
import threading
from configparser import ConfigParser

from constants import blockSize, imageSize, subtitleSize
from drawtil import drawTextCenteredInBox
from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from position import (
    inputKeys,
    inputPosition,
    outputPosition,
    outputResultMap,
    outputTextMap,
    overwriteBlockSize,
)


def process(inputImage: Image.Image, text: bool) -> Image.Image:
    outputImage = Image.new("RGBA", imageSize, (0, 0, 0, 0))
    outputDraw = ImageDraw(outputImage)
    colorMap = {}
    for key in inputKeys:
        realBlockSize = blockSize
        if key in overwriteBlockSize:
            realBlockSize = overwriteBlockSize[key]
        colorMap[key] = inputImage.getpixel(inputPosition[key])
        outputDraw.rectangle(
            (
                outputPosition[key],
                (
                    outputPosition[key][0] + realBlockSize,
                    outputPosition[key][1] + realBlockSize,
                ),
            ),
            fill=colorMap[key],
            outline=(255, 0, 0),
            width=useBorder,
        )
        outputDraw.line(
            (
                outputPosition[key][0] - crossLength + realBlockSize // 2,
                outputPosition[key][1] + realBlockSize // 2,
                outputPosition[key][0] + crossLength + realBlockSize // 2,
                outputPosition[key][1] + realBlockSize // 2,
            ),
            fill=(255, 0, 0),
            width=crossWidth,
        )
        outputDraw.line(
            (
                outputPosition[key][0] + realBlockSize // 2,
                outputPosition[key][1] - crossLength + realBlockSize // 2,
                outputPosition[key][0] + realBlockSize // 2,
                outputPosition[key][1] + crossLength + realBlockSize // 2,
            ),
            fill=(255, 0, 0),
            width=crossWidth,
        )
    if text:
        for key in inputKeys:
            realBlockSize = blockSize
            if key in overwriteBlockSize:
                realBlockSize = overwriteBlockSize[key]
            drawTextCenteredInBox(
                outputDraw,
                outputTextMap[key],
                (
                    outputPosition[key][0],
                    outputPosition[key][1],
                    outputPosition[key][0] + realBlockSize,
                    outputPosition[key][1] + realBlockSize,
                ),
                ImageFont.truetype("C:/Windows/Fonts/Deng.ttf", 50),
                (0, 0, 0),
            )
            drawTextCenteredInBox(
                outputDraw,
                f"T{outputResultMap[key]}:{key}",
                (
                    outputPosition[key][0],
                    outputPosition[key][1] + subtitleSize,
                    outputPosition[key][0] + realBlockSize,
                    outputPosition[key][1] + realBlockSize,
                ),
                ImageFont.truetype("C:/Windows/Fonts/Deng.ttf", 35),
                (100, 100, 100),
            )
    return outputImage


def frame(index: int):
    global finishedCount
    process(
        Image.open(os.path.join(inputPath, f"{index}.png")),
        False,
    ).save(
        os.path.join(outputPath, f"{index}.png"),
    )
    finishedCount += 1
    print(
        f"已完成{finishedCount}/{totalCount+useBackground}(线程{createdThread}/{totalCount}个)",
        end="\r",
    )
    if finishedCount == totalCount + useBackground:
        print("")


parser = ConfigParser()
parser.read("config.ini")
debug = parser.getboolean("build", "debug")

inputPath = "blocks"
outputPath = os.path.join(
    "dist" if debug else parser["runtime"]["path"],
    "_internal",
    "pics2",
)
useBackground = True
crossLength = 10
crossWidth = 3
useBorder = False

totalCount = int(parser["frames"]["count"])
finishedCount = 0
createdThread = 0

if not os.path.exists(outputPath):
    os.makedirs(outputPath, exist_ok=True)
if useBackground:
    process(
        Image.open(os.path.join(inputPath, "display_frame.png")),
        True,
    ).save(os.path.join(outputPath, "display_frame.png"))
    finishedCount += 1
for i in range(totalCount):
    threading.Thread(target=lambda: frame(i)).start()
    createdThread += 1
