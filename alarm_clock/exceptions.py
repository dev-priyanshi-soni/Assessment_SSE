class AlarmClockError(Exception):
    pass

class AlarmNotFoundError(AlarmClockError):
    pass

class InvalidAlarmTimeError(AlarmClockError):
    pass

class InvalidAlarmLabelError(AlarmClockError):
    pass
