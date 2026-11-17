---
id: computing-software.collaboration-platform-administration.vikunja.fail2ban-login-jail
name: fail2ban-login-jail
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, fail2ban-jail, failregex-login, http-log-file, brute-force-protection]
level: advanced
status: docs-checked
description: "Ban brute-force login attempts on Vikunja with a Fail2Ban filter and jail reading the HTTP log, with the reverse-proxy pitfall and CalDAV limits."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/fail2ban.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
First, behind a reverse proxy configure client IP extraction. Otherwise `remote_ip` is the proxy and the jail bans the proxy after `maxretry` failures, locking out everyone.

Log HTTP requests to a file:

```
log:
  path: "/var/lib/vikunja/logs"
  enabled: true
  http: "file"
```

Filter `/etc/fail2ban/filter.d/vikunja.conf`:

```
[Definition]
datepattern = ^time=%%Y-%%m-%%dT%%H:%%M:%%S%%Z
failregex = ^.*\bmsg="POST\s+/api/v\d+/login[^"]*".*\bstatus=(?:400|403|412)\b.*\bremote_ip=<HOST>\b.*$
```

Jail in `/etc/fail2ban/jail.local`: `[vikunja]`, `enabled = true`, `backend = auto`, `filter = vikunja`, `port = http,https`, `logpath = /var/lib/vikunja/logs/http.log`, `maxretry = 3`, `findtime = 600`, `bantime = 3600`.

Check with `fail2ban-client status vikunja`.

Only `POST /api/v1/login` and `/api/v2/login` match; CalDAV (`/dav`, `/.well-known/caldav`) failures do not. From 2.6.0 an always-on limit applies to Basic Auth endpoints (10 failed attempts per IP per minute by default, `ratelimit.basicauthlimit`). Rate limits and Fail2Ban can be combined.

## Checked

2026-11-04. Confirmed against the Vikunja Fail2Ban Setup page (setup/fail2ban): reverse proxy warning, log config, filter and failregex, the endpoints matched, the 2.6.0 Basic Auth limit and ratelimit.basicauthlimit, jail values and the fail2ban-client check. Nothing removed.

Method: documentation only; no commands were run.
