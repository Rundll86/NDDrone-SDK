import datetime

import rich
from pydantic import BaseModel

from engine.api.logging.constants import MESSAGETYPE_COLOR_MAP, MessageType
from engine.api.timer import format


class LogRecord(BaseModel):
    type: MessageType
    message: str
    time: datetime.datetime

    def __init__(self, type: MessageType = MessageType.INFO, message: str = ""):
        super().__init__(type=type, message=message, time=datetime.datetime.now())

    def print(self):
        color = MESSAGETYPE_COLOR_MAP[self.type]
        rich.print(
            f"[{color}]\\[[cyan]{format(self.time)}[/cyan] {self.type.name}][/{color}] {self.message}"
        )


class Logger:
    records: list[LogRecord]

    def __init__(self) -> None:
        self.records = []

    def log(self, type: MessageType, message: str):
        record = LogRecord(type, message)
        self.records.append(record)
        record.print()

    def info(self, message: str):
        self.log(MessageType.INFO, message)

    def warning(self, message: str):
        self.log(MessageType.WARNING, message)

    def error(self, message: str | Exception):
        self.log(MessageType.ERROR, str(message))


mainLogger = Logger()
