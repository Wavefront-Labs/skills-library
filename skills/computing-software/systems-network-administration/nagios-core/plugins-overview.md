---
id: computing-software.systems-network-administration.nagios-core.plugins-overview
name: plugins-overview
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, plugins, nagios-plugins, check-http, plugin-help, plugin-sources, nagios-exchange]
level: intro
status: docs-checked
description: "What Nagios Core plugins are, why core has no built-in checks, where to get official and community plugins, and how to read a plugin's usage."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/plugins.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugins

- Plugins are standalone programs (compiled or Perl, shell, Python, PHP, Ruby scripts) that Nagios runs when a host or service needs checking.
- Nagios Core has no built-in check logic: it tracks state changes and triggers handlers and notifications. Only the plugin knows what is being monitored.
- Categories available: protocols (HTTP, POP3, IMAP, FTP, SSH, DHCP), resources (load, disk, memory, users), platforms (Unix/Linux, Windows, Netware), network gear (routers, switches).

## Getting them
Not shipped with Core. Sources: Nagios Plugins project on GitHub, the Nagios downloads page, Nagios Exchange.

## Reading usage
Most plugins respond to `-h`/`--help`:
```
./check_http --help
```
## Next
Exit codes and output format: `computing-software.systems-network-administration.nagios-core.plugin-exit-codes-output`. Wiring to a command: `computing-software.systems-network-administration.nagios-core.command-definition`.

## Checked

2026-11-04. Confirmed against the Plugins page (what plugins are, no internal checks in Core, categories available, three download locations, -h and --help with ./check_http --help). Removed an unconfirmed note about check_snmp and check_hpjd build requirements.

Method: documentation only; no commands were run.
