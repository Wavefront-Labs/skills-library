---
id: computing-software.networking-hardware-and-wireless.haproxy.logging-to-syslog-and-journald
name: logging-to-syslog-and-journald
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, log-global, syslog, log-stdout, log-format-length, dontlognull]
level: practitioner
status: docs-checked
description: "Send HAProxy logs to syslog, stdout or a ring with the log keyword: targets, formats, length, levels, dontlognull and set-log-level silent."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logging to syslog and journald
The `log` keyword declares loggers per instance (defaults, frontend, listen, backend). `log global` reuses the global section's loggers and takes no other parameter; only one `log global` per instance. `no log` flushes the inherited logger list.

```
global
    log /dev/log local0 info
    log stdout format short daemon
defaults
    log global
    option httplog
    option dontlognull
    option log-health-checks
```
Syntax: `log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>] <facility> [<level> [<minlevel>]]`.

- Targets: IPv4 address with optional UDP port (default 514); IPv6 address followed by a colon and optional port; a UNIX socket path (it must be reachable and writable inside any chroot); `fd@<n>`; `stdout`/`stderr` (aliases for `fd@1`/`fd@2`); `ring@<name>`; `backend@<name>` (a backend with `mode log`); or a stream prefix such as `tcp@`, `tcp4@`, `tcp6@`, `uxst@`, which creates an implicit ring with a stream forward server.
- `fd@` targets use unbuffered logs with one `writev()` per log: messages are not truncated but may be dropped (the `DroppedLogs` counter increments). Pointing an fd at a file is for debugging only and cannot be rotated without restarting.
- `ring@<name>` is an in-memory buffer readable with `show events` on the CLI; it is lost on reload or restart, so use it as a complement.
- `len <length>` truncates lines to 80 to 65535 bytes (default 1024, which all syslog servers support). Raise it only when the server accepts long lines, and raise `tune.http.logurilen` if request URIs are truncated.
- `format`: `local` (default; RFC3164 without the hostname), `rfc3164`, `rfc5424`, `priority`, `short` (only `<level>` then text, compatible with what the systemd logger consumes), `timed`, `iso`, `raw` (text only, for containers or development where severity depends on stdout or stderr). The facility is ignored for `short` and `raw` but is still a required positional field; `daemon` is recommended.
- Facilities are the 24 standard names (`kern` to `local7`). The optional `<level>` filters: only messages at least that severe are sent. An optional `<minlevel>` caps more severe messages to that level (to avoid sending `emerg` to all terminals).
- The frontend decides what is logged for a connection; backend log entries are ignored under content switching. Connections log at `info`. Backend log declarations govern server status changes: `notice` for a server going up, `warning` for termination signals and definitive service termination, `alert` for a server going down.
- `log-tag <string>` sets the syslog tag; it defaults to the global `log-tag`, otherwise the program name (usually `HAProxy`). Server up/down logs in a backend use that backend's tag.
- `option dontlognull` (defaults, frontend, listen) skips logging connections where no data was transferred, which is typically probes. Errors are still returned to the client and counted in stats. The manual advises against it on uncontrolled networks such as the internet, since scans go unlogged. `option http-ignore-probes` is the alternative if you want accounting kept.
- `http-request set-log-level <level>` changes the level for one request; the special level `silent` disables logging for it, which suits health checks from other equipment. It is not final: the last matching rule wins.
- `option log-health-checks` (not valid in a frontend) logs every health check status change. By default only failed checks on an UP server and successful checks on a DOWN server are logged.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `log` (all arguments, targets, formats, facilities, levels, defaults and the frontend/backend logging notes), `log-tag`, `option dontlognull`, `set-log-level`, `option log-health-checks`. Removed: the rsyslog configuration file and its socket line, the `/dev/log` chroot explanation beyond the manual's chroot note, the claim that logs vanish silently without a listener, the `ring` consumption by TCP sinks, and the `logger`/`tail` verification. Read as sections of the manual only.
Method: documentation only; no commands were run.
