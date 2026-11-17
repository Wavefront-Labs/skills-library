---
id: computing-software.devops-ci-cd.forgejo.logging-filters-and-flags
name: logging-filters-and-flags
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [log-exclusion, log-expression, log-flags, healthz-logs]
level: advanced
status: docs-checked
description: "Filter log events with EXPRESSION and EXCLUSION regexes and control line prefixes with FLAGS."
sources:
  - https://forgejo.org/docs/latest/admin/troubleshooting/logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every log writer accepts common settings: `MODE` (defaults to the section name, so `[log.console]` implies console), `LEVEL`, `STACKTRACE_LEVEL` and `COLORIZE` (true for a terminal console, otherwise false).

`EXPRESSION` is a regular expression that events must match to be logged; either the colorless message or the `longfilename:linenumber:functionname` must match, and a partial match is enough. `EXCLUSION` is the opposite: events must not match. Both run in the writer's goroutine, not the logging goroutine. The page's example keeps router logs but drops health and metrics requests: in `[log.router]` with `MODE = console`, `LEVEL = INFO`, set `EXCLUSION = (\/api\/healthz|\/metrics)`.

`FLAGS` is a comma-separated set that selects the context printed before each message. It defaults to `stdflags`, equal to date, time, medfile, shortfuncname and levelinitial, except the access log, which defaults to none. Other values include none, microseconds, longfile, shortfile, funcname, utc, level (for example [INFO]), levelprefix (journald-style prefix such as <5>), gopid, and `journaldflags`, equal to levelprefix.

Under systemd the page recommends leaving the logging configuration at its defaults (`MODE = console`); `FLAGS` then defaults to `journaldflags` when the stream is connected to journald.

## Checked

2026-11-04. Confirmed against the Forgejo Logging Configuration page (Common configuration, EXPRESSION, EXCLUSION, FLAGS, journald mode). Replaced the Docker and systemd closing line with what the page says about systemd.

Method: documentation only; no commands were run.
