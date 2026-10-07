from alarm_clock.clock import SystemClock
from alarm_clock.exceptions import AlarmClockError
from alarm_clock.notifier import ConsoleNotifier
from alarm_clock.repository import InMemoryAlarmRepository
from alarm_clock.scheduler import AlarmScheduler
from alarm_clock.service import AlarmService

class CLI:
    def __init__(self) -> None:
        service = AlarmService(InMemoryAlarmRepository())
        self._service = service
        self._scheduler = AlarmScheduler(service, SystemClock(), ConsoleNotifier())

    def run(self) -> None:
        self._scheduler.start()
        print("\nAlarm Clock\n-----------")
        print("Scheduler started automatically.")
        try:
            while True:
                print("\n1. Add alarm\n2. List alarms\n3. Delete alarm\n4. Exit")
                choice = input("Choose an option: ").strip()
                if choice == "1":
                    self._add_alarm()
                elif choice == "2":
                    self._list_alarms()
                elif choice == "3":
                    self._delete_alarm()
                elif choice == "4":
                    break
                else:
                    print("Invalid option. Please choose 1-4.")
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down...")
        finally:
            self._scheduler.stop()
            print("Application stopped.")

    def _add_alarm(self) -> None:
        try:
            alarm = self._service.create_alarm(
                input("Enter alarm time (HH:MM): "),
                input("Enter label: "),
            )
            print(f"Alarm {alarm.id} created for {alarm.time:%H:%M} - {alarm.label}")
        except AlarmClockError as exc:
            print(f"Error: {exc}")

    def _list_alarms(self) -> None:
        alarms = self._service.list_alarms()
        if not alarms:
            print("No alarms configured.")
            return
        print("\nID   TIME   STATUS   LABEL")
        print("-" * 50)
        for alarm in alarms:
            print(f"{alarm.id:<4} {alarm.time:%H:%M}   "
                  f"{'enabled' if alarm.enabled else 'disabled':<8} {alarm.label}")

    def _delete_alarm(self) -> None:
        try:
            alarm_id = int(input("Enter alarm ID to delete: "))
            self._service.delete_alarm(alarm_id)
            print(f"Alarm {alarm_id} deleted.")
        except ValueError:
            print("Error: Alarm ID must be an integer.")
        except AlarmClockError as exc:
            print(f"Error: {exc}")
