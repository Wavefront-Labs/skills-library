---
id: computing-software.cybersecurity-defensive.cloud-security.saas-incident-response
name: saas-incident-response
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [saas-incident-response, m365-compromise, salesforce-incident, oauth-token-theft, saas-audit-logs, third-party-breach, cloud-incident-response]
level: practitioner
status: draft
description: "Respond to SaaS application incidents: audit log sources per app, compromised accounts and OAuth/integration tokens, data export scoping, vendor breach coordination."
sources: ["https://www.cisa.gov/resources-tools/services/secure-cloud-business-applications-scuba-project", "https://help.salesforce.com/s/articleView?id=sf.event_monitoring.htm", "https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SaaS application incident response

## Typical scenarios
- Account takeover of a SaaS user (phished SSO session, local password on an app without SSO).
- Stolen OAuth/integration tokens (third-party app breach, e.g. compromised connected app with API access).
- Malicious or over-privileged OAuth app consented by users.
- Vendor-side breach notification.

## Evidence sources (enable and export before you need them)
| App | Logs |
|---|---|
| Microsoft 365 | Unified Audit Log (MailItemsAccessed, FileDownloaded, New-InboxRule), Entra sign-ins |
| Google Workspace | Admin, login, Drive, token audit logs |
| Salesforce | Setup Audit Trail, Login History, Event Monitoring (Shield) for API/report exports |
| Slack | Audit Logs API (Enterprise Grid), access logs |
| GitHub | Org audit log (incl. git events), token usage |
| Okta | System Log |
Retention on lower tiers is short; stream to the SIEM.

## Steps
1. **Contain identity:** disable/reset the user in the IdP and in the app (apps with local sessions), revoke sessions and tokens, remove attacker-added MFA methods, forwarding rules, API tokens, connected apps.
2. **Revoke integrations:** rotate the integration's client secret/tokens, disable the connected app/OAuth client, review its scopes and the data it accessed (API logs filtered by client ID / IP).
3. **Scope data access:** downloads, report exports, API bulk queries, mailbox access, files shared externally, by the compromised identity/token during the window.
4. **Persistence hunt:** new admins, new SSO/IdP configuration, new API users, webhooks, mailbox rules, delegated access.
5. **Vendor coordination:** for vendor-side breaches, get IOCs (IPs, user agents, token IDs), affected tenants, timelines; check contractual notification duties.
6. **Notify** per legal assessment of data scope.

## Gotchas
- SSO reset does not kill tokens already issued to integrations or app-local sessions.
- Many SaaS logs lack read events by default (e.g. Salesforce needs Event Monitoring for report exports).

## Verify
- [ ] Runbook per critical SaaS lists log sources, admin actions for revocation, and retention.
- [ ] All tokens/integrations in the blast radius rotated and verified unused afterwards.
