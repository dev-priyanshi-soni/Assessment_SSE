import sys
from alarm_clock.models import Alarm
from alarm_clock.ports import Notifier

class ConsoleNotifier(Notifier):
    def notify(self, alarm: Alarm) -> None:
        print(
            f"\n{'=' * 50}\n"
            f"🔔 ALARM {alarm.id}: {alarm.label}\n"
            f"Time: {alarm.time:%H:%M}\n"
            f"{'=' * 50}\n\a",
            file=sys.stdout, flush=True,
        )

    def wait_for_dismissal(self) -> None:
        try:
            input("Press Enter to dismiss the alarm...")
        except (EOFError, KeyboardInterrupt):
            pass
