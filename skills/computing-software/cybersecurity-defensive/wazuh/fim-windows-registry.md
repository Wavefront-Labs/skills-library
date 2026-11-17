---
id: computing-software.cybersecurity-defensive.wazuh.fim-windows-registry
name: fim-windows-registry
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [windows-registry, registry-ignore, recursion-level, report-changes, syscheck]
level: practitioner
status: docs-checked
description: "Monitor Windows registry keys with windows_registry entries in syscheck, including recursion_level, report_changes, registry_ignore and scan timing."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/windows-registry-monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registry keys are monitored with `<windows_registry>` entries inside `<syscheck>` in `%ProgramFiles(x86)%\ossec-agent\ossec.conf` (or centralized configuration). Wildcards `*` and `?` work as in cmd. Apply changes with `Restart-Service -Name WazuhSvc` from elevated PowerShell.

Attributes:
- `check_all` (default yes): records size, last modification date and MD5, SHA1, SHA256 hashes.
- `check_sum` and `check_mtime`: toggle hashes and modification time.
- `recursion_level`: integer 0 to 512. 0 monitors only the values in the key itself. If unset, the default comes from `syscheck.default_max_depth` in internal options.
- `report_changes`: supports REG_SZ, REG_EXPAND_SZ, REG_MULTI_SZ, REG_DWORD, REG_DWORD_BIG_ENDIAN and REG_QWORD. Data is copied to `queue\diff\registry`, which uses extra storage.

Exclusions: `<registry_ignore>` takes one entry per line; add `type="sregex"` for regex matching.

Gotchas:
- Keys created after the initial scan are picked up only at the next scheduled scan. The default `<frequency>` is 43200 seconds; the page's use case lowers it to 300.
- Startup `Run` and `RunOnce` keys are monitored by default.
- The local FIM database lives in `%ProgramFiles(x86)%\ossec-agent\queue\fim\db`; the server's is under `/var/ossec/queue/db`.

## Checked

2026-11-03. Confirmed against the Wazuh page "Windows Registry monitoring": `<windows_registry>` entries and wildcards, `check_all`/`check_sum`/`check_mtime`, `recursion_level` 0 to 512 and the `syscheck.default_max_depth` default, report_changes value types and queue\diff\registry, `registry_ignore` with sregex, the next-scan note, the 43200-second default and 300-second use case, Run/RunOnce monitored by default, the `WazuhSvc` restart, and the database locations. Removed: the `<WAZUH_AGENT_DIR>` placeholders (the page gives the real path).

Method: documentation only; no commands were run.
