---
id: computing-software.systems-network-administration.apache-guacamole.guacd-conf-options
name: guacd-conf-options
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, guacd, guacd-conf, guacd-ssl, bind-host, bind-port, log-level, tls-guacd, command-line-options]
level: practitioner
status: docs-checked
description: "Configure guacd with guacd.conf sections ([daemon], [server], [ssl]) and command-line flags -b -l -p -L -f -C -K, including enabling TLS between web app and guacd."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# guacd.conf and command-line options

`guacd.conf` lives in `/etc/guacamole` by default.

```ini
[daemon]
pid_file = /path/to/guacd.pid
log_level = info        ; trace, debug, info, warning, error

[server]
bind_host = localhost   ; default
bind_port = 4822        ; default

[ssl]
server_certificate = /path/to/server.crt
server_key = /path/to/server.key
```

Command-line flags override the file:
- `-b HOST` bind address; `-l PORT` listen port (default 4822)
- `-p PIDFILE`; `-L LEVEL` log level (default info); `-f` foreground
- `-C CERTIFICATE`, `-K KEY` enable SSL

TLS between web app and guacd:
1. Give guacd a certificate and key (`[ssl]` section or `-C`/`-K`); setting either enables SSL.
2. Set `guacd-ssl: true` in `guacamole.properties` (Docker: `GUACD_SSL`). The two sides must agree.
3. guacd must have been built with SSL support (libssl installed at build time).

If the web app and guacd are on different hosts, guacd binds to localhost by default and then only accepts connections from its own host, so set `bind_host` (or `-b`) to a reachable address and enable SSL.

Verify: start `guacd -f -L debug` in the foreground with debug logging and confirm a Guacamole connection works.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole and guacamole-native: guacd.conf location and INI layout, [daemon], [server] and [ssl] parameters and defaults, the command-line flags and that they take precedence over the file, SSL enabled by a certificate or key, the matching guacd-ssl setting and GUACD_SSL, and libssl giving guacd SSL support. Changed: removed the authentication and firewall claim and the bind-address log claim, which the page does not make.

Method: documentation only; no commands were run.
