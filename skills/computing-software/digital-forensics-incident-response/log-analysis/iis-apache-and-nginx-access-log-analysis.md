---
id: computing-software.digital-forensics-incident-response.log-analysis.iis-apache-and-nginx-access-log-analysis
name: iis-apache-and-nginx-access-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [apache-logs, nginx-logs, web-server-logs, log-analysis, dfir]
level: practitioner
status: docs-checked
description: "Read W3C (HTTP Server API), Apache and nginx access logs for intrusions: field meanings, time zones, buffering, conditional logging and log-injection traps."
sources: ["https://learn.microsoft.com/en-us/windows/win32/http/w3c-logging", "https://httpd.apache.org/docs/current/logs.html", "https://nginx.org/en/docs/http/ngx_http_log_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS-style W3C, Apache and nginx access logs

**Goal:** interpret web server access logs correctly before using them to tie requests to an attacker and to a compromise.

## W3C extended logs (HTTP Server API, as used by IIS-style logging)
- Fields are listed in the `#Fields:` header line and separated by spaces. Always read the header of each file: the field set is customisable and fields vary between files.
- Prefixes: `s` server, `c` client, `sc` server-to-client, `cs` client-to-server.
- The `time` field is in UTC. Useful fields: `c-ip`, `cs-username` (hyphen for anonymous), `cs-method`, `cs-uri-stem`, `cs-uri-query`, `sc-status`, `sc-substatus`, `sc-win32-status`, `sc-bytes`, `cs-bytes`, `cs(User-Agent)`, `cs(Referrer)`, `cs-host`, `time-taken`.
- A hyphen is a placeholder for a selected field with no value. Non-printable characters are replaced with `+`, which the page says typically happens with attacks that send carriage returns or line feeds.
- `time-taken` runs from the first byte received to the last send completion and excludes network time.
- Files are created when the first request arrives; a separate file exists per URL group when logging is enabled on a URL group.

## Apache httpd
- The access log is controlled by `CustomLog` and `LogFormat`; the error log by `ErrorLog` (the page calls it the most important log) and `ErrorLogFormat`. Read the configuration to find real locations and formats.
- Common format is `%h %l %u %t "%r" %>s %b`; combined adds `"%{Referer}i" "%{User-agent}i"`. `%t` writes the time with a numeric offset (the example shows `-0700`), so convert using the offset. `%b` is `-` when no content was returned.
- Several `CustomLog` lines can write several files, and `env=` clauses can exclude requests, so absence from a log is not proof a request never happened.
- Logs contain client-supplied data without escaping; malicious clients can insert control characters, so treat raw logs carefully (for example do not print them straight into a terminal).
- Anyone who can write to the log directory can probably gain the server's start uid (normally root).

## nginx
- `access_log` defaults to `logs/access.log` in the `combined` format (`$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"`); `$time_local` is local time in Common Log Format. Check `log_format` for local changes, including `escape=json`.
- Default escaping writes `"` , `\` and bytes outside 32 to 126 as `\xXX`, and a missing variable as `-`.
- `buffer=` or `gzip` makes writes buffered, so recent lines may not yet be on disk; gzip-buffered logs are readable with `zcat`.
- `if=` conditional logging can omit requests (the page's example drops 2xx and 3xx), `access_log off` cancels logging at that level, and logging can go to syslog with the `syslog:` prefix. Confirm what was logged before treating a missing request as absent.
- Requests are logged in the location where processing ends, which can differ after an internal redirect.

## Practice
1. Record the format directive or `#Fields:` header, time zone convention and logging conditions first.
2. Normalise all timestamps to UTC before merging sources.
3. Check whether the logged client address is the real client or a proxy hop; the pages cited do not describe forwarded-header logging, so consult the configuration.
4. POST bodies are not part of these formats; use other logs for payloads.

## Verify
Each request attributed to the attacker cites file, line, format definition and time zone conversion, and gaps from buffering, conditional logging or rotation are stated.

## Checked
Confirmed against the HTTP Server API W3C logging page (fields, prefixes, UTC time, hyphen and plus-sign handling, time-taken), the Apache httpd Log Files page (CustomLog, LogFormat, common and combined formats, environment-based exclusion, unescaped client data, directory write risk) and the nginx ngx_http_log_module page (defaults, combined format, escaping, buffering, conditional logging, syslog). Removed unconfirmed content: default log paths, the claim that IIS logs live under `inetpub\logs\LogFiles\W3SVC<id>`, the shell and Log Parser triage commands, exploit signatures and web shell heuristics, X-Forwarded-For logging details, and the w3wp correlation step.

Method: docs-only read of cited pages, 2026-11-09
