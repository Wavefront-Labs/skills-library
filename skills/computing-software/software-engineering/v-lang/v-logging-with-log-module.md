---
id: computing-software.software-engineering.v-lang.v-logging-with-log-module
name: v-logging-with-log-module
category: computing-software
field: software-engineering
product: v-lang
tags: [v-logging-with-log-module, standard-library-misc, log, logging, log.log, log levels, info, warn, error, debug, logger, v-lang]
level: practitioner
status: docs-checked
description: "Use log.Log levels, set output to file or stderr, structured-ish messages and global logger helpers."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging with the log module

Goal: leveled logs.

- `import log`; `mut l := log.Log{}`; `l.set_level(.info)`; `l.set_output_label('app')`; `l.info('started')`, `l.warn(...)`, `l.error(...)`, `l.debug(...)`; `l.fatal(msg)` ends in a `panic`.
- File output: `l.set_full_logpath('app.log')`, `l.log_to_console_too()`.
- Global helpers: `log.info('msg')`, `log.set_level(.debug)`, `log.set_logger(l)`, `log.set_always_flush(true)`.
- Include fields manually: `l.info('user=${id} action=login')`.
- Level from env: `log.level_from_tag(os.getenv('LOG_LEVEL'))` returns `?Level`.
- File based loggers: `l.flush()` and `l.close()`; `l.set_always_flush(true)` flushes on every message.

Gotchas:
- Avoid logging secrets.

Verify: set level warn and confirm info lines are suppressed.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: Log methods set_level, set_output_label, set_full_logpath, log_to_console_too, flush, close, set_always_flush, info/warn/error/debug/fatal (vlib/log/log.v), the global info/set_level/set_logger/set_always_flush (vlib/log/default.v), level_from_tag (vlib/log/common.v). The fatal doc says it performs a panic at the end.
Removed or corrected: 'fatal exits' (it panics), '(confirm)' markers, and the unverified thread-safety claim.
Method: documentation only; no commands were run.
