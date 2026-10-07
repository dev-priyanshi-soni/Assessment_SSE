from datetime import time
import pytest
from alarm_clock.exceptions import InvalidAlarmLabelError, InvalidAlarmTimeError
from alarm_clock.validation import AlarmValidator

def test_valid_time():
    assert AlarmValidator.parse_time("07:30") == time(7,30)

@pytest.mark.parametrize("value", ["25:00", "07:60", "abc", "", "7"])
def test_invalid_time(value):
    with pytest.raises(InvalidAlarmTimeError):
        AlarmValidator.parse_time(value)

def test_invalid_label():
    with pytest.raises(InvalidAlarmLabelError):
        AlarmValidator.validate_label("")

def test_trim_label():
    assert AlarmValidator.validate_label(" Wake up ") == "Wake up"
