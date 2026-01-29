from enum import Enum


class MessageType(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2


MESSAGETYPE_COLOR_MAP = {
    MessageType.INFO: "green",
    MessageType.WARNING: "yellow",
    MessageType.ERROR: "red",
}
