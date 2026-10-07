from threading import RLock
from alarm_clock.exceptions import AlarmNotFoundError
from alarm_clock.models import Alarm
from alarm_clock.ports import AlarmRepository

class InMemoryAlarmRepository(AlarmRepository):
    def __init__(self) -> None:
        self._alarms: dict[int, Alarm] = {}
        self._next_id = 1
        self._lock = RLock()

    def add(self, alarm: Alarm) -> Alarm:
        with self._lock:
            alarm.id = self._next_id
            self._alarms[alarm.id] = alarm
            self._next_id += 1
            return alarm

    def get(self, alarm_id: int) -> Alarm:
        with self._lock:
            if alarm_id not in self._alarms:
                raise AlarmNotFoundError(f"Alarm {alarm_id} was not found.")
            return self._alarms[alarm_id]

    def list_all(self) -> list[Alarm]:
        with self._lock:
            return sorted(self._alarms.values(), key=lambda a: (a.time, a.id))

    def delete(self, alarm_id: int) -> None:
        with self._lock:
            if alarm_id not in self._alarms:
                raise AlarmNotFoundError(f"Alarm {alarm_id} was not found.")
            del self._alarms[alarm_id]
