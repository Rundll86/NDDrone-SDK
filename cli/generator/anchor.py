from constants import imageSize, blockSize


def top(distance: int) -> int:
    return distance


def bottom(distance: int) -> int:
    return imageSize[1] - blockSize - distance


def left(distance: int) -> int:
    return distance


def right(distance: int) -> int:
    return imageSize[0] - blockSize - distance


def center(offsetX: int, offsetY: int, blockSize: int = blockSize) -> tuple[int, int]:
    return (
        imageSize[0] // 2 - blockSize // 2 + offsetX,
        imageSize[1] // 2 - blockSize // 2 + offsetY,
    )
