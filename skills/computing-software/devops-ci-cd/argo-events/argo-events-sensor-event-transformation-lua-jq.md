---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-event-transformation-lua-jq
name: argo-events-sensor-event-transformation-lua-jq
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, transform, lua, jq, gojq, sensor, event-data]
level: advanced
status: docs-checked
description: "Rewrite event data before filters run, using a Lua script or a JQ command, including how to emit empty JSON arrays from Lua."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/transform.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor event transformation lua jq

Event transformation is available after v1.6.0 and is configured per dependency under `transform`. Rules:
- The transformation runs before filters.
- Use a Lua script or a JQ command, not both.
- Only event data is available, not the context.
- The event is discarded if the transformation fails.
- The output must be a valid JSON object.

Lua: the event data is the global table `event`, and the script must return a table.

```yaml
dependencies:
  - name: test-dep
    eventSourceName: webhook
    eventName: example
    transform:
      script: |-
        event.body.message='updated'
        return event
```

Empty Lua tables serialize as `{}`, not `[]`. To output an empty array use the metatable flag:

```lua
event.env = setmetatable({}, { __is_array = true })
return event
```

This matters for Kubernetes fields like `env` that require arrays.

JQ (evaluated with gojq):

```yaml
transform:
  jq: ".body.message *= 2"
```

The page says this appends the value of `.body.message` to itself. In the page's samples the transformed data then feeds trigger parameters, e.g. `src.dependencyName: test-dep`, `dataKey: body`, `dest: spec.arguments.parameters.0.value`.

## Checked

2026-11-04. Confirmed against the Event Transformation page: available after v1.6.0, the four notes (runs before filters, Lua or JQ not both, event data only, discarded on failure), the Lua `event` global and Table return, the `__is_array` metatable for empty arrays, gojq, `.body.message *= 2`, the JSON object output requirement and the trigger parameter sample. Nothing removed.
Method: documentation only; no commands were run.
