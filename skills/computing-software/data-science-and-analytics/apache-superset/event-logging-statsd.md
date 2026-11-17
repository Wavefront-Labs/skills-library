---
id: computing-software.data-science-and-analytics.apache-superset.event-logging-statsd
name: event-logging-statsd
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [event-logging, statsd, db-event-logger, stats-logger, metrics]
level: practitioner
status: docs-checked
description: "Capture Superset events and metrics: EVENT_LOGGER with DBEventLogger or a custom class, STATS_LOGGER with StatsdStatsLogger and SERVER_STATSD env vars."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/event-logging.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record user actions and emit operational metrics.

Event logging: by default Superset logs special action events in its internal database through `DBEventLogger`; view them in the UI under Security, Action Log. You can implement your own event log class with a `log(self, user_id, action, *args, **kwargs)` method (keyword arguments include `records`, `dashboard_id`, `slice_id`, `duration_ms`, `referrer`). A custom class disables `DBEventLogger`, so the Action Log stops filling, unless your class extends the built-in `DBEventLogger`. Activate it with an instance in `superset_config.py`:

```python
EVENT_LOGGER = JSONStdOutEventLogger()
```

StatsD: most endpoints hit are logged, plus key events such as query start and end in SQL Lab. Superset can also collect Gunicorn metrics when these environment variables are set: `SERVER_STATSD_HOST`, `SERVER_STATSD_PORT` (for example `8125`) and `SERVER_STATSD_PREFIX` (for example `superset`).

```python
import os
from superset.stats_logger import StatsdStatsLogger

STATS_LOGGER = StatsdStatsLogger(
    host=os.environ.get("SERVER_STATSD_HOST", "localhost"),
    port=int(os.environ.get("SERVER_STATSD_PORT", "8125")),
    prefix=os.environ.get("SERVER_STATSD_PREFIX", "superset"),
)
```

`statsd` in version ~3.3.0 must be installed. A custom metrics logger can be written by deriving `superset.stats_logger.BaseStatsLogger`.

## Checked

2026-11-08. Confirmed against the Logging page (event logging and StatsD sections, page read in full). Removed: `AbstractEventLogger` as the base class (the page names `DBEventLogger` and a plain class), the `MyEventLogger` example, "install with the Superset extras", and the audit-versus-metrics usage advice with the oversized-cache counter.
Method: documentation only; no commands were run.
