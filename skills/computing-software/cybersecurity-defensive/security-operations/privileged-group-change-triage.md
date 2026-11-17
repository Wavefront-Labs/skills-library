---
id: computing-software.cybersecurity-defensive.security-operations.privileged-group-change-triage
name: privileged-group-change-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [privileged-change-triage, alert-triage, active-directory, entra-id, privileged-access, event-4728, soc]
level: practitioner
status: docs-checked
description: "Triage alerts for changes to privileged groups (Domain Admins, Entra Global Administrator, cloud admin roles): validate change, actor, method and roll back if unauthorised."
sources: ["https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-audit-activities", "https://attack.mitre.org/techniques/T1098/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Privileged group change alert triage

Privilege escalation via group membership (ATT&CK T1098 Account Manipulation) is a key step in
domain and tenant compromise.

## Signals
- AD: 4732 (member added to a security-enabled local group) and 4733 (removed), plus the equivalent
  events for global and universal groups (look the IDs up in Microsoft's auditing reference);
  target groups Domain Admins, Enterprise Admins, Schema Admins, Administrators, Account
  Operators, Backup Operators, DnsAdmins, Group Policy Creator Owners. Microsoft's guidance on
  4732/4733 is to monitor additions to high-value groups such as domain and enterprise admins.
  5136 (directory service object modified) and 4662 also cover changes to the AdminSDHolder object.
- Entra ID audit: the RoleManagement activity "Add member to role", and the ApplicationManagement
  activity "Add owner to service principal".
- Other cloud IAM (AWS, Azure subscription roles): alert on admin-level policy or role grants; the
  event names are provider specific, so take them from that provider's audit log reference.

## Triage steps
1. Who made the change (`SubjectUserName`, initiatedBy), from which host/IP, at what time.
2. Is there a change ticket or PIM request with approval? Was it via the normal admin path
   (PAW, PIM) or an odd host?
3. Who was added? New account? Service account? Account created minutes earlier is high risk.
4. Has the added account used the privilege yet (logons to DCs, DCSync: 4662 showing the "Replicating Directory Changes" rights (ATT&CK T1003.006),
   GPO changes)?
5. Actor account health: recent anomalous sign-ins, password resets, MFA changes.

## Response
- Unauthorised: remove membership, disable the added account and the actor account if compromise
  suspected, reset passwords (and krbtgt considerations if DA used), revoke tokens; open incident.
- Authorised but outside process: close as benign, notify the admin's manager; feed process gap.

## Gotchas
- Nested group adds (group added into a privileged group) are easy to miss; alert on any
  membership change of privileged groups including groups as members.
- Logs from all DCs are required; a single unforwarded DC hides the event.

## Verify
Membership after response matches the approved baseline (export members and diff); timeline
in the case shows actor, change, use, and rollback.

## Checked
2026-11-09. Read: Microsoft Learn security auditing pages for events 4732, 4733, 5136 and 4662,
Appendix B privileged accounts and groups in AD (group names), the Entra audit activities reference
("Add member to role", "Add owner to service principal"), ATT&CK T1098 and T1003 (Replicating
Directory Changes). Removed unconfirmed claims: event IDs 4728/4729/4756/4757 (their pages did not
load), Entra role names Privileged Role Administrator and Application Administrator, AWS and Azure
policy and role event names, PIM-outside-process signal, replication GUIDs.
Method: documentation only; no commands were run.
