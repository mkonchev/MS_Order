from enum import Enum


class Status(str, Enum):
    ok = "ok"
    wait = "wait"
    error = "error"
