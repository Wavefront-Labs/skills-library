---
id: computing-software.networking-hardware-and-wireless.apache-httpd.access-logging-logformat
name: access-logging-logformat
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, logging, logformat, customlog, mod-log-config, conditional-logging, access-log]
level: practitioner
status: docs-checked
description: "Define access logs with LogFormat and CustomLog: common and combined formats, format tokens, status modifiers, conditional logging with env= and expr=."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_log_config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access logging with LogFormat and CustomLog
```apache
LogFormat "%h %l %u %t \"%r\" %>s %b" common
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined
CustomLog "logs/access_log" combined
```
A `LogFormat` that defines a nickname only defines it; with a single argument it sets the format used by later `TransferLog` lines. `TransferLog` uses the last unnamed format and no conditions. `GlobalLog` (2.4.19+) is not valid in vhost context. `BufferedLogs On` batches writes; a crash may lose data.

## Tokens
| Token | Meaning |
|---|---|
| `%h` `%u` `%t` `%r` | host, user, time, request line |
| `%>s` | final status |
| `%b` / `%B` | bytes (`-` for zero / always number) |
| `%{X}i` `%{X}o` `%{X}e` | request header, response header, env |
| `%D` / `%T` | microseconds / seconds |
| `%X` | `X` aborted, `+` keep-alive, `-` closed |
| `%I` `%O` `%S` | bytes in, out, total (mod_logio) |

Modifiers: `%400,501{User-agent}i` logs only for those codes; `%!200,304,302{Referer}i` for all others.

## Conditional
```apache
SetEnvIf Request_URI \.gif$ gif-image
CustomLog "gif-requests.log" common env=gif-image
CustomLog "nongif-requests.log" common env=!gif-image
CustomLog logs/errors.log common "expr=%{REQUEST_STATUS} >= 400"
```

## Security
Non-printable characters are written as `\xhh`. Log directories must not be writable by anyone other than the user that starts the server.

## Checked

2026-11-08. Format tokens, status modifiers, nickname behaviour, TransferLog, GlobalLog (2.4.19 and later, not valid in vhost context), BufferedLogs, env= and expr= conditions and the escaping note confirmed against the full mod_log_config page; the REQUEST_STATUS expr example confirmed on the ap_expr page. Corrected the nickname wording and the negated-codes example, and removed the unread env.html source.

Method: documentation only; no commands were run.
