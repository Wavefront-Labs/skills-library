---
id: computing-software.cloud-infrastructure-engineering.netdata.netdatacli-commands
name: netdatacli-commands
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, netdatacli, reload-health, readiness-check]
level: practitioner
status: docs-checked
description: "Control a running Netdata Agent without restarting it using netdatacli: reload health, labels, claiming state, logs, ping readiness and show ACLK state."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/start-stop-restart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`netdatacli` is the Agent's CLI tool; it sends commands to the running Agent without restarting it.

```
sudo netdatacli reload-health
sudo netdatacli ping
sudo netdatacli shutdown-agent
```

Commands listed in the docs:
- `reload-health`: reload alert configuration
- `reload-labels`: reload host labels from netdata.conf
- `reload-claiming-state`: reload claiming state from disk
- `reopen-logs`: close and reopen log files
- `ping`: readiness check
- `shutdown-agent`: graceful shutdown
- `aclk-state`: show ACLK/Cloud connection state
- `version`: show Agent version

`ping` prints `pong` and exits 0 when ready, exits 1 while initializing, and exits 255 if the Agent is unreachable, so it works in scripts and health checks.

Windows: the default install path is `Program Files\Netdata\usr\bin\netdatacli.exe`; run PowerShell as Administrator and use the full path (or add its directory to `PATH`):

```
& "$env:ProgramFiles\Netdata\usr\bin\netdatacli.exe" reload-health
```

Gotcha: other netdata.conf changes still need a restart; `reload-health` covers health config only.

## Checked

2026-11-04. Confirmed against the Netdata Service Control page: the eight netdatacli commands and descriptions, reload-health and shutdown-agent usage, the ping output and exit codes 0, 1 and 255, the Windows default path, Administrator PowerShell, full-path or PATH use, and the restart-needed note with the health exception. Replaced the unstated any-init-system wording and the drive placeholder with the documented default path.

Method: documentation only; no commands were run.
