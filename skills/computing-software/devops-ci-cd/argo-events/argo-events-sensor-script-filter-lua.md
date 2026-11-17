---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-script-filter-lua
name: argo-events-sensor-script-filter-lua
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, script-filter, lua, sensor, event-body]
level: advanced
status: docs-checked
description: "Filter events with a Lua script that returns true or false using the event table."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/script.md", "https://github.com/argoproj/argo-events/blob/master/docs/sensors/filters/intro.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor script filter lua

A script filter evaluates a Lua script against the event. It is set directly under `filters` as `script`:

```yaml
filters:
  script: |-
    if event.body.a == "b" and event.body.d.e == "z" then return true else return false end
```

The script works on the event `data` (header and body), exposed as `event`, so `event.body.a` reads the JSON body field `a`. The page's example script returns `true` or `false`.

Example from the docs: create the webhook EventSource and the sensor from `examples/sensors/filter-script.yaml`, port-forward `svc/webhook-eventsource-svc 12000`, then send `{"hello": "world"}` to `/example` and the sensor logs show nothing triggered. Send `{"a": "b", "d": {"e": "z"}}` and a workflow gets created.

Script is one of the five filter types listed on the Filters introduction page, where any kind of filter error counts as false.

## Checked

2026-11-04. Confirmed against the Script filter page (Lua, applied to event `data`, the `script` field under `filters`, the example script, and the practical example commands and outcomes) and the Filters Introduction page (five types, errors as false). Removed the "must return a boolean" rule, the claim about `filtersLogicalOperator` participation beyond the intro's general text, and the advice to prefer expr or data filters, none of which the Script page states.
Method: documentation only; no commands were run.
