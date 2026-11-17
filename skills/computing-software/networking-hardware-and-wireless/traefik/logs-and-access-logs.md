---
id: computing-software.networking-hardware-and-wireless.traefik.logs-and-access-logs
name: logs-and-access-logs
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, accesslog, log, json, filters, redact, bufferingsize]
level: practitioner
status: docs-checked
description: "Configure Traefik application logs and access logs, with format, file, filters and header redaction."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/observability/logs-and-accesslogs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logs and access logs
Application logs: `log.filePath`, `log.format` (common or json), `log.level` (default ERROR), `log.noColor` and rotation `maxSize`, `maxAge`, `maxBackups`. Access logs are off until you set `accesslog`: `filePath`, `dualOutput`, `format` (common, genericCLF or json), `bufferingSize`, `addInternals`, `filters` (`statusCodes`, `retryAttempts`, `minDuration`) and `fields` (`defaultMode`, `names`, `headers`, `queryParameters`).

```yaml
log:
  level: INFO
  format: json
accessLog:
  format: json
  filters:
    statusCodes: ["400-599"]
  fields:
    defaultMode: keep
    headers:
      defaultMode: drop
      names:
        Authorization: redact
```
Header modes are keep, drop and redact.

Gotchas: the default log level is ERROR (levels are TRACE, DEBUG, INFO, WARN, ERROR, FATAL and PANIC). By default logs and access logs go to standard output; when `filePath` is set Traefik writes only to that file. With OTLP logging enabled, access logs still go to stdio only if `accessLog.dualOutput` is set. Keeping the Authorization or cookie headers would write them to the log, so use `drop` or `redact` for them. `log.maxSize` defaults to 100MB, and `maxAge` and `maxBackups` default to 0, which keeps all old files.

## Checked
2026-11-03. Confirmed against the Traefik logs and access logs reference page: `log.*` options and defaults, `accessLog` options (`filePath`, `dualOutput`, `format`, `filters` with `statusCodes`, `retryAttempts`, `minDuration`, and `fields` modes keep, drop and redact) and the stdout default. Removed: the option-name casing hedge and the curl Verify step.
Method: documentation only; no commands were run.


