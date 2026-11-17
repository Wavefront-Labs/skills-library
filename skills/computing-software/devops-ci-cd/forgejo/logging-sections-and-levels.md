---
id: computing-software.devops-ci-cd.forgejo.logging-sections-and-levels
name: logging-sections-and-levels
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [log-config, log-modes, logger-access, log-level]
level: practitioner
status: docs-checked
description: "Configure Forgejo logging with the [log] section, per-mode writers and sub-logger modes."
sources:
  - https://forgejo.org/docs/latest/admin/troubleshooting/logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Logging uses three kinds of components: the `[log]` section, `[log.<mode-name>]` writer sections, and sub-logger keys. A working log output exists by default, so no configuration is required.

The `[log]` properties: `ROOT_PATH` (default AppWorkPath/log), `MODE` (default console), `LEVEL` (default Info; Trace, Debug, Info, Warn, Error, Fatal), and `STACKTRACE_LEVEL` (default None). Sub-loggers are set with `LOGGER_DEFAULT_MODE`, `LOGGER_ROUTER_MODE`, `LOGGER_XORM_MODE` and `LOGGER_ACCESS_MODE`. A comma `,` means "use the global MODE", and the access logger is disabled by default (empty).

Samples from the page: to disable router logs and write warnings and above of the access logger to a file, set `LOGGER_ROUTER_MODE =` empty, `LOGGER_ACCESS_MODE = access-file`, then define `[log.access-file]` with `MODE = file`, `LEVEL = Warn`, `FILE_NAME = access.log`. To keep Warn logs in forgejo.log and Error logs in a second file, use `MODE = file, file-error` and a `[log.file-error]` section with `LEVEL = Error` and `FILE_NAME = file-error.log`.

Writers include console, file and conn (a network or unix socket).

## Checked

2026-11-04. Confirmed against the Forgejo Logging Configuration page: the three component kinds, the [log] properties and defaults, sub-logger modes and the comma rule, both quick samples and the writer list. Nothing removed.

Method: documentation only; no commands were run.
