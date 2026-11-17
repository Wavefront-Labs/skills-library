---
id: computing-software.systems-network-administration.nagios-core.monitor-routers-switches-snmp
name: monitor-routers-switches-snmp
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, monitor-router, monitor-switch, check-snmp, check-ping, check-local-mrtgtraf, snmpwalk, ifoperstatus, switch-cfg]
level: practitioner
status: docs-checked
description: "Monitor a switch or router in Nagios Core: switch.cfg host, ping thresholds, SNMP uptime and port link status with check_snmp, MRTG bandwidth, finding OIDs with snmpwalk."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/monitoring-routers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring routers and switches

## Prereqs
- Uncomment `cfg_file=/usr/local/nagios/etc/objects/switch.cfg` in `nagios.cfg`.
- `check_snmp` must exist in the plugin dir; it is built only if net-snmp and net-snmp-utils were installed first.

## Host
Use the `generic-switch` template with `host_name`, `alias`, `address`, `hostgroups`.

## Services (community `public` is the docs' example)
- Ping: `check_ping!200.0,20%!600.0,60%` (WARNING at RTA > 200 ms or 20% loss; CRITICAL at 600 ms or 60%), normal 5 min, retry 1 min.
- Uptime: `check_snmp!-C public -o sysUpTime.0`
- Port link: `check_snmp!-C public -o ifOperStatus.1 -r 1 -m RFC1213-MIB` (`-r 1` OK if result contains 1; `-m` limits MIBs for speed).
- Bandwidth: `check_local_mrtgtraf!/path/to/mrtg/<ip>_1.log!AVG!1000000,2000000!5000000,5000000!10` (warn in/out bytes, crit in/out, CRITICAL if log older than 10 min).

## Find OIDs
```
snmpwalk -v1 -c public <switch-ip> -m ALL .1
```

Then verify and restart: `computing-software.systems-network-administration.nagios-core.verify-configuration`.

## Checked

2026-11-04. Confirmed on the Monitoring Routers and Switches page: uncommenting cfg_file for switch.cfg, check_snmp built only with net-snmp and net-snmp-utils, generic-switch template, check_ping!200.0,20%!600.0,60% thresholds with 5 minute and 1 minute intervals, check_snmp with -C public -o sysUpTime.0 and ifOperStatus.1 -r 1 -m RFC1213-MIB, check_local_mrtgtraf arguments (AVG, in/out warning and critical bytes, 10 minute log age), and the snmpwalk tip. Nothing removed.

Method: documentation only; no commands were run.
