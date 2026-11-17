---
id: computing-software.software-engineering.erlang.logger-api
name: logger-api
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-logging, logger-api]
level: practitioner
status: docs-checked
description: "Erlang logger: level macros, structured reports, primary level, module levels and process metadata."
sources:
  - https://www.erlang.org/doc/apps/kernel/logger.html
  - https://www.erlang.org/doc/apps/kernel/logger_chapter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logger API, levels and metadata
**Goal:** emit useful structured logs.

```erlang
-include_lib("kernel/include/logger.hrl").
?LOG_INFO("started on port ~p", [Port]),
?LOG_ERROR(#{what => db_failed, reason => Reason}),
logger:set_primary_config(level, info),
logger:set_module_level(my_noisy_mod, warning),
logger:update_process_metadata(#{request_id => Id}).
```
- Levels: emergency, alert, critical, error, warning, notice, info, debug. Events less severe than the primary level are immediately discarded.
- The macros add location (originator) information to the metadata; the exported functions such as `logger:info/2` do not.
- The macros wrap the call in a case so it is only evaluated if the event passes the primary level check (lazy evaluation).
- A map or report can be given instead of a format string; formatters decide how it is rendered.
- Supervisor and crash reports are issued as `error` level log events through the default handler.

## Gotchas
- Calling `logger:info/2` directly evaluates its arguments even when the level is disabled; use the macros in hot paths.

## Self-check
Set the level to debug at runtime and watch debug lines appear.

## Checked

2026-11-03. Confirmed in the `logger` module page and the Logger chapter: level list, macros versus functions (location metadata, lazy evaluation), `set_primary_config(level, Level)`, `set_module_level/2`, `update_process_metadata/1`, and supervisor/crash reports logged at error level.
Method: documentation only; no commands were run.
