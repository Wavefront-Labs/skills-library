---
id: computing-software.systems-network-administration.windows-server.ad-change-auditing-ds-access
name: ad-change-auditing-ds-access
category: computing-software
field: systems-network-administration
product: windows-server
tags: [security-auditing, event-5136, ds-access-auditing, sacl, active-directory]
level: advanced
status: docs-checked
description: "Audit Active Directory object changes: Directory Service Changes subcategory, SACLs on OUs and AdminSDHolder, events 5136/5137/5141 and reading old/new values."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-directory-service-changes
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-5136
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing AD object changes (DS Access)

The Audit Directory Service Changes subcategory logs modifications to Active Directory objects, including the changed attribute (event 5136).

## Enable
Advanced Audit Policy on the domain controllers: DS Access > **Audit Directory Service Changes**. Failed access attempts to
AD objects are covered by the separate **Audit Directory Service Access** subcategory.

## SACLs decide what is logged
Audit policy only fires for objects whose SACL has a matching audit entry. Monitor high-value objects such as the
`CN=AdminSDHolder,CN=System,DC=domain,DC=com` container and Domain Admins group objects (both named on the event pages).

## Events
| ID | Meaning |
|---|---|
| 5136 | directory service object modified |
| 5137 | object created |
| 5138 | object undeleted |
| 5139 | object moved |
| 5141 | object deleted |

In 5136 the operation is Value Added (`%%14674`) or Value Deleted (`%%14675`); Value Deleted is typically part of a change
operation. Related events share a Correlation ID. The event data includes `SubjectUserName`, `ObjectDN` and
`AttributeLDAPDisplayName`.

## Verify
- [ ] Changing a test user's description produces a 5136 event on the DC that made the change; events reach the SIEM.

## Checked

2026-10-28. Confirmed against: Audit Directory Service Changes and event 5136 pages (events 5136-5141, Value Added %%14674 / Value Deleted %%14675, Correlation ID, AdminSDHolder, Audit Directory Service Access subcategory, event data field names). Removed (not confirmable from the cited pages): event 4738 comparison, SACL PowerShell example, DCSync/GPO/Tier 0 object list, noise statements, Get-WinEvent parsing script and OperationType field name.

Method: documentation only; no commands were run.
