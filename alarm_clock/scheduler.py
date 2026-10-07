import threading
from alarm_clock.ports import Clock, Notifier
from alarm_clock.service import AlarmService

class AlarmScheduler:
    def __init__(self, service: AlarmService, clock: Clock,
                 notifier: Notifier, interval_seconds: float = 1.0) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be greater than zero.")
        self._service = service
        self._clock = clock
        self._notifier = notifier
        self._interval_seconds = interval_seconds
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        with self._lock:
            if self.is_running:
                return
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._run, name="alarm-scheduler", daemon=True
            )
            self._thread.start()

    def stop(self) -> None:
        with self._lock:
            self._stop_event.set()
            thread = self._thread
        if thread and thread.is_alive():
            thread.join(timeout=3)
        with self._lock:
            self._thread = None

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._check_alarms()
            except Exception as exc:
                print(f"\nScheduler error: {exc}", flush=True)
            self._stop_event.wait(self._interval_seconds)

    def _check_alarms(self) -> None:
        for alarm in self._service.get_due_alarms(self._clock.now()):
            self._notifier.notify(alarm)
            self._notifier.wait_for_dismissal()
