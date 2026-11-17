---
id: computing-software.web-development.vapor.vapor-logging-levels-handlers
name: vapor-logging-levels-handlers
category: computing-software
field: web-development
product: vapor
tags: [vapor,vapor-logging,log-level,swiftlog,logger,logging,swift]
level: practitioner
status: docs-checked
description: "Log in Vapor with req.logger, app.logger and Logger(label:), set levels via --log or LOG_LEVEL, and bootstrap a custom SwiftLog handler."
sources:
  - https://docs.vapor.codes/basics/logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: log with the right logger and level, and configure the backend.

Vapor logging is built on SwiftLog, so any SwiftLog backend works.

## Which logger
- Per request: `req.logger.info("Hello, logs!")`; it carries a unique request-id (metadata shows only at debug level or lower).
- During boot/configuration: `app.logger.info("Setting up migrations...")`.
- Elsewhere: `Logger(label: "dev.logger.my")`; it reaches your backend but lacks metadata such as the request UUID. Prefer request/app loggers.

## Levels
trace, debug, info, notice, warning, error, critical. A `critical` message lets the backend capture heavier state (e.g. stack traces). Default is `info`; the `production` environment uses `notice`.

## Change level
```sh
swift run App serve --log debug
```
```sh
export LOG_LEVEL=debug
swift run App serve
```
Both can be set in Xcode via the `App` scheme.

## Configure the backend
Bootstrap `LoggingSystem` once per process, typically in `entrypoint.swift`:
```swift
var env = try Environment.detect()
try LoggingSystem.bootstrap(from: &env)
```
This helper configures the default handler from CLI args and env variables (terminal output with ANSI colour).

Custom handler:
```swift
import Logging

LoggingSystem.bootstrap { label in
    StreamLogHandler.standardOutput(label: label)
}
```
Gotcha: `--log` and `LOG_LEVEL` only work with Vapor's default handler.

## Checked

2026-11-08: read in full the Logging page at docs.vapor.codes/basics/logging/ (loggers, levels, --log and LOG_LEVEL, bootstrap, custom handler). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
