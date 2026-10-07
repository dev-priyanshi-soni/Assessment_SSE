from dataclasses import dataclass, field
from datetime import date, time

@dataclass
class Alarm:
    id: int
    time: time
    label: str
    enabled: bool = True
    _last_triggered_date: date | None = field(default=None, repr=False)

    @property
    def last_triggered_date(self) -> date | None:
        return self._last_triggered_date

    def is_due(self, current_time: time, current_date: date) -> bool:
        return (
            self.enabled
            and self._last_triggered_date != current_date
            and current_time.hour == self.time.hour
            and current_time.minute == self.time.minute
        )

    def mark_triggered(self, triggered_date: date) -> None:
        self._last_triggered_date = triggered_date

    def disable(self) -> None:
        self.enabled = False

    def enable(self) -> None:
        self.enabled = True
