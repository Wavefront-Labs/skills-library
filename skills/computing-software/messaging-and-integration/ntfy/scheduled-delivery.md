---
id: computing-software.messaging-and-integration.ntfy.scheduled-delivery
name: scheduled-delivery
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, delay, scheduled, x-delay, timezone]
level: practitioner
status: docs-checked
description: "Schedule ntfy delivery with X-Delay/At/In, set timezones, and respect the 10 second minimum and 3 day default maximum."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled delivery

Header `X-Delay` with aliases `Delay`, `X-At`, `At`, `X-In`, `In`.

Accepted formats: Unix timestamp, RFC3339/ISO-8601 timestamp, duration (`30m`, `3h`, `2 days`), natural language (`10am`, `tomorrow, 3pm`).

```
curl -H "At: tomorrow, 10am" -d "Good morning" ntfy.sh/hello
curl -H "In: 30min" -d "Reminder" ntfy.sh/hello
```

## Timezone

`X-Timezone` (alias `Timezone`), the `timezone` query parameter, or JSON `timezone`, as an IANA name such as `Asia/Tokyo`. Without it the server's local timezone is used. An invalid name returns HTTP 400, but only when a delay is also given.

## Limits

- Minimum delay 10 seconds; maximum 3 days, configurable with `message-delay-limit`.
- Scheduled messages stay cached 12 hours past delivery by default. Server-side caching cannot be disabled when scheduling is used.

## Subscribing

Scheduled messages are not returned by the API unless you pass `scheduled=1` (alias `sched=1`); see the subscribe-polling-since skill.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Scheduled delivery: aliases, formats, timezone rules, 10 second minimum, 3 day maximum, 12 hour cache) and subscribe API page (scheduled=1, sched=1). Removed: the Verify step.
Method: documentation only; no commands were run.
