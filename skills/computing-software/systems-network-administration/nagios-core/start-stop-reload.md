---
id: computing-software.systems-network-administration.nagios-core.start-stop-reload
name: start-stop-reload
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, start, stop, restart, reload, sighup, sigterm, init-script, daemon]
level: intro
status: docs-checked
description: "Start, stop and reload Nagios Core: init script commands, manual -d start, SIGHUP to reload, SIGTERM to stop, and the web UI Process Info restart."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/startstop.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Starting and stopping Nagios Core

Restarting or reloading is necessary after modifying configuration files. See also `computing-software.systems-network-administration.nagios-core.verify-configuration`.

| Action | Init script | Manual | Web UI |
|---|---|---|---|
| Start | `/etc/rc.d/init.d/nagios start` | `/usr/local/nagios/bin/nagios -d /usr/local/nagios/etc/nagios.cfg` | - |
| Reload (after config change) | `/etc/rc.d/init.d/nagios reload` | `kill -HUP <nagios_pid>` | Process Info, restart |
| Stop | `/etc/rc.d/init.d/nagios stop` | `kill <nagios_pid>` (SIGTERM) | Process Info, shutdown |

Notes
- The web UI entries are the Process Info page links "Restart the Nagios process" and "Shutdown the Nagios process".
- The page does not cover systemd units.

## Checked

2026-11-04. Confirmed against the Starting and Stopping page: init script start, reload and stop, manual -d start, kill -HUP and kill (SIGTERM), and the Process Info restart and shutdown links. Removed unconfirmed notes about lock_file, make install-init, retained state and a self-check.

Method: documentation only; no commands were run.
