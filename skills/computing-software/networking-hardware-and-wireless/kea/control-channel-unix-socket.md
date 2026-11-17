---
id: computing-software.networking-hardware-and-wireless.kea.control-channel-unix-socket
name: control-channel-unix-socket
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, control-channel, unix-socket, socat, control-sockets]
level: practitioner
status: docs-checked
description: "Open and use the Kea UNIX control socket: control-sockets settings, path restrictions since 2.7.9, and sending commands with socat."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
  - https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea UNIX control socket
Set `socket-type` to "unix" and `socket-name` in `control-sockets`. Only one unix control socket is allowed in the list. By default no sockets are open.

- Path length is limited to the size of `sun_path` minus 1: between 91 and 107 characters depending on the OS (typically 107 on Linux, 103 on FreeBSD).
- Since Kea 2.7.9, control sockets may only live in `[kea-install-dir]/var/run/kea`, which must have 0750 access rights. Override with the environment variable `KEA_CONTROL_SOCKET_DIR`. A different path in `socket-name` makes Kea refuse to start (or log an unrecoverable error if running). Simplest is to give only a file name.
- Communication uses JSON.

Talk to the daemon directly with socat. Interactive:

```
socat UNIX:/path/to/the/kea/socket -
```

Batch, where `ignoreeof` makes socat wait for the response:

```
echo '{ "command": "config-get" }' | socat UNIX:/path/to/the/kea/socket -,ignoreeof
```

The path is the one in `Dhcp4/control-sockets/socket-name`. This reaches the specific server directly.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the DHCPv4 chapter sections Management API and UNIX Control Socket (default no sockets, sun_path limit 91-107, one unix socket, 2.7.9 directory rule with 0750) and the control channel chapter (socat usage). Nothing removed.
