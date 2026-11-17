---
id: computing-software.messaging-and-integration.apache-camel.timer-component
name: timer-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, timer, scheduling, period]
level: intro
status: docs-checked
description: "Camel timer component: consumer-only, delay and period defaults of 1000 ms, fixedRate, repeatCount, shared timer by name, exchange properties and example URIs."
sources:
  - https://camel.apache.org/components/next/timer-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# timer:

Consumer only: `timer:name[?options]`. Endpoints with the same name share one Timer object and thread. The IN body is `null`. For advanced scheduling use Quartz.

Options (defaults):
- `delay` 1000 ms before the first event (negative fires immediately; do not combine with `time`)
- `period` 1000 ms (zero or positive)
- `fixedRate` false
- `repeatCount`: 1 fires once, zero or negative forever
- `daemon` true
- `synchronous` false
- `time` first event time, `yyyy-MM-dd HH:mm:ss` or `yyyy-MM-dd'T'HH:mm:ss`; `pattern` for a custom format
- `includeMetadata` false
- `bridgeErrorHandler` false
- `runLoggingLevel` TRACE

Exchange properties: `Exchange.TIMER_NAME`, `TIMER_TIME`, `TIMER_PERIOD`, `TIMER_FIRED_TIME`, `TIMER_COUNTER` (starts at 1). Headers: `CamelTimerFiredTime`, `CamelMessageTimestamp`. The `includeMetadata` option (default false) is described as adding the properties `CamelTimerCounter`, `CamelTimerName`, `CamelTimerPeriod`, `CamelTimerFiredTime`, `CamelTimerTime` and those two headers.

Examples:
- `timer://foo?fixedRate=true&period=60000` every 60 seconds
- `timer://foo?delay=-1` fires immediately and continues until the route stops
- `timer://foo?repeatCount=1` once, e.g. at route startup

Verify: `repeatCount` is a maximum number of fires (the page: 5 fires five times), so `timer:foo?period=1000&repeatCount=3` should stop after three fires, with the counter starting at 1.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel timer component page: defaults (delay 1000, period 1000, fixedRate false, daemon true, synchronous false, includeMetadata false, bridgeErrorHandler false, runLoggingLevel TRACE), repeatCount semantics, time formats, exchange properties, headers and examples all match. The old claim that a run "fires exactly three times with counter 1, 2, 3" was reworded to what the page states. No commands were run.
