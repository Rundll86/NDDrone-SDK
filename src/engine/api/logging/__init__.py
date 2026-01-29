import datetime

import rich
from pydantic import BaseModel

from engine.api.logging.constants import MESSAGETYPE_COLOR_MAP, MessageType
from engine.api.timer import format


class LogRecord(BaseModel):
    type: MessageType
    message: str
    time: datetime.datetime
    moduleName: str

    def __init__(
        self,
        type: MessageType = MessageType.INFO,
        message: str = "",
        moduleName: str = "main",
    ):
        super().__init__(
            type=type,
            message=message,
            time=datetime.datetime.now(),
            moduleName=moduleName,
        )

    def print(self):
        color = MESSAGETYPE_COLOR_MAP[self.type]
        rich.print(
            f"[cyan]{format(self.time)}[/cyan] [{color}]\\[{self.type.name}][/{color}] {self.message}"
        )


class Logger:
    records: list[LogRecord]
    moduleName: str

    def __init__(self, moduleName: str) -> None:
        self.records = []
        self.moduleName = moduleName

    def log(self, type: MessageType, message: str):
        record = LogRecord(type, message, self.moduleName)
        self.records.append(record)
        record.print()

    def info(self, message: str):
        self.log(MessageType.INFO, message)

    def warning(self, message: str):
        self.log(MessageType.WARNING, message)

    def error(self, message: str | Exception):
        self.log(MessageType.ERROR, str(message))


loggerMain = Logger("main")
