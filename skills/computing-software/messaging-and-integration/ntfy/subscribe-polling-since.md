---
id: computing-software.messaging-and-integration.ntfy.subscribe-polling-since
name: subscribe-polling-since
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, polling, since, scheduled, replay]
level: practitioner
status: docs-checked
description: "Fetch cached ntfy messages with poll=1 and since, include scheduled messages, and respect the 10 MB replay cap."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polling and since

`poll=1` (aliases `po`, `X-Poll`) returns cached messages and closes the connection.

```
curl -s "ntfy.sh/mytopic/json?poll=1"
curl -s "ntfy.sh/mytopic/json?poll=1&since=10m"
curl -s "ntfy.sh/mytopic/json?poll=1&since=latest"
```

`since` (aliases `si`, `X-Since`) takes a duration (`10m`, `30s`), a Unix timestamp, a message ID, or `all`. `since=latest` returns only the newest cached message. A poll without `since` defaults to `all` and can be large.

## Scheduled messages

Add `scheduled=1` (aliases `sched=1`, `X-Scheduled`); without it scheduled messages are not returned.

## Replay limits

- A replay returns only the newest messages that fit in 10 MB per topic; a capped response sets header `X-Messages-Truncated: 1`.
- Replayed bytes count against the daily bandwidth budget shared with attachment downloads. Exceeding it returns HTTP 429 with error code 42905 and writes no messages.
- For repeated polling pass `since=<last message ID>`.

## Gotcha

Reading back what you missed only works if the server has message caching configured.

## Checked

2026-11-04. Confirmed against the ntfy subscribe API page (Poll for messages, Fetch cached messages, latest, scheduled, Replay limits: 10 MB per topic, X-Messages-Truncated, 429 and 42905). Removed: the Verify step.
Method: documentation only; no commands were run.
