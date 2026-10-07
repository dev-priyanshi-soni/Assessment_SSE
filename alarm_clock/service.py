from datetime import datetime
from alarm_clock.models import Alarm
from alarm_clock.ports import AlarmRepository
from alarm_clock.validation import AlarmValidator

class AlarmService:
    def __init__(self, repository: AlarmRepository) -> None:
        self._repository = repository
        self._validator = AlarmValidator()

    def create_alarm(self, alarm_time: str, label: str) -> Alarm:
        alarm = Alarm(0, self._validator.parse_time(alarm_time),
                      self._validator.validate_label(label))
        return self._repository.add(alarm)

    def list_alarms(self) -> list[Alarm]:
        return self._repository.list_all()

    def delete_alarm(self, alarm_id: int) -> None:
        self._repository.delete(alarm_id)

    def get_due_alarms(self, current: datetime) -> list[Alarm]:
        due = []
        for alarm in self._repository.list_all():
            if alarm.is_due(current.time(), current.date()):
                alarm.mark_triggered(current.date())
                due.append(alarm)
        return due
