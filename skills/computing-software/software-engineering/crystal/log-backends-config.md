---
id: computing-software.software-engineering.crystal.log-backends-config
name: log-backends-config
category: computing-software
field: software-engineering
product: crystal
tags: [log-backends-config, log, log-setup, log-backend, io-backend, log-formatter, log-level, setup-from-env, dispatcher, json-logs, syslog, crystal]
level: practitioner
status: docs-checked
description: "Configure logging with Log.setup or Log.setup_from_env, choose IOBackend, custom formatters, JSON output and async dispatch."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log.setup, backends and LOG_LEVEL

Goal: route logs.

- Env: `Log.setup_from_env` reads `LOG_LEVEL` (`debug`, `info`, ...) and its `default_sources:` and `default_level:` arguments for the rest.
- Code: `Log.setup do |c| c.bind "*", :info, Log::IOBackend.new(STDERR); c.bind "myapp.db", :debug, other_backend end` or `Log.setup(:debug)` for a default.
- Custom formatter: `Log::IOBackend.new(formatter: Log::ShortFormat)` or `Log::Formatter.new { |entry, io| ... }` using `entry.severity`, `entry.message`, `entry.timestamp`, `entry.data`.
- Dispatch modes: `Log::DispatchMode::Sync`, `::Async` (the `IOBackend` default on most targets), `::Direct`.
- JSON lines: `Log::Metadata` implements `to_json`, so a formatter proc `Log::Formatter.new { |entry, io| ... }` can write a JSON line from `entry.severity`, `entry.message` and `entry.data`; `Log::MemoryBackend` for tests.

Gotchas:
- The log builder is closed in an `at_exit` handler, which flushes the backends.
- Calling `Log.setup` replaces earlier bindings.
- Sources not matched by any binding go nowhere.

Verify: `LOG_LEVEL=debug ./app` shows debug records.

## Checked

Date 2026-11-03. Confirmed in the Log source: Log.setup (block, level and backend, sources string forms, discarding previous bindings), Log.setup_from_env reading LOG_LEVEL with default_level, default_sources and log_level_env parameters, Log::IOBackend with formatter and dispatcher parameters (Async default except on wasm32), Log::ShortFormat, Log::DispatchMode Sync, Async and Direct, Log::MemoryBackend, bind(source, level, backend), and the at_exit builder close. Removed CRYSTAL_LOG_SOURCES (not read by setup_from_env).

Method: documentation only; no commands were run.
