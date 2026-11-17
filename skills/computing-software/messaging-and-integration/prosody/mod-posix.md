---
id: computing-software.messaging-and-integration.prosody.mod-posix
name: mod-posix
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, posix, daemon, signals, pidfile, umask]
level: practitioner
status: docs-checked
description: "mod_posix in Prosody: daemonize, pidfile, umask 027 and run_as_root defaults, signal handling (SIGHUP reload), and its deprecation in Prosody 13.0."
sources:
  - https://prosody.im/doc/modules/mod_posix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_posix

POSIX features: daemonizing, syslog logging, signal handling. Loaded automatically on POSIX platforms; deprecated since 13.0, so it can be removed from configs.

Signals: SIGTERM and SIGINT start a graceful shutdown, SIGHUP reloads the config.

| Option | Default |
|---|---|
| `daemonize` | true (deprecated since 0.12; use the `-D` or `-F` flags) |
| `run_as_root` | false (Prosody exits if run as root unless true) |
| `pidfile` | nil |
| `umask` | `"027"` |

```lua
daemonize = false
pidfile = "/path/to/prosody.pid"
umask = "027"
```

Prosody does not need root. In Debian/Ubuntu packages setuid and setgid are handled by the systemd service or init script.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_posix (deprecation since 13.0, signals, four options and defaults, Debian/Ubuntu note). Removed the unconfirmed claim that SIGHUP reload keeps sessions and a generic verify line.
Method: documentation only; no commands were run.
