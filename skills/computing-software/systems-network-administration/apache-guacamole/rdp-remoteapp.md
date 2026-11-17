---
id: computing-software.systems-network-administration.apache-guacamole.rdp-remoteapp
name: rdp-remoteapp
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, remoteapp, remote-app, remote-app-dir, remote-app-args, published-application, initial-program]
level: practitioner
status: draft
description: "Publish a single Windows application through Guacamole RDP RemoteApp: remote-app with the double-bar prefix, remote-app-dir and remote-app-args."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP RemoteApp

Show one program instead of a full desktop.

| Parameter | Meaning |
|---|---|
| `remote-app` | RemoteApp name prefixed with two vertical bars, e.g. `||notepad` |
| `remote-app-dir` | working directory; no effect without remote-app |
| `remote-app-args` | command-line arguments; no effect without remote-app |

Steps:
1. The Windows server must have the program published as a RemoteApp (an alias such as `notepad`).
2. In the Guacamole connection set `remote-app` to `||` plus that alias.
3. Optionally set `remote-app-dir` and `remote-app-args`.
4. Connect.

Difference from `initial-program`: that parameter launches a program inside a normal desktop session (apache-guacamole.rdp-gateway-and-session), whereas RemoteApp uses the RemoteApp channel.

Tip: check the server's RemoteApp configuration and allowlist if the connection ends immediately; the manual lists no RemoteApp-specific log messages.

Verify: only the application window appears, and typed input reaches it.
