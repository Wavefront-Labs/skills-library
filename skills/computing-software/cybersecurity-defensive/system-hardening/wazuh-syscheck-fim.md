---
id: computing-software.cybersecurity-defensive.system-hardening.wazuh-syscheck-fim
name: wazuh-syscheck-fim
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [file-integrity-monitoring, wazuh-fim, syscheck, realtime-monitoring, whodata, windows-registry-monitoring, ossec]
level: practitioner
status: docs-checked
description: "Configure Wazuh syscheck FIM on Linux and Windows agents: directories, realtime and whodata modes, registry monitoring, ignores, and tuning alerts in the manager."
sources: ["https://github.com/wazuh/wazuh-documentation/blob/main/source/user-manual/reference/ossec-conf/syscheck.rst", "https://github.com/wazuh/wazuh-documentation/blob/main/source/user-manual/capabilities/file-integrity/advanced-settings.rst", "https://github.com/wazuh/wazuh-documentation/blob/main/source/user-manual/capabilities/file-integrity/how-it-works.rst", "https://github.com/wazuh/wazuh-documentation/blob/main/source/user-manual/capabilities/file-integrity/windows-registry-monitoring.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wazuh syscheck FIM

**Goal:** centrally managed FIM with who-changed-what detail on critical paths, without drowning in noise.

## Agent config (centralised via `agent.conf` groups)
```xml
<syscheck>
  <frequency>43200</frequency>
  <directories check_all="yes" realtime="yes">/etc,/usr/bin,/usr/sbin</directories>
  <directories check_all="yes" whodata="yes" report_changes="yes">/etc/ssh,/etc/sudoers.d</directories>
  <ignore>/etc/mtab</ignore>
  <ignore type="sregex">.log$|.swp$</ignore>
  <nodiff>/etc/ssl/private.key</nodiff>
</syscheck>
```
Windows:
```xml
<syscheck>
  <directories check_all="yes" whodata="yes">%WINDIR%\System32\drivers\etc</directories>
  <directories check_all="yes" realtime="yes">%PROGRAMFILES%\MyApp</directories>
  <windows_registry arch="both">HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run</windows_registry>
  <windows_registry arch="both">HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services</windows_registry>
</syscheck>
```

## Modes
- Scheduled scan (frequency) - baseline coverage.
- `realtime` - continuous monitoring on Linux (inotify) and Windows; works only with directories, not single files.
- `whodata` - adds who-made-the-change information on Linux and Windows. On Linux the default is audit mode (the Linux Audit subsystem; auditd must be installed and running); an `<whodata><provider>ebpf</provider></whodata>` block selects eBPF mode and falls back to audit mode if the health check fails. Heavier; use for crown-jewel paths.
- `report_changes` - reports changes to files, limited to text files; `nodiff` lists files (such as private keys) whose content changes must not be sent in alerts; `diff_size_limit` (default 50MB) caps the size.

## Manager side
- The manager keeps a synchronised copy of each agent's FIM database and normalises FIM events into Wazuh Common Schema documents.
- Findings are shown on the Wazuh dashboard under Endpoint security, File Integrity Monitoring, Findings. Custom alerting rules for critical or noisy paths are covered in the Wazuh ruleset documentation (not checked here).

## Gotchas
- In audit mode, an auditd rule such as `-a never,task` stops processing of later rules and prevents who-data reporting; remove it from the audit rules. The agent adds its audit rule when it starts and removes it when it stops.
- `ignore` paths are still scanned; they are only left out of reports.
- Monitoring package-managed dirs without correlating patches produces mass alerts after every update.

## Verify
- [ ] Touching `/etc/ssh/sshd_config` produces an alert with user and process name.
- [ ] Registry Run key change produces an alert on a Windows test agent.

## Checked
Checked 2026-10-25 against the Wazuh documentation sources (wazuh/wazuh-documentation, last commit 2026-10-23): the syscheck configuration reference (directories attributes `realtime`, `whodata`, `report_changes`, `check_all`, `diff_size_limit`; `frequency` default 43200; `ignore` with `type="sregex"`; `nodiff`; `windows_registry` with `arch` 32bit, 64bit or both), the FIM advanced-settings page (audit and eBPF who-data modes, the `-a never,task` caveat), how-it-works and Windows registry pages. Removed or corrected: `scan_on_start` is not in the current reference, the ReadDirectoryChangesW and SACL implementation details, rule IDs 550/553/554 and `0015-ossec_rules.xml` (rule files not checked), the `syscheck.path` indexer query (the dashboard now presents FIM findings), and the inotify watch-limit remark (documented for osquery, not Wazuh). The PCI DSS requirement reference was dropped from sources because the standard was not read.

Method: documentation only; no commands were run.
