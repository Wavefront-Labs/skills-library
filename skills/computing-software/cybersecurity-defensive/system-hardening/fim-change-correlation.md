---
id: computing-software.cybersecurity-defensive.system-hardening.fim-change-correlation
name: fim-change-correlation
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [file-integrity-monitoring, fim-change-correlation, change-management, itsm-integration, authorised-change, alert-triage]
level: advanced
status: draft
description: "Correlate FIM alerts with approved change records and patch windows so only unexplained changes reach analysts, using CMDB, ITSM and package-manager data."
sources: ["PCI DSS v4.0 Requirements 11.5.2 and 6.5 change management", "NIST SP 800-53 Rev 5 CM-3 and SI-7", "ITIL 4 Change Enablement practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Correlating FIM alerts with change records

**Goal:** FIM output becomes actionable: authorised changes are auto-explained, the rest are investigated as potential intrusions.

## Data needed
- FIM events: host, path, change type, hashes before/after, user/process (whodata), timestamp.
- Change records: ITSM change id, affected CIs (hosts/services), approved window start/end, implementer.
- Patch/deploy events: package manager logs (`/var/log/dnf.log`, `/var/log/apt/history.log`, Windows `Setup` log / Intune), CI/CD deploy events with host and version.

## Correlation logic (SIEM rule/lookup)
1. Enrich FIM event with CMDB CI and owning team.
2. Match against open change records where host in affected CIs and timestamp within window -> tag `authorised:change=<id>`.
3. Match against package events: file belongs to a package (`rpm -qf`) updated within N minutes on that host -> tag `authorised:patch`.
4. Match deploy pipeline events for application paths -> tag `authorised:deploy`.
5. Everything else -> alert to SOC, priority by path criticality (sshd_config, sudoers, binaries in PATH, web roots high).

Splunk-style sketch:
```
index=fim | lookup change_windows host OUTPUT change_id start end
| where isnull(change_id) OR _time<start OR _time>end
| lookup critical_paths path OUTPUT criticality
```

## Process
- Changes outside window or by an unexpected user get a ticket to the implementer for explanation within an SLA; unexplained -> incident.
- Monthly report: % FIM changes linked to change records (target > 95%); repeat offenders indicate emergency changes bypassing process.

## Gotchas
- Change records with vague CIs ("all web servers") weaken matching; require explicit host groups.
- Auto-updates (unattended-upgrades, Windows Update) need standing change records or package correlation.
- Attackers time changes into maintenance windows; still verify hashes against vendor packages.

## Verify
- [ ] A test change during an approved window auto-closes; the same change outside the window alerts.
- [ ] Report shows linkage rate and unexplained change count per month.
