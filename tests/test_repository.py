from datetime import time
import pytest
from alarm_clock.models import Alarm
from alarm_clock.repository import InMemoryAlarmRepository
from alarm_clock.exceptions import AlarmNotFoundError

def test_ids():
    r = InMemoryAlarmRepository()
    assert r.add(Alarm(0,time(7,30),"A")).id == 1
    assert r.add(Alarm(0,time(8,30),"B")).id == 2

def test_sorted():
    r = InMemoryAlarmRepository()
    r.add(Alarm(0,time(18,0),"B"))
    r.add(Alarm(0,time(7,0),"A"))
    assert [a.label for a in r.list_all()] == ["A","B"]

def test_missing():
    with pytest.raises(AlarmNotFoundError):
        InMemoryAlarmRepository().get(1)
