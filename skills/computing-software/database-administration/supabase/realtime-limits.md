---
id: computing-software.database-administration.supabase.realtime-limits
name: realtime-limits
category: computing-software
field: database-administration
product: supabase
tags: [realtime, limits, quotas, too-many-joins, tenant-events]
level: practitioner
status: docs-checked
description: "Supabase Realtime plan limits for connections, messages per second, payload sizes and presence, plus the error codes when limits are hit."
sources:
  - https://supabase.com/docs/guides/realtime/limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size a Realtime workload and diagnose limit errors.

Per plan (Free / Pro / Pro without spend cap and Team / Enterprise):
- Concurrent connections: 200 / 500 / 10,000 / 10,000+.
- Messages per second: 100 / 500 / 2,500 / 2,500+.
- Channel joins per second: 100 / 500 / 2,500 / 2,500+.
- Presence messages per second: 20 / 50 / 1,000 / 1,000+.
- Broadcast payload: 256 KB on Free, 3,000 KB on Pro, Pro without spend cap and Team, 3,000+ KB on Enterprise.

Identical on Free, Pro, Pro without spend cap and Team (Enterprise shows a plus sign on the first three): 100 channels per connection (Enterprise 100+), 10 presence keys per object (Enterprise 10+), Postgres change payload 1,024 KB (Enterprise 1,024+ KB). Also the same everywhere, with no plus sign: 5 presence calls per client per 30 seconds, broadcast replay retention 72 hours, and 25 replay messages per request.

Rules:
- Upgrading raises limits; some still apply without a spend cap or on Enterprise to protect budgets.
- The page says both that all limits are configurable per project and that beyond the Free and Pro plans you can customise limits by contacting support; either way, contact support to raise them.
- Exceeding a limit shows errors in the Realtime logs and in WebSocket messages visible in browser developer tools.
- Join refusals: `too_many_channels` (too many on one connection), `too_many_connections` (too many for the project), `too_many_joins` (too many per second).
- Too many messages per second disconnects with `tenant_events` (an event is a WebSocket message delivered to or sent from a client); supabase-js reconnects automatically when throughput drops below the plan limit.
- When the Postgres change payload limit is hit, `new` and `old` records include only fields of 64 bytes or smaller.
- The Realtime Inspector can reproduce an error and share connection details with support.

## Checked

2026-11-04: Read the Realtime Limits page in full and compared every table cell. Corrected the "same on every plan" line, since the Enterprise column shows plus signs on channels, presence keys and Postgres change payload size. Reworded the customisation rule because the page states two versions of it, and added the page's definition of an event.
Method: documentation only; no commands were run.
