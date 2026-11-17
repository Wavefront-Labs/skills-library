---
id: computing-software.networking-hardware-and-wireless.apache-httpd.error-log-and-loglevel
name: error-log-and-loglevel
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, logging, errorlog, loglevel, errorlogformat, per-module-logging, debugging]
level: practitioner
status: docs-checked
description: "Read and tune the error log: ErrorLog, per-module LogLevel such as rewrite:trace5, ErrorLogFormat, the 2.4 level changes, and correlating with access logs."
sources:
  - https://httpd.apache.org/docs/2.4/logs.html
  - https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error log and LogLevel
The error log is the first place to look when the server fails to start or misbehaves.

```
[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] AH00124: Request exceeded the limit of 10 internal redirects due to probable configuration error
```
Fields: timestamp, module:severity, process/thread, client, message. `ErrorLogFormat` selects the fields.

## Per-module levels
```apache
LogLevel info rewrite:trace5
```
Global `info` with `mod_rewrite` at `trace5`. This replaces `RewriteLog`. Rewrite levels run `trace1` to `trace8`; above `trace2` is very slow.
```apache
LogLevel alert rewrite:trace3
```
Filter with `tail -f error_log | fgrep '[rewrite:'`.

## Level changes
Some messages, such as 404 File does not exist, dropped from `error` to `info` in 2.4. Restore with:
```apache
LogLevel warn core:info
```

## Correlation
`%L` in both error and access log formats yields a log entry ID.

## Checked

2026-11-08. Error log format and fields, 2.4 downgrade of File does not exist, LogLevel warn core:info, per-module LogLevel, %L correlation confirmed on the full logs page; trace1 to trace8, slowdown above trace2 and RewriteLog replacement confirmed on the mod_rewrite page. Removed the httpd -e / -E startup line, which no cited page covers.

Method: documentation only; no commands were run.
