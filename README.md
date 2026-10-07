# Alarm Clock CLI

Python CLI alarm clock with automatic background scheduling.

## Run
```bash
pip install -e ".[dev]"
python -m alarm_clock
```

The scheduler starts automatically in a daemon background thread, so the main CLI
remains available for adding/listing/deleting alarms.

## Test
```bash
pytest
```

## Architecture
CLI -> AlarmService -> Repository
       Scheduler -> Clock + Notifier

The scheduler, clock, repository and notifier are separated for testability and
dependency inversion. `FakeClock` makes time-dependent tests deterministic.

## Scope
In-memory storage, one-time-per-day alarms, terminal notifications. No database,
web UI, or external services.
