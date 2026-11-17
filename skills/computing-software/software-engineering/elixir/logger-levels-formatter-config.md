---
id: computing-software.software-engineering.elixir.logger-levels-formatter-config
name: logger-levels-formatter-config
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, logger, log-level, logger-info, logger-metadata, logger-formatter, compile-time-purge, logger-handlers, logger-config, elixir-logging]
level: practitioner
status: docs-checked
description: "Configure Logger levels, formatter and metadata, use macros with lazy messages and understand the Erlang :logger handlers underneath."
sources: ["https://hexdocs.pm/logger/Logger.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logger levels, backends and formatting

**Goal:** useful, structured, low-noise logs.

```elixir
require Logger
Logger.info("order placed", order_id: id)               # metadata as keyword
Logger.error(fn -> "expensive #{inspect(big)}" end)     # lazy: only evaluated if the level is enabled
Logger.warning("slow")
Logger.metadata(request_id: rid)                        # per-process metadata
# config/config.exs
config :logger, :default_formatter, format: "[$level] $message $metadata\n", metadata: [:request_id, :order_id]
config :logger, level: :info
Logger.configure(level: :debug)                          # change at runtime
```

## Rules
- Levels from least to most severe: debug, info, notice, warning, error, critical, alert, emergency. A configured level passes that level and everything above it to the handlers.
- `Logger` calls are macros: `require Logger` first. Their arguments are only evaluated if the current level requires it (except `bare_log/3`), including the function form `Logger.info(fn -> ... end)`.
- Metadata can be set per process with `Logger.metadata/1`; `:mfa`, `:file` and `:line` are added automatically by the macros.
- Never log secrets or personal data.
- Before Elixir 1.15 custom logging used Logger backends; the `:console` backend configuration now maps to the default handler and `:default_formatter` (all console options except `:level` go under `:default_formatter`).

## Self-check
Log with metadata and confirm it appears using the configured format.

## Checked
2026-11-03: confirmed against the Elixir Logger docs (level list and filtering, lazy arguments, `Logger.metadata/1`, `:default_formatter` config with `format` and `metadata`, `Logger.configure/1`, backend-to-handler change in 1.15). Removed: the JSON-library and Phoenix/Ecto redaction advice, the `:warn` deprecation comment and the production level recommendation (not in the Logger docs).
Method: documentation only; no commands were run.
