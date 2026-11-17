---
id: computing-software.systems-network-administration.keepalived.daemon-config-file-and-subsystems
name: daemon-config-file-and-subsystems
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, command-line, config-file, vrrp-only, check-only, dump-conf, dont-fork]
level: practitioner
status: docs-checked
description: "Keepalived daemon options for choosing the config file and subsystems: -f, -P vrrp only, -C checker only, -n foreground, -d dump config, -x SNMP, -v version."
sources:
  - https://keepalived.readthedocs.io/en/latest/programs_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemon options: config and subsystems

| Option | Effect |
|---|---|
| `-f`, `--use-file=FILE` | Use FILE as configuration. Default /etc/keepalived/keepalived.conf |
| `-P`, `--vrrp` | Run only the VRRP subsystem (no IPVS load balancing needed) |
| `-C`, `--check` | Run only the health-check subsystem (single director, no failover) |
| `-n`, `--dont-fork` | Stay in the foreground |
| `-d`, `--dump-conf` | Dump parsed configuration data to the logs |
| `-x`, `--snmp` | Enable the SNMP subsystem |
| `-v`, `--version` | Show version and exit |
| `-h`, `--help` | Show help and exit |

Typical uses: `-P` for a pure VRRP pair; `-C` for one IPVS director that only needs health checking; `-n` plus `-d` to see what was parsed while debugging a config.

Verify: with `-d`, the parsed configuration in the logs matches what you wrote in the file.

## Checked

2026-11-04. Confirmed each option, the default config path and the -P and -C use cases on the Keepalived programs synopsis page, including that the dump appears in the syslog output. Nothing removed.

Method: documentation only; no commands were run.
