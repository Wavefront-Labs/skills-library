---
id: computing-software.messaging-and-integration.prosody.prosodyctl-commands
name: prosodyctl-commands
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, prosodyctl, cli, administration, users]
level: intro
status: docs-checked
description: "prosodyctl command reference for Prosody: adduser, passwd, deluser, reload, status, shell, install, remove, list, about, and the --config and --root flags."
sources:
  - https://prosody.im/doc/prosodyctl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prosodyctl commands

Usage: `prosodyctl COMMAND [OPTIONS]`

- Users: `adduser JID`, `passwd JID`, `deluser JID` (permanent).
- Process: `reload` (reloads config and reopens log files), `status`.
- `shell`: opens a secure connection to the Prosody console.
- Plugins: `install mod_plugin`, `remove mod_plugin`, `list`.
- Info: `about` (versions and paths), `check WHAT`.
- Legacy process management for systems without an init system: `start`, `stop`, `restart`. Otherwise use `systemctl`.

Flags:

- `--config /path/to/config.cfg.lua` uses an alternative config file.
- `--root` stops prosodyctl switching to the Prosody user when run as root.

```
prosodyctl adduser alice@example.com
prosodyctl reload
```

Verify: `prosodyctl status` reports Prosody running and `prosodyctl about` prints the expected paths.

## Checked

2026-11-04. Read the prosodyctl page: every listed command, the legacy start, stop and restart note, and the --config and --root flags match. Nothing removed.

Method: documentation only; no commands were run.
