---
id: computing-software.networking-hardware-and-wireless.apache-httpd.apachectl-start-stop-graceful
name: apachectl-start-stop-graceful
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, apachectl, restart, graceful, configtest, status]
level: intro
status: docs-checked
description: "Control a running server with apachectl: start, stop, restart, graceful, graceful-stop, configtest and status, and how restart differs from graceful."
sources:
  - https://httpd.apache.org/docs/2.4/programs/apachectl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apachectl start, stop, graceful
apachectl is a front end to httpd; each command equals `apachectl -k <option>` unless noted.

## Commands
- `start`: errors if already running.
- `stop`: stops httpd.
- `restart`: restarts, starting it if not running. It runs a config check first so the daemon does not die.
- `graceful`: graceful restart, starting if needed; also checks config first. It does not abort open connections.
- `graceful-stop`: graceful stop.
- `configtest`: reports `Syntax Ok` or error details (same as `-t`).
- `status`: brief report from mod_status.
- `fullstatus`: full report including current requests; needs mod_status and a text browser such as lynx. The URL comes from `STATUSURL` in the script.

## Notes
- Side effect of `graceful`: old log files are not closed immediately, so rotation scripts need a delay before processing them.
- `startssl` has been removed; configure SSL directives and use `apachectl start`.
- Exit value is 0 on success, above 0 on error.
- Non-standard installs may need the script edited for the httpd binary path.

```
apachectl configtest
apachectl graceful
```

## Checked

2026-11-08. All commands, equivalences, side effects, exit values and the removed startssl option confirmed against the full apachectl manual page (httpd 2.4).

Method: documentation only; no commands were run.
