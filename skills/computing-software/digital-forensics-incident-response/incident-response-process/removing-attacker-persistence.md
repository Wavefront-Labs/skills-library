---
id: computing-software.digital-forensics-incident-response.incident-response-process.removing-attacker-persistence
name: removing-attacker-persistence
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [persistence-removal, eradication, persistence, autoruns, web-shell, dfir]
level: practitioner
status: draft
description: "Remove attacker persistence and backdoors across the estate: inventory from forensics, removal per mechanism, avoiding partial clean-up, and verification sweeps."
sources: ["https://attack.mitre.org/tactics/TA0003/", "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Removing attacker persistence

**Goal:** every mechanism the attacker could use to regain execution is removed at once,
backed by an inventory built from forensics rather than guesswork.

## Build the inventory first
From forensic findings and estate-wide sweeps (Velociraptor `Windows.Sys.StartupItems`,
`Windows.System.TaskScheduler`, `Windows.Persistence.PermanentWMIEvents`; Autoruns compare
to baseline):
| Mechanism | Removal |
|---|---|
| Services | `sc.exe stop <svc>`, `sc.exe delete <svc>`, delete binary |
| Scheduled tasks | `schtasks /delete /tn "<name>" /f`; check `%SystemRoot%\System32\Tasks` and registry `TaskCache` for hidden tasks (SD value removed) |
| Run/RunOnce, Winlogon, IFEO | Delete values; also check Wow6432Node and every NTUSER.DAT |
| WMI subscriptions | `Get-WMIObject -Namespace root\subscription -Class __EventFilter`; remove filter, consumer and binding |
| Web shells | Delete file, check web root integrity vs deployment, rotate app secrets |
| Accounts | Disable attacker-created local/domain accounts, remove group memberships |
| Remote access tools | Uninstall AnyDesk/ScreenConnect etc. installed by attacker; block at firewall |
| SSH keys / cron (Linux) | Clean `authorized_keys`, crontabs, systemd units, `/etc/ld.so.preload` |
| Cloud | Attacker IAM users/keys, app registrations, OAuth grants, federation trusts |

## Rules
- Prefer **rebuild** for hosts with kernel/rootkit or unknown persistence; cleaning is for
  well-understood, user-level persistence.
- Collect a copy (and hash) of each artefact before deleting; it is evidence.
- Remove everything in the remediation window; removing piecemeal teaches the attacker.

## Verify
Re-run the same sweeps 24 h and 7 days later; zero hits for every removed mechanism, and no
new persistence appearing on reset hosts.
