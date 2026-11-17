---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-context-and-time-filters
name: argo-events-sensor-context-and-time-filters
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, context-filter, time-filter, timezone, cloudevents, window]
level: practitioner
status: docs-checked
description: "Filter on CloudEvent context fields and on time windows, including timezone support and windows crossing midnight."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/time.md", "https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/ctx.md", "https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/intro.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor context and time filters

Context filter: matches the CloudEvent `context` (type, subject, source, datacontenttype). id, specversion and time may appear in the YAML but are ignored in filtering. The docs note that filtering on `datacontenttype`, `source` and `subject` could be useless because they currently come fixed from the event source: `datacontenttype` is always `application/json`, `source` corresponds to the `eventSourceName` and `subject` to the `eventName` in the Sensor manifest.

```yaml
filters:
  context:
    source: custom-webhook
```

Time filter: keeps only events whose context time falls within a range.

```yaml
filters:
  time:
    start: "09:00:00"
    stop: "17:00:00"
    timezone: "America/New_York"   # optional, IANA name, default UTC
```

`start` and `stop` use `HH:MM:SS`. With a `timezone` the window follows daylight saving changes. `start` is inclusive and `stop` exclusive. If `start` < `stop` the event time must lie in `[start, stop)`. If `stop` < `start` the stop is treated as the next day, i.e. `[00:00:00, stop) || [start, 24:00:00)`: for example start 22:00 and stop 06:00 covers overnight.

The Filters introduction page gives the evaluation order of filter types as expr, data, context, time.

## Checked

2026-11-04. Confirmed against the Time Filter, Context Filter and Filters Introduction pages: context fields and ignored fields, the fixed values note, the `source: custom-webhook` example, time filter fields with `HH:MM:SS`, IANA timezone names with daylight saving, UTC default, inclusive start and exclusive stop, the next-day rule when stop < start, and the evaluation order. Reworded the fixed-values sentence to match the page; the overnight example (22:00 to 06:00) is an illustration of the stated rule.
Method: documentation only; no commands were run.
