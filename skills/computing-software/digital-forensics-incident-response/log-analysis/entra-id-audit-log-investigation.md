---
id: computing-software.digital-forensics-incident-response.log-analysis.entra-id-audit-log-investigation
name: entra-id-audit-log-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [entra-audit-logs, entra-id, azure-ad, cloud-identity, dfir]
level: practitioner
status: docs-checked
description: "Investigate Entra ID audit logs: what they record, high-value activity names for app, role, federation and MFA changes, and Microsoft Graph export."
sources: ["https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-audit-activities", "https://learn.microsoft.com/en-us/graph/api/directoryaudit-list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra ID audit log investigation

Entra audit logs are a report of logged events in Microsoft Entra ID: changes to applications, groups, users and licenses. Entries are system generated and cannot be changed or deleted. Sign-in logs, provisioning logs and (for external tenants) sign-up logs are separate activity logs; you need the sign-in logs alongside the audit log to tie a change to an authentication.

## What an entry shows
Date and time, the service that logged it, category and activity name, status; in the details, a correlation ID, the actor and target resource, and where applicable the old and new values of changed properties. The IP address in the details is the OAuth client's IP address (the TCP peer of the service endpoint). Custom security attribute changes are on a separate Custom Security tab and need the Attribute Log Administrator or Attribute Log Reader role.

## Export through Microsoft Graph
`GET https://graph.microsoft.com/v1.0/auditLogs/directoryAudits` lists directory audits. It needs `AuditLog.Read.All` and `Directory.Read.All` (delegated or application) and supports `$filter` (eq, ge, le, startswith), `$top`, `$orderby` and `$select`; the page's own filter example is on `initiatedBy/user/id`, and entries carry `activityDateTime` and `activityDisplayName`. For retention periods and longer-term export options see the Microsoft documentation for your licence; they are not covered by the cited pages.

## High-value activities (names from the audit activity reference)
| Category | Activity | Why |
|---|---|---|
| ApplicationManagement | `Add service principal credentials`, `Update application - Certificates and secrets management` | Added credentials on an app |
| ApplicationManagement | `Consent to application`, `Add delegated permission grant`, `Add app role assignment to service principal` | Consent and permission grants |
| RoleManagement | `Add member to role` | Privilege changes |
| DirectoryManagement | `Set domain authentication`, `Set federation settings on domain` | Domain federation changes |
| UserManagement | `User registered security info`, `Admin registered security info` | Authentication method registration |
| UserManagement | `Add user`, `Reset password (by admin)` | Account creation and resets |

## Gotchas
- The actor can be an application rather than a user; follow it into the sign-in logs for that service principal.
- Read the old and new property values in the entry rather than only the activity name.
- A service principal's audit entries can say "Microsoft Substrate Management": these are Exchange Online write-backs to Entra ID, informational only.

## Verify
Each suspicious change is tied to an actor sign-in and has been reverted or documented in remediation.

## Checked
Checked 2026-11-09 against the Entra audit logs concept page, the audit activity reference (all activity names listed above, with categories) and the Graph directoryAudit list page (URL, permissions, $filter operators). Removed: retention figures (7 and 30 days), the PowerShell cmdlet, the KQL query on the `AuditLogs` table, the conditional access activity names (not found in the reference), and the threat-actor labels (Solorigate, golden SAML, illicit consent).
Method: documentation only; no commands were run.
