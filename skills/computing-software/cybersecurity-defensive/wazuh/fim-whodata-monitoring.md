---
id: computing-software.cybersecurity-defensive.wazuh.fim-whodata-monitoring
name: fim-whodata-monitoring
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [whodata, audit, ebpf, queue-size, windows-audit, sacl]
level: advanced
status: docs-checked
description: "Enable who-data FIM on Linux with the audit or ebpf provider and on Windows with whodata=yes, plus the auditd checks and fallbacks that commonly break it."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/advanced-settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Who-data adds the acting user and process to FIM alerts.

Linux: set `<whodata><provider>` inside `<syscheck>` to `audit` (default) or `ebpf`. Do not combine them; the last configured provider applies to all who-data directories.
- Audit mode needs the `auditd` package. On Audit 3.1.1+, also install `audispd-plugins` and restart `auditd`.
- Look for a blocking rule with `auditctl -l | grep task`; a `-a never,task` rule must be removed from `/etc/audit/rules.d/audit.rules`.
- Confirm the Wazuh rule with `auditctl -l | grep wazuh_fim`. The agent removes it when it stops.
- eBPF needs BPF ring buffer and BTF support (kernel 5.8+ or backported kernels). If the health check fails, FIM falls back to audit.
- Raise `queue_size` (the page uses 50000) to avoid losing bursts, at the cost of agent memory.

Alert fields include `audit.user`, `audit.login_user`, `audit.effective_user`, `audit.group`, `audit.process.id`, `.name` and `.ppid`.

Windows: add `whodata="yes"` to `<directories>`. Audit policies and SACLs are set automatically; if another service changes them, FIM falls back to real-time for affected directories. Manual setup needs Success auditing for Audit File System and Audit Handle Manipulation.

Other gotchas: `syscheck.rt_delay` (milliseconds, server `internal_options.conf`) sets the delay between alerts. `SysWOW64` must be added separately from `System32`. UNC paths are not supported from 4.13.0.

## Checked

2026-11-03. Confirmed against the Wazuh page "Advanced settings" (FIM): audit/ebpf provider and last-provider-wins, audispd-plugins on Audit 3.1.1+, the `-a never,task` check and file, the `wazuh_fim` rule check and its removal on stop, eBPF kernel 5.8 / BPF ring buffer / BTF, health-check fallback to audit, queue_size 50000 and memory note, the audit.* alert fields, Windows `whodata="yes"` with automatic audit policy/SACL and real-time fallback, manual Success auditing policies, `syscheck.rt_delay` in milliseconds, and SysWOW64. Nothing else removed.

Method: documentation only; no commands were run.
