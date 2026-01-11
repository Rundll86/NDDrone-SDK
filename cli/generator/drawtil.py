from PIL import ImageDraw, ImageFont


def drawTextCenteredInBox(
    draw: ImageDraw.ImageDraw,
    text: str,
    rect: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
):
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0]
    height = box[3] - box[1]
    x = rect[0] + (rect[2] - rect[0] - width) / 2
    y = rect[1] + (rect[3] - rect[1] - height) / 2
    draw.text((x, y), text, fill=fill, font=font)
