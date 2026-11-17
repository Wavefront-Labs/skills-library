---
id: computing-software.devops-ci-cd.semaphore-ui.runner-poll-interval-and-timeout
name: runner-poll-interval-and-timeout
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [runner-tuning, check-interval-seconds, timeout, heartbeat, runners, semaphore-ui]
level: advanced
status: docs-checked
description: "Tune runner check_interval_seconds (default 5) and connection.timeout_seconds (default 3)."
sources:
  - https://semaphoreui.com/docs/admin-guide/runners
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tune runner polling and timeouts

Goal: balance job pickup latency against request volume.

Poll interval in the runner config:

```json
{ "runner": { "check_interval_seconds": 5 } }
```

Variable: `SEMAPHORE_RUNNER_CHECK_INTERVAL_SECONDS`.

| Value | Effect |
|---|---|
| 1 | Pickup within about a second; lowest latency. |
| 5 (default) | Balanced. |
| 10-30 | Less HTTP traffic with many runners; slightly later starts. |

Zero or invalid values fall back to 5. Task progress is reported every second regardless; that request doubles as the heartbeat.

Request timeout:

```json
{ "runner": { "connection": { "timeout_seconds": 3 } } }
```

Variable: `SEMAPHORE_RUNNER_CONNECTION_TIMEOUT_SECONDS`. It bounds the TCP connect, the TLS handshake and the wait for response headers. Without it a server that accepts then goes silent would hang the runner, stop the heartbeat, and the server would mark the runner offline.

Rules of thumb:
- Keep the timeout below the poll interval.
- Raise it on slow links when the runner log says `timeout awaiting response headers`; a timed-out progress report keeps its log records and retries next cycle.
- Uploading request bodies is deliberately not bounded, so big log batches are not cut off.

Verify: the runner log shows no repeated `timeout awaiting response headers` messages.

## Checked

2026-11-07. Read in full: the Runners page, from its markdown source in the semaphore-docs repository (admin-guide/runners.md; no snippet files included). Confirmed: check_interval_seconds and its variable, the value table (1, 5 default, 10-30), the fallback to 5 for zero or invalid values, the one-second progress and heartbeat cadence, connection.timeout_seconds with its variable, the default of 3, what the timeout bounds, why it exists, the keep-it-below-the-interval rule, the timeout awaiting response headers log line, the retry of a timed-out progress report, and the unbounded body upload. Removed: the generic Verify step about load.
Method: documentation only; no commands were run.
