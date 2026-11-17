---
id: computing-software.systems-network-administration.nagios-core.monitor-windows-ncpa
name: monitor-windows-ncpa
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, monitor-windows, ncpa, check-ncpa, nrdp, ncpa-cfg, passive-checks, windows-monitoring]
level: practitioner
status: docs-checked
description: "Monitor a Windows host from Nagios Core with the NCPA agent: active checks via check_ncpa.py (port 5693, token) and passive checks through NRDP."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/monitoring-windows.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows with NCPA

The doc page covers only NCPA (not NSClient++).

## Active
1. Download `check_ncpa.py`, own it as the nagios user, place it in the plugins directory (`/usr/local/nagios/libexec`).
2. Define a `check_ncpa` command passing the host address and variable arguments.
3. Define the host and services using `-t <TOKEN>`, port **5693** and a metric path:
   - CPU `cpu/percent` warn 20, crit 40
   - Memory `memory/virtual` warn 50, crit 80 (GB)
   - Processes `processes` warn 150, crit 200
4. Restart Nagios. Replace the example token with your own.

## Passive
1. In the NCPA `ncpa.cfg.d` directory add checks: `%HOSTNAME%|Service = metric --warning X --critical Y`. Append `|interval` seconds to the service name (default 5 minutes).
2. In `ncpa.cfg` add an `[nrdp]` section (parent URL, token, hostname).
3. Set `handlers = nrdp` in `[passive]`.
4. Restart `ncpa_listener`.

Windows service commands: `net stop ncpa`, `net start ncpa`.

Auth is a token, not a password. The Nagios host must accept the passive results (`computing-software.systems-network-administration.nagios-core.passive-checks`).

## Checked

2026-11-04. Confirmed on the Monitoring Windows page: NCPA only, check_ncpa.py installed to the plugins directory and owned by nagios, check_ncpa command, -t token with -P 5693, cpu/percent -w 20 -c 40, memory/virtual -w 50 -c 80 -u G, processes -w 150 -c 200, passive checks in ncpa.cfg.d with the %HOSTNAME%|Service = metric --warning --critical form and |interval in seconds (default 5 minutes), [nrdp] parent/token/hostname, handlers = nrdp under [passive], restart ncpa_listener, net stop/start ncpa. Nothing removed.

Method: documentation only; no commands were run.
