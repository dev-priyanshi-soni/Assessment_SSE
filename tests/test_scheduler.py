from datetime import datetime
from alarm_clock.clock import FakeClock
from alarm_clock.models import Alarm
from alarm_clock.notifier import ConsoleNotifier
from alarm_clock.repository import InMemoryAlarmRepository
from alarm_clock.scheduler import AlarmScheduler
from alarm_clock.service import AlarmService

class RecordingNotifier(ConsoleNotifier):
    def __init__(self):
        self.notifications = []
        self.dismissals = 0
    def notify(self, alarm: Alarm):
        self.notifications.append(alarm)
    def wait_for_dismissal(self):
        self.dismissals += 1

def make_scheduler(dt):
    service = AlarmService(InMemoryAlarmRepository())
    notifier = RecordingNotifier()
    scheduler = AlarmScheduler(service, FakeClock(dt), notifier, .01)
    return service, notifier, scheduler

def test_due_notification():
    service, notifier, scheduler = make_scheduler(datetime(2026,10,7,7,30))
    service.create_alarm("07:30","Wake up")
    scheduler._check_alarms()
    assert len(notifier.notifications) == 1
    assert notifier.dismissals == 1

def test_not_due():
    service, notifier, scheduler = make_scheduler(datetime(2026,10,7,7,29))
    service.create_alarm("07:30","Wake up")
    scheduler._check_alarms()
    assert notifier.notifications == []

def test_start_stop():
    _, _, scheduler = make_scheduler(datetime(2026,10,7,7,29))
    assert not scheduler.is_running
    scheduler.start()
    assert scheduler.is_running
    scheduler.stop()
    assert not scheduler.is_running
