---
id: computing-software.cloud-infrastructure-engineering.netdata.start-stop-restart-unix
name: start-stop-restart-unix
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, systemctl, restart-agent, init-script]
level: intro
status: docs-checked
description: "Start, stop, restart and check the Netdata Agent on UNIX systems under systemd, non-systemd init, or when run directly, and confirm it is up."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/start-stop-restart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
systemd:

```
sudo systemctl start netdata
sudo systemctl stop netdata
sudo systemctl restart netdata
sudo systemctl status netdata
```

Non-systemd: `sudo service netdata start|stop|restart|status`, or `sudo /etc/init.d/netdata <action>`.

Direct daemon (typically `/usr/sbin/netdata`): start with `sudo netdata`; if you started it that way, stop it with `sudo killall netdata`.

Verify the Agent is answering:

```
curl http://NODE:19999/api/v1/info
```

Replace `NODE` with the Agent IP or hostname, or open `http://NODE:19999` in a browser.

Gotchas:
- The Agent starts automatically at boot after installation (Homebrew on macOS is the exception).
- Most configuration changes need a restart; health (alert) config files can be reloaded without one (`sudo netdatacli reload-health`).
- A restart causes temporary gaps in collected metrics.

## Checked

2026-11-04. Confirmed against the Netdata docs page netdata-agent/start-stop-restart: systemctl and service/init.d commands, direct netdata start and killall stop, the curl api/v1/info check against NODE:19999, autostart at boot with the Homebrew exception, restart being needed for most config but not health config, and temporary metric gaps on restart. Replaced the cross-reference to a netdatacli skill with the documented reload-health command.
Method: documentation only; no commands were run.
