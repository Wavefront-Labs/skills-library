---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mpm-common-limits
name: mpm-common-limits
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mpm, maxrequestworkers, serverlimit, listenbacklog, maxconnectionsperchild, gracefulshutdowntimeout]
level: practitioner
status: docs-checked
description: "Set the directives shared by all MPMs: MaxRequestWorkers, ServerLimit, StartServers, ThreadsPerChild, MaxConnectionsPerChild, ListenBackLog, PidFile and more."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mpm_common.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common MPM directives
| Directive | Default and notes |
|---|---|
| `MaxRequestWorkers` | 256 prefork; threaded default is 16 (`ServerLimit`) x 25 (`ThreadsPerChild`). Multiple of `ThreadsPerChild`; was `MaxClients` before 2.3.13 |
| `ServerLimit` | fixed for server life; raise only if needing >16 processes (worker/event) or >256 (prefork) |
| `StartServers` | 3 worker/event, 5 prefork |
| `ThreadsPerChild` | 25 (64 on winnt), up to `ThreadLimit` |
| `ThreadLimit` | 64 (1920 on winnt); restart-time change has no effect |
| `MaxConnectionsPerChild` | 0 = never expire; formerly `MaxRequestsPerChild` |
| `ListenBackLog` | 511; the OS may cap it |
| `ReceiveBufferSize` / `SendBufferSize` | 0 = OS default; otherwise at least 512 |
| `GracefulShutdownTimeout` | 0 = wait indefinitely |
| `PidFile` | `logs/httpd.pid`, relative to ServerRoot |
| `ScoreBoardFile` | `logs/apache_runtime_status`; unset uses shared memory |

## Notes
- `Listen` is required; the server will not start without it.
- A non-zero `MaxConnectionsPerChild` limits memory growth from leaks.
- Start and stop with `apachectl` or the init script.

## Checked
2026-11-04. Confirmed against the MPM common directives reference: defaults and limits in the table, MaxClients rename, Listen requirement, MaxConnectionsPerChild, apachectl recommendation. Removed: the mod_unixd User/Group note (not on the page). Reworded the threaded MaxRequestWorkers default to the documented 16 x 25.
Method: documentation only; no commands were run.
