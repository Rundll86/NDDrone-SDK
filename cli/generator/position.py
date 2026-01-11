from anchor import top, bottom, left, right, center

inputPosition = {
    "up": (630, 110),
    "down": (630, 750),
    "left": (950, 430),
    "right": (1590, 430),
    "forward": (1260, 110),
    "back": (1260, 750),
    "takeoff": (30, 110),
    "land": (30, 750),
    "flip": (330, 430),
}
disableKeys = ["land", "flip"]
outputPosition = {
    "up": (left(250 // 2), center(0, 0, 250)[1]),
    "down": (right(250 // 2), center(0, 0, 250)[1]),
    "left": (right(0), top(0)),
    "right": (right(0), bottom(0)),
    "forward": (left(0), top(0)),
    "back": (left(0), bottom(0)),
    "takeoff": center(0, 0, 500),
    "land": (left(0), bottom(0)),
    "flip": (right(0), bottom(0)),
}
outputTextMap = {
    "up": "短上",
    "down": "短下",
    "left": "短左",
    "right": "短右",
    "forward": "短前",
    "back": "短后",
    "takeoff": "步进",
    "land": "",
    "flip": "",
}
outputResultMap = {
    "up": 1,
    "down": 3,
    "left": 7,
    "right": 5,
    "forward": 4,
    "back": 6,
    "takeoff": 0,
    "land": 2,
    "flip": 8,
}
overwriteBlockSize = {
    "takeoff": 500,
    "up": 250,
    "down": 250,
}

inputKeys = list(inputPosition.keys())
for key in disableKeys:
    inputKeys.remove(key)
