---
id: computing-software.game-programming.game-engine-architecture.logging-channels-and-verbosity
name: logging-channels-and-verbosity
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, engine-support, logging-system, log-channels, verbosity, compile-time-stripping, spdlog, game-programming]
level: practitioner
status: docs-checked
description: "Design an engine logging system with channels, runtime and compile-time verbosity, async sinks, backtrace buffers and flushing, using spdlog features as the reference."
sources: ["https://github.com/gabime/spdlog"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging channels and verbosity

A custom C++ engine can build its logging on spdlog or copy its feature set. Features below are
from the spdlog README.

## Levels: runtime and compile time
- Log levels can be changed at runtime and at compile time. `spdlog::set_level(...)` sets the
  global level, `logger->set_level(...)` a single logger, and a sink can have its own level and
  pattern.
- Compile-time levels: the `SPDLOG_TRACE(...)`, `SPDLOG_DEBUG(...)` macros remove the call from
  release code depending on `SPDLOG_ACTIVE_LEVEL`. This does not change the current runtime
  level.
- Channels: use one named logger per subsystem (AI, net, physics, audio) so one can be raised
  without drowning the others (own design advice; spdlog loggers have names).

## Sinks
- Console (colour, multi-threaded `_mt` variants), basic file, rotating files (the README example
  uses 5 MB max size and 3 rotated files), daily files, callback sinks, and custom sinks.
- A logger can have several sinks, each with its own format and level, for example console at
  warn and file at trace.
- Use `_mt` loggers when more than one thread logs.

## Async logging
Optional asynchronous mode (`spdlog/async.h`) with a thread pool; the pool size can be set
before creating the async logger, for example `init_thread_pool(8192, 1)` for an 8k-item queue and
one backing thread.

## Backtrace and flushing
- `enable_backtrace(32)` stores the latest 32 messages in a ring buffer without logging them;
  `dump_backtrace()` logs them on demand. Use it to attach recent context to an error or crash
  report.
- `flush_every(std::chrono::seconds(3))` flushes all registered loggers periodically; the README
  warns to use it only if all loggers are thread-safe (`_mt`).
- Flush on error and in the crash handler so the last lines survive (own advice; with async
  sinks the final lines are the ones you need).

## Verify
- [ ] Release builds define SPDLOG_ACTIVE_LEVEL so verbose macros compile out.
- [ ] Raising one logger at runtime does not change the others.
- [ ] A forced crash leaves the final log lines on disk.

## Checked
Method: docs-checked 2026-11-09 against the spdlog README on GitHub (features list, compile-time levels, rotating, multi-sink, backtrace, periodic flush and async sections; downloaded). Removed the Unreal and Unity command details, the custom macro sketch and gameenginebook.com landing page source (not verified).
