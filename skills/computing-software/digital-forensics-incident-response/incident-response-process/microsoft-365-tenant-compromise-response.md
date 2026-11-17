---
id: computing-software.digital-forensics-incident-response.incident-response-process.microsoft-365-tenant-compromise-response
name: microsoft-365-tenant-compromise-response
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [m365-tenant-compromise, cloud-incident-response, azure-incident-response, entra-id, dfir]
level: advanced
status: docs-checked
description: "Respond to a Microsoft 365 / Entra tenant compromise: preserve audit logs against short retention, review tenant-level persistence areas, contain and verify."
sources: ["https://learn.microsoft.com/en-us/security/operations/incident-response-playbooks", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention", "https://learn.microsoft.com/en-us/purview/audit-solutions-overview", "https://learn.microsoft.com/en-us/powershell/module/exchange/search-unifiedauditlog", "https://github.com/cisagov/untitledgoosetool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft 365 tenant compromise response

**Goal:** when an attacker holds Global Admin or equivalent, the whole tenant is in scope: mail, files, identities, apps and federation.

## Preserve first
- Microsoft Entra audit and sign-in logs are kept 7 days on Entra ID Free and 30 days on P1 and P2. They are separate from the Microsoft 365 Unified Audit Log (UAL), whose retention is managed through Microsoft Purview Audit. Route Entra logs to an Azure storage account via Azure Monitor (or, with the licences Microsoft lists, Purview Audit Premium) to keep them longer. Retention changes are not retroactive, so export now.
- Microsoft Graph activity logs are not retained unless archived to storage or an analytics tool.
- UAL: Audit (Standard) records are kept 180 days. With Audit (Premium), Entra ID, Exchange, OneDrive and SharePoint records are kept one year by default and other activities 180 days unless a retention policy extends them; retention policies cannot be retroactive.
- Search the UAL in the Purview portal, with `Search-UnifiedAuditLog` (returns up to 100 records by default; `-SessionCommand ReturnLargeSet` searches exhaustively up to 50,000 results and returns unsorted data), or the Office 365 Management Activity API, which also lets you keep data longer and feed a SIEM.
- CISA's Untitled Goose Tool gathers telemetry for investigations against Microsoft Entra ID, Azure and M365 environments; it needs read-only tenant permissions and its config can dump Entra ID audit logs and filter UAL records.
- Entra audit log entries are system generated and cannot be changed or deleted.

## Review tenant-level persistence areas
Use the audit logs (Entra audit logs record changes to applications, groups, users and licences, including who created a service principal) and the admin portals to review each area against a known baseline:
- Privileged role membership and assignments.
- Federation and domain authentication settings.
- Service principals and application credentials created or changed.
- OAuth apps with high-privilege permissions and consent grants.
- Cross-tenant access and external partner settings.
- Conditional Access policy changes.
- Exchange mail-flow (transport) rules, mailbox permissions and inbox rules.
- eDiscovery searches and exports by the attacker.
Microsoft's incident response playbooks cover phishing, password spray, app consent grant, and compromised and malicious applications; each has prerequisites, workflow, checklist and investigation steps.

## Contain
- Use a break-glass account to take control; remove attacker roles and principals; revoke sessions of all admins; rotate app credentials; restore Conditional Access; require phishing-resistant MFA for admins.
- If federation was abused, move the domain to managed authentication or replace the token-signing certificates; confirm the exact procedure in Microsoft's current guidance for your setup.

## Gotchas
- Log retention depends on licence and log type; check yours before the incident.

## Verify
Privileged role, app credential and federation inventories match an approved baseline after cleanup.

## Checked
2026-11-08: confirmed from Microsoft Learn: Entra retention table (7 and 30 days), Entra versus UAL separation, Audit Standard 180 days and Premium retention, Search-UnifiedAuditLog default and ReturnLargeSet limits, Microsoft's four playbooks, Entra audit log content, and the Untitled Goose Tool README. Removed: Hawk and Microsoft-Extractor-Suite (not on cited pages), specific Graph cmdlet and audit event names (`Get-MgDomainFederationConfiguration` and similar), the "twice" token-signing rotation claim, the "180 days on many licences" wording and the hybrid Entra Connect Tier 0 note.
Method: documentation only; no commands were run.
