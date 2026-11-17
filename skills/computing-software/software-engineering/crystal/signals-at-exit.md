---
id: computing-software.software-engineering.crystal.signals-at-exit
name: signals-at-exit
category: computing-software
field: software-engineering
product: crystal
tags: [signals-at-exit, process-system, signal, sigint, sigterm, trap, at-exit, graceful-shutdown, exit, abort, sighup, crystal]
level: practitioner
status: draft
description: "Trap SIGINT and SIGTERM with Signal.trap, run at_exit handlers and shut down servers and fibers gracefully."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signals, at_exit and graceful shutdown

Goal: stop cleanly.

```crystal
Signal::INT.trap { server.close; exit }
Signal::TERM.trap { server.close }
at_exit { |status, ex| flush_logs }
```
- Handlers run in a fiber (not in the raw signal context), so normal Crystal code is fine in them.
- `exit(code)` runs `at_exit` handlers; `exit!`/`Process.exit` variants skip them (confirm); `abort("msg", 1)` prints to stderr and exits.
- Reset: `Signal::INT.reset`, ignore: `Signal::PIPE.ignore`.
- Pattern: main waits on a `Channel(Nil)` closed by the signal handler; workers drain then exit.
- Containers send SIGTERM; make it the shutdown path.

Gotchas:
- SIGKILL and SIGSTOP cannot be trapped.
- Windows supports a smaller signal set.
- `at_exit` handlers run in reverse registration order.

Verify: send `kill -TERM` and see the cleanup message.
