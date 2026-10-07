from datetime import time
from alarm_clock.exceptions import InvalidAlarmLabelError, InvalidAlarmTimeError

class AlarmValidator:
    @staticmethod
    def parse_time(value: str) -> time:
        try:
            parsed = time.fromisoformat(value.strip())
        except ValueError as exc:
            raise InvalidAlarmTimeError("Use HH:MM format, e.g. 07:30.") from exc
        if parsed.second or parsed.microsecond:
            raise InvalidAlarmTimeError("Alarm time must have minute precision.")
        return parsed

    @staticmethod
    def validate_label(value: str) -> str:
        label = value.strip()
        if not label:
            raise InvalidAlarmLabelError("Alarm label cannot be empty.")
        if len(label) > 100:
            raise InvalidAlarmLabelError("Alarm label must be 100 characters or fewer.")
        return label
