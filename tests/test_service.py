from datetime import datetime
import pytest
from alarm_clock.exceptions import AlarmNotFoundError
from alarm_clock.repository import InMemoryAlarmRepository
from alarm_clock.service import AlarmService

@pytest.fixture
def service():
    return AlarmService(InMemoryAlarmRepository())

def test_create_alarm(service):
    alarm = service.create_alarm("07:30", "Wake up")
    assert alarm.id == 1
    assert alarm.label == "Wake up"

def test_delete_alarm(service):
    alarm = service.create_alarm("07:30", "Wake up")
    service.delete_alarm(alarm.id)
    assert service.list_alarms() == []

def test_delete_missing_alarm(service):
    with pytest.raises(AlarmNotFoundError):
        service.delete_alarm(999)

def test_due_alarm(service):
    service.create_alarm("07:30", "Wake up")
    assert len(service.get_due_alarms(datetime(2026,10,7,7,30))) == 1

def test_alarm_only_triggers_once_per_day(service):
    service.create_alarm("07:30", "Wake up")
    assert len(service.get_due_alarms(datetime(2026,10,7,7,30))) == 1
    assert service.get_due_alarms(datetime(2026,10,7,7,30)) == []

def test_alarm_triggers_next_day(service):
    service.create_alarm("07:30", "Wake up")
    service.get_due_alarms(datetime(2026,10,7,7,30))
    assert len(service.get_due_alarms(datetime(2026,10,8,7,30))) == 1
