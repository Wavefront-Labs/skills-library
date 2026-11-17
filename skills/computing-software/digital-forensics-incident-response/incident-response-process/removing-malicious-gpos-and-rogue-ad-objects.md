---
id: computing-software.digital-forensics-incident-response.incident-response-process.removing-malicious-gpos-and-rogue-ad-objects
name: removing-malicious-gpos-and-rogue-ad-objects
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [malicious-gpo, eradication, active-directory, persistence-removal, dfir]
level: advanced
status: docs-checked
description: "Find and remove attacker-modified GPOs and check AdminSDHolder and protected-group permissions during Active Directory eradication, preserving evidence first."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-c--protected-accounts-and-groups-in-active-directory", "https://attack.mitre.org/techniques/T1484/001/", "https://learn.microsoft.com/en-us/powershell/module/grouppolicy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing malicious GPOs and rogue AD objects

**Goal:** attackers use Group Policy to push payloads and weaken defences, and persist through AD permission changes that survive password resets.

## Why GPOs
MITRE ATT&CK T1484.001 says adversaries modify GPOs to subvert access controls and often escalate privileges. GPOs are stored under `\\<DOMAIN>\SYSVOL\<DOMAIN>\Policies\`, and a malicious GPO can implement many behaviours: scheduled tasks, disabling tools, tool transfer, account creation, service execution. Documented examples: a scheduled task written to `<GPO_PATH>\Machine\Preferences\ScheduledTasks\ScheduledTasks.xml` (for instance by the public script New-GPOImmediateTask), and a user right such as SeEnableDelegationPrivilege set in `<GPO_PATH>\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf`, which would let an attacker-controlled account modify GPOs. ATT&CK lists ransomware and wiper operators among users of this technique.

## Triage with the GroupPolicy module
The Microsoft GroupPolicy module (installed with RSAT) provides:
- `Get-GPO` to list one or all GPOs; `Get-GPOReport` to produce XML or HTML for one or all GPOs; `Get-GPPermission` to see who holds permissions on a GPO; `Get-GPInheritance` for inheritance on a domain or OU.
- `Backup-GPO` to back up one or all GPOs; `Remove-GPLink` to unlink; `Remove-GPO` to delete; `Restore-GPO` and `Import-GPO` if you need to restore a known-good one.

Suggested order (practice): report and back up each suspect GPO as evidence, check its permissions and the files under its SYSVOL path, unlink it so it stops applying, then delete it and any dropped files.

ATT&CK's detection note: look for GPO container changes (such as gPCFileSysPath), delegation assignments and SYSVOL writes to files like ScheduledTasks.xml and GptTmpl.inf. Its mitigation suggestions: audit GPO permission abuse with tools such as BloodHound, and consider WMI and security filtering to narrow where a GPO applies.

## Protected accounts and AdminSDHolder
Microsoft's Appendix C lists protected accounts and groups, including Account Operators, Administrator, Administrators, Backup Operators, Domain Admins, Domain Controllers, Enterprise Admins, Enterprise Key Admins, Key Admins, Krbtgt, Print Operators, Read-only Domain Controllers, Replicator, Schema Admins and Server Operators.
- AdminSDHolder (`CN=AdminSDHolder,CN=System,DC=...`) holds template permissions for them. SDProp runs every 60 minutes by default on the PDC Emulator and resets any protected object's permissions to match AdminSDHolder. So an extra permission entry an attacker places on AdminSDHolder is propagated to every protected account and group; review its ACL against a known-good baseline, and review protected-group membership.
- To test AdminSDHolder changes without waiting, Microsoft documents running SDProp manually through Ldp.exe (the `RunProtectAdminGroupsTask` rootDSE attribute set to 1). Do not shorten the interval in production.

## Not covered by the cited pages
Rogue accounts, SID history, delegation attributes, shadow credentials, DCSync rights and AD CS templates are common eradication checks, but none of the cited pages detail them; use other sources and a baseline comparison.

## Verify
Re-run the permission and membership comparison after cleanup and confirm replication has carried the removal to all DCs.

## Checked
Dated 2026-11-08. Confirmed against MITRE ATT&CK T1484.001 (technique description, file paths, detection and mitigations), Microsoft Learn Appendix C (protected groups list, AdminSDHolder, SDProp 60 minute default on the PDC Emulator, manual run) and the GroupPolicy module cmdlet list. Removed as unstated: event IDs 5136/5137, Get-GPO property names, ms-DS-MachineAccountQuota, DCSync and SIDHistory queries, msDS-AllowedToActOnBehalfOfOtherIdentity, msDS-KeyCredentialLink, ESC1, PingCastle, and the PDC-emulator remediation advice.
Method: docs-only read of cited pages, 2026-11-08
