---
id: computing-software.cloud-infrastructure-engineering.vector.lua-transform
name: lua-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [lua, transform, hooks, timers, scripting, event-model, vector]
level: advanced
status: docs-checked
description: "Run Lua hooks for stateful logic Remap cannot express, mapping Vector types to Lua tables."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/lua/
  - https://vector.dev/docs/reference/configuration/transforms/remap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `lua` transform runs Lua code. It is stateful and state is lost on restart. The remap reference describes VRL as a restrictive, fast and safe language, so prefer `remap` unless you need state across events or timers.

```yaml
transforms:
  count:
    type: lua
    inputs: [logs]
    version: "2"
    hooks:
      init: |
        function (emit) count = 0 end
      process: |
        function (event, emit)
          count = count + 1
          emit(event)
        end
    timers:
      - interval_seconds: 5
        handler: |
          function (emit) end
```

The reference defines these options: `version` (the transform API version), `source` (code to load modules and define functions), `hooks.init` (runs when the first event arrives), `hooks.process` (per event), `hooks.shutdown`, `timers` (a handler plus `interval_seconds`) and `search_dirs` (for `require`; defaults to the config directories). Hooks can produce new events with `emit`.

Type mapping: strings, integers, floats and booleans map directly. Timestamps are tables with fields like year, month, day, hour, min, sec and nanosec. Null becomes an empty string, because setting a Lua table field to nil deletes it. Maps are tables and arrays are sequences indexed from 1.

Version 1 of the transform API is deprecated and will be removed; use version 2. Logs and metrics are both supported as input. Check the reference for the event layout before reading or writing fields in a hook.

Verify with a unit test around the transform.

## Checked

2026-11-03. Read transforms/lua and transforms/remap. Confirmed: stateful, logs and metrics input, `version` 1 deprecated, `hooks.init` runs when the first event comes in, `hooks.process`, `hooks.shutdown`, `timers` with `interval_seconds`, `search_dirs`, `emit`, and the type-mapping table (timestamps as tables, null as empty string, arrays indexed from 1). The VRL fast-and-safe wording comes from the remap page. Nothing removed.

Method: documentation only; no commands were run.
