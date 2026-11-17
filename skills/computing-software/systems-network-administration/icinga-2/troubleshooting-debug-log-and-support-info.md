---
id: computing-software.systems-network-administration.icinga-2.troubleshooting-debug-log-and-support-info
name: troubleshooting-debug-log-and-support-info
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, troubleshooting, debuglog, debug-log, fileloggers, support-information]
level: practitioner
status: docs-checked
description: "Collect Icinga 2 support info and enable debug output via debuglog, daemon -x notice, or a runtime FileLogger created through the API."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting: support information and debug output
**Information to gather** when asking for help: expected versus actual behaviour; how Icinga 2 was installed and the distribution; `icinga2 --version`, `icinga2 feature list`, `icinga2 daemon -C`; Icinga Web version and modules; relevant config (`icinga2.conf`, `zones.conf` from every node, or `icinga2 object list --type Endpoint` and `--type Zone`); main and debug logs from `/var/log/icinga2`, the newest crash log in `/var/log/icinga2/crash`; manual plugin output if a check failed.

**Debug log (Linux/Unix):** `icinga2 feature enable debuglog`, restart, then `tail -f /var/log/icinga2/debug.log`. Or run in the foreground with `/usr/sbin/icinga2 daemon -x notice`; severities are critical, warning, information, notice, debug.

**Windows:** run `icinga2.exe feature enable debuglog` from an administrative PowerShell, then `Restart-Service icinga2`.

**On the fly, no restart:** create a FileLogger via the API (useful when reloads are slow; the log grows fast, so remove it afterwards).
```
PUT /v1/objects/fileloggers/on-the-fly-debug-file
{ "attrs": { "severity": "debug", "path": "/var/log/icinga2/on-the-fly-debug.log" } }
```
Remove it with `DELETE /v1/objects/fileloggers/on-the-fly-debug-file`; this works only for loggers created this way. In an HA zone the calls toggle the feature on both nodes.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/. No commands were run.
