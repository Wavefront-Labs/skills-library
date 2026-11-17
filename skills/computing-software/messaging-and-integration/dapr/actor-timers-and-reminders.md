---
id: computing-software.messaging-and-integration.dapr.actor-timers-and-reminders
name: actor-timers-and-reminders
category: computing-software
field: messaging-and-integration
product: dapr
tags: [actors, timers, reminders, scheduler, duetime, period, ttl, iso8601, turn-based-concurrency]
level: practitioner
status: docs-checked
description: "Register Dapr actor timers and reminders over HTTP: dueTime, period, ttl formats, how they persist, and reminders stored in the Scheduler in v1.15."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/actors/actors-timers-reminders.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Actors schedule periodic work on themselves with timers or reminders. Both honour turn-based concurrency: no other method or callback runs on the actor until the callback finishes, and state is saved when it ends (a save error deactivates the actor and a new instance activates).

Difference: timers are not retained after the actor deactivates (all stop on garbage collection); reminders persist and fire until the actor unregisters them. In Dapr v1.15 reminders are stored in the Scheduler service by default, and existing ones migrate automatically with no loss.

Endpoints (POST or PUT to create, DELETE to remove; reminders also support GET):

```md
POST/PUT http://localhost:3500/v1.0/actors/<actorType>/<actorId>/timers/<name>
POST/PUT http://localhost:3500/v1.0/actors/<actorType>/<actorId>/reminders/<name>
```

Body fields, all optional:

- `dueTime`: first fire; RFC3339 date (`2020-10-02T15:00:00Z`), duration (`2h30m`) or ISO 8601 (`PT2H30M`). Omitted means fire immediately.
- `period`: interval; duration or ISO 8601, which also allows repetition counts such as `R5/PT1M30S`. Omitted means fire once.
- `ttl`: expiry date or interval after which it is deleted. Omitted means no limit.

If both a repetition count and `ttl` are set, it stops at whichever comes first. Invalid input returns an error.

Examples: `{"dueTime":"0h0m9s0ms","period":"0h0m3s0ms"}` fires after 9s then every 3s; `{"period":"R10/PT3S"}` fires 10 times; `{"dueTime":"10s","period":"R4/PT3S","ttl":"10s"}` is bounded by both.

## Checked

2026-11-04. Parameter formats, endpoints and examples confirmed on the Actors timers and reminders page.

Method: documentation only; no commands were run.
