---
id: computing-software.software-engineering.wails.wails-runtime-logging
name: wails-runtime-logging
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, runtime, logging, logger]
level: practitioner
status: docs-checked
description: "Log from Go or JS with the Wails runtime, set the log level, and plug in a custom logger through options.App Logger, LogLevel and LogLevelProduction."
sources: [https://wails.io/docs/reference/runtime/log, https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails runtime logging

Goal: write log messages from Go or JavaScript and control verbosity.

## Levels

Trace, Debug, Info, Warning, Error, Fatal. The logger outputs messages at the current level or higher (Debug level prints everything except Trace).

## Calls

Go takes `ctx` first. Plain forms: `LogPrint`, `LogTrace`, `LogDebug`, `LogInfo`, `LogWarning`, `LogError`, `LogFatal` (message string; JS has the same names with `(message)`). Go also has formatted variants taking `format string, args ...interface{}`: `LogPrintf`, `LogTracef`, `LogDebugf`, `LogInfof`, `LogWarningf`, `LogErrorf`, `LogFatalf` (not in JS).

`LogSetLogLevel(ctx, level logger.LogLevel)` in Go. In JS, `LogSetLogLevel(level: number)` with 1 Trace, 2 Debug, 3 Info, 4 Warning, 5 Error.

## App options

- `Logger` (`logger.Logger`): default logs to stdout.
- `LogLevel`: default `Info` in dev, `Error` in production.
- `LogLevelProduction`: default `Error`.

## Custom logger

Provide any value implementing `logger.Logger` (package `github.com/wailsapp/wails/v2/pkg/logger`) via the `Logger` option:

```go
type Logger interface {
	Print(message string)
	Trace(message string)
	Debug(message string)
	Info(message string)
	Warning(message string)
	Error(message string)
	Fatal(message string)
}
```

## Checked

2026-11-07. Read the whole runtime Log reference page (website/docs/reference/runtime/log.mdx: levels, every Log* and Log*f entry, LogSetLogLevel numeric table, custom Logger interface) and the Logger, LogLevel and LogLevelProduction sections of the Options reference page (website/docs/reference/options.mdx). Confirmed that the formatted variants are Go-only, that JS LogSetLogLevel numbers run 1 to 5 (Trace to Error), and the log-level defaults. No claims were trimmed.

Method: documentation only; no commands were run.
