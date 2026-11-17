---
id: computing-software.database-administration.couchdb.smoosh-scheduling-windows
name: smoosh-scheduling-windows
category: computing-software
field: database-administration
product: couchdb
tags: [smoosh, compaction, scheduling, strict-window, utc]
level: advanced
status: docs-checked
description: "Restrict a smoosh compaction channel to hours of the day with from, to and strict_window, in UTC, and the 60 second check behaviour."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/compaction.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each channel can run only during certain hours using `from`, `to` and `strict_window`:

```ini
[smoosh.overnight_channel]
from = 20:00
to = 06:00
strict_window = true
```

Times are interpreted in UTC (GMT), so express them in UTC.

- `strict_window = true`: active compactions are suspended on leaving the window and resumed on re-entering.
- `strict_window = false` (default): active compactions finish, but no new ones start.

Timing behaviour:

- A new channel starts a 60 second timer. It is then set to pending, and after 60 seconds it checks whether it should be running; if not it is paused. Another 60 second timer is started after each check.
- So for the first 60 seconds after leaving the window, or when a channel is created outside the window, compactions can run for up to 60 seconds.
- This differs from the old compaction daemon, which cancelled compactions outright.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/compaction page (Scheduling Windows): the channel example, UTC (GMT) requirement, strict_window true and false behaviour, the 60 second timer notes, contrast with the old daemon. Nothing removed.

Method: documentation only; no commands were run.
