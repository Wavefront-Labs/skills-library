---
id: computing-software.systems-network-administration.apache-guacamole.troubleshooting-guacd-errors
name: troubleshooting-guacd-errors
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, troubleshooting, syslog, guacd-errors, error-instantiating-client, client-plugin-errors, vnc-errors, rdp-errors, debugging]
level: practitioner
status: draft
description: "Decode Guacamole guacd and client-plugin log messages in syslog: bind failures, plugin load errors, bad parameters, handshake failures, and RDP/VNC-specific messages."
sources:
  - https://guacamole.apache.org/doc/gug/troubleshooting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Troubleshooting: guacd and plugins (syslog)

guacd and plugins log to syslog.

guacd:
- `Unable to bind socket to any addresses`: port (default 4822) in use; free it or start guacd with `-l PORT` and update `guacd-port`.
- `Unable to start input/output thread`: cause logged beside it.
- `Client finished abnormally`: read the lines just above.
- `Could not fork() parent`: system load/resources.
- `Unable to resolve host`: guacd's own listen address, not the target.
- `Could not write PID file`: permissions on the path.
- `Error loading client plugin`: protocol plugin (VNC, RDP...) not installed; rebuild with its library (apache-guacamole.build-guacamole-server).
- `Error instantiating client`: a malformed or incorrect connection parameter.
- `Error reading OPCODE` / `Error sending "args"`: handshake failure; confirm all components are from the same release.
- `Error sending "sync"` / `Error flushing output`: client closed; usually ignorable.
- `Error reading instruction` / `Client instruction handler error`: mostly a closed connection; otherwise an old client, a plugin bug or the remote server.

VNC: `Error waiting for VNC message` / `Error handling VNC server message` (server closed or unsupported data); `Wrong argument count received` (web-app bug).

RDP:
- `Invalid PARAMETER`: bad width, height or color-depth.
- `Support for the CLIPRDR channel could not be loaded`: no clipboard redirection.
- `Cannot create static channel "NAME": failed to load "guac-common-svc"`: sound/drive/printer unavailable; place plugins in `freerdp2/` next to `libfreerdp2.so`.
- Clipboard type/terminator messages are informational.

Raise detail with `log_level` in guacd.conf (apache-guacamole.guacd-conf-options).

Verify: after the fix, the same action produces no new error lines in syslog.
