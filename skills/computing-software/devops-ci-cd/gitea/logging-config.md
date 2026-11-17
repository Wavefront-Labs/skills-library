---
id: computing-software.devops-ci-cd.gitea.logging-config
name: logging-config
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-log-writers, gitea, log-mode, logger-access-mode, access-log-template, logrotate, release-and-reopen, log-flags]
level: advanced
status: docs-checked
description: "Configure Gitea logging: [log] MODE and LEVEL, [log.<name>] writers (console, file, conn), router/access/xorm loggers, flags, rotation and logrotate with SIGUSR1."
sources: ["https://docs.gitea.com/administration/logging-config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea logging configuration

Defaults work without any config. Structure: `[log]` (global), `[log.<name>]` writer sections (name defaults to the writer `MODE`), and sub-loggers `logger.<router|access|xorm>.MODE` inside `[log]`.

## [log] keys
`ROOT_PATH` (default `%(GITEA_WORK_DIR)/log`), `MODE` (default `console`), `LEVEL` (default Info; Trace, Debug, Info, Warn, Error, Fatal), `STACKTRACE_LEVEL` (default None). Sub-logger modes: `logger.router.MODE` and `logger.xorm.MODE` default `,` (a comma means use the global MODE), `logger.access.MODE` defaults empty (access log disabled).

Examples:
```ini
[log]
LEVEL = Warn
MODE = file, file-error

[log.file-error]
MODE = file
LEVEL = Error
FILE_NAME = file-error.log
```
```ini
[log]
logger.router.MODE =
logger.access.MODE = access-file

[log.access-file]
MODE = file
LEVEL = Warn
FILE_NAME = access.log
```
Careful: the access logger logs at INFO, so setting its writer LEVEL to Warn or higher means no access logs appear (the docs sample uses Warn, so check your level choice).

## Writers
Common: `MODE`, `LEVEL`, `STACKTRACE_LEVEL`, `COLORIZE` (true only for console), `EXPRESSION` (regexp matched against the message or `longfilename:line:funcname`, evaluated in the writer goroutine), `FLAGS` (default `stdflags` = `date,time,medfile,shortfuncname,levelinitial`; others `none`, `microseconds`, `longfile`, `shortfile`, `funcname`, `utc`, `level`, `gopid`).
- console: `STDERR` (false).
- file: `FILE_NAME` (default `gitea.log`, access log `access.log`, relative to `ROOT_PATH`), `MAX_SIZE_SHIFT` 28 (1<<28 = 256 MB), `LOG_ROTATE` true, `DAILY_ROTATE` true, `MAX_DAYS` 7, `COMPRESS` true (gzip), `COMPRESSION_LEVEL` -1 (1 fastest to 9 best, -2 Huffman only).
- conn: `ADDR` `:7020`, `PROTOCOL` tcp|unix|udp, `RECONNECT`, `RECONNECT_ON_MSG`.

## Special loggers
Router: started at TRACE, polling/completed at INFO (`/assets` at TRACE), slow and failed at WARN. XORM SQL output also needs `LOG_SQL = true` in `[database]`. Access log (since 1.9) is NCSA common format; customise with `ACCESS_LOG_TEMPLATE` (Go template with `Ctx`, `Identity`, `Start`, `ResponseWriter`), keep it simple because it runs on every request outside panic recovery.

## Rotation and runtime control
Send `SIGUSR1` or run `gitea manager logging release-and-reopen` to make Gitea reopen files (needed with external logrotate: set `LOG_ROTATE = false`, and call it from `postrotate`; test with `logrotate /etc/logrotate.conf --debug`; Docker: `docker exec -u $OS_USER $CONTAINER sh -c 'gitea manager logging release-and-reopen'`). `manager logging pause/resume` should be brief: paused logging drops events below INFO, keeps only a limited number, and can block Gitea. `manager logging add/remove` can attach temporary loggers to a running server but cannot start router/access loggers that were not initialised; edit `app.ini` and restart for those.

## Checked

2026-11-03: read https://docs.gitea.com/administration/logging-config/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
