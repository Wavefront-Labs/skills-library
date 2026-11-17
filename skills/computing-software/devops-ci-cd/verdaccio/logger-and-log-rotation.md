---
id: computing-software.devops-ci-cd.verdaccio.logger-and-log-rotation
name: logger-and-log-rotation
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [logger, log-level, logrotate, log-config, pino, redaction, sigusr2]
level: practitioner
status: docs-checked
description: "Configure Verdaccio's log block (stdout or file, format, level, redact) and rotate log files with logrotate plus SIGUSR2, since the logger has no built-in rotation."
sources:
  - https://verdaccio.org/docs/logger/
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/uplinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
log: { type: stdout, format: pretty, level: http }
# or
log: { type: file, path: verdaccio.log, level: info }
```
Properties: `type` (stdout, file), `path` (for file), `format` (pretty, pretty-timestamped, json), `level` (fatal, error, warn, info, http, debug, trace), `colors` (false), `redact`, `sync` (true).

Gotchas:
- The old key `logs` still works but gives deprecation warning VERWAR002; use `log`.
- When `format` is unset it is `json` if `NODE_ENV=production`, otherwise `pretty`. Set it explicitly for identical output everywhere.
- There is no built-in rotation (dropped with pino). Use logrotate or your platform's equivalent, then send `SIGUSR2` so Verdaccio reopens the file.
- With `level: http`, outgoing tarball downloads log their target URL and uplink; refused off-uplink fetches log a warn.

Redaction masks sensitive fields:
```yaml
log:
  redact:
    paths: ['req.header.authorization', 'req.header.cookie', 'ip', 'user']
    censor: '<redacted>'
```
Verify: make a request and confirm the redacted fields show `<redacted>`.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Logger, Configuration (Logger) and Uplinks. Confirmed: the stdout and file examples, the property list, VERWAR002, the NODE_ENV format default, no built-in rotation with SIGUSR2, the redact example and the tarball logging at level http. Removed or corrected: nothing.

Method: documentation only; no commands were run.
