from datetime import datetime

class SystemClock:
    def now(self) -> datetime:
        return datetime.now()

class FakeClock:
    def __init__(self, current: datetime) -> None:
        self._current = current

    def now(self) -> datetime:
        return self._current

    def set(self, current: datetime) -> None:
        self._current = current
