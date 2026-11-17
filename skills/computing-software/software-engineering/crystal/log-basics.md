---
id: computing-software.software-engineering.crystal.log-basics
name: log-basics
category: computing-software
field: software-engineering
product: crystal
tags: [log-basics, log, logging, severity, log-info, log-error, log-context, metadata, log-source, debug, crystal]
level: practitioner
status: draft
description: "Create named Log sources, log at trace to fatal levels with blocks and exceptions, and use Log::Context metadata."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log basics and severities

Goal: structured logging.

```crystal
Log = ::Log.for("myapp.db")
Log.info { "connected" }
Log.error(exception: ex) { "query failed" }
Log.with_context(user_id: 5) { Log.warn { "slow" } }
```
- Severities: trace, debug, info, notice, warn, error, fatal. Block form avoids building the message when disabled.
- Hierarchy by dotted source name; configuration applies to prefixes (`myapp.*`).
- `Log::Context` carries key/value data per fiber; `Log.context.set(a: 1)`.
- Define one `Log = ::Log.for(self)` per class/module for the type's name as source.

Gotchas:
- The constant name `Log` inside a namespace shadows `::Log`; refer to `::Log` explicitly.
- Exceptions need `exception:` to include backtraces.
- Default level when unconfigured is Info (confirm), so debug is hidden.

Verify: set `LOG_LEVEL=debug` and see debug lines.
