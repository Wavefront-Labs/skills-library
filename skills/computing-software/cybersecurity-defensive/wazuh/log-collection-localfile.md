---
id: computing-software.cybersecurity-defensive.wazuh.log-collection-localfile
name: log-collection-localfile
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [localfile, log-format, location, strftime, logcollector, wildcards]
level: intro
status: docs-checked
description: "Collect log files with the Wazuh localfile block: location, log_format, strftime placeholders, wildcards, Windows variables, 4.13.0 UNC change."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/monitoring-log-files.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Log files are read by the logcollector via `<localfile>` blocks in the agent `ossec.conf`:
- Linux/Unix: `/var/ossec/etc/ossec.conf`
- Windows: `ossec.conf` in the agent install directory (`ossec-agent` under Program Files (x86) by default)
- macOS: `/Library/Ossec/etc/ossec.conf`

```xml
<localfile>
  <location>/<FILE_PATH>/file.log</location>
  <log_format>syslog</log_format>
</localfile>
```

Patterns:
- Date-based names use `strftime` placeholders, for example `file-%y-%m-%d.log`.
- Wildcards such as `file*.log` match multiple files.
- Environment variables in the path work only on Windows endpoints, for example `%WINDIR%\Logs\StorGroupPolicy.log` (`%WINDIR%` is the Windows directory); `%ProgramFiles%` is another example variable.

Restart after changes: `systemctl restart wazuh-agent` (Linux), `Restart-Service -Name wazuh` in elevated PowerShell (Windows), `/Library/Ossec/bin/wazuh-control restart` (macOS).

Failure modes:
- From 4.13.0, Windows agents ignore UNC paths such as `\\server\share\file.log` and mapped drives such as `<DRIVE>:\logs\file.log`; only local file systems are supported and no monitoring or alerts occur for those locations.
- Centralized `agent.conf` settings take precedence over local `ossec.conf`.
- Wazuh server CPU and memory consumption is influenced by the number of events per second it must analyze.

## Checked

2026-11-08: confirmed against the Wazuh docs page Configuration for monitoring log files (read in full): ossec.conf locations, the localfile block, strftime date-based, wildcard and Windows environment-variable examples, the restart commands per OS, the 4.13.0 UNC and mapped-drive note, centralized precedence and the events-per-second note. Replaced a machine path with a description, fixed the doubled backslashes and removed the unsupported advice to be selective.
Method: documentation only; no commands were run.
