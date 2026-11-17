---
id: computing-software.cybersecurity-defensive.cloud-security.entra-m365-tenant-compromise-response
name: entra-m365-tenant-compromise-response
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-incident-response, tenant-compromise-response, entra-id, microsoft-365, session-revocation, oauth-app-persistence, federation-backdoor, global-admin-compromise]
level: advanced
status: draft
description: "Respond to an Entra ID / Microsoft 365 tenant compromise: contain privileged accounts, revoke sessions and tokens, hunt persistence (apps, federation, CA changes) and recover."
sources: ["Microsoft Learn - Incident response playbooks (compromised and malicious applications, password spray, app consent)", "CISA/NSA guidance on detecting post-compromise threat activity in Microsoft cloud environments", "Microsoft Learn - Revoke user access in an emergency in Microsoft Entra ID"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entra ID / Microsoft 365 tenant compromise response

**Goal:** remove an attacker with privileged access to your Microsoft cloud tenant, including
the persistence they add, without locking yourself out.

## Contain (first hours)
1. Use **break-glass accounts** or verified clean admin accounts from clean devices (PAW).
2. For compromised users: reset password (twice if on-prem synced), **revoke sessions**
   (`Revoke-MgUserSignInSession -UserId <id>`), disable account if needed, require MFA re-registration, remove attacker-registered authentication methods.
3. Remove attacker from privileged roles; review **all** role assignments, including PIM eligible assignments and administrative units.
4. Block attacker IPs/locations via Conditional Access temporarily; enforce phishing-resistant MFA for admins.

## Hunt persistence
| Persistence | Where to look |
|---|---|
| New/modified app registrations and service principals with credentials | Entra audit logs: "Add service principal credentials", "Update application - Certificates and secrets" |
| OAuth consent grants with broad scopes | Enterprise apps > permissions; audit "Consent to application" |
| Federated domain added or federation settings changed (forged SAML tokens) | "Set domain authentication", "Set federation settings on domain" |
| Conditional Access policies weakened or exclusions added | CA audit events |
| New users, guest invites, group owner changes | Audit logs |
| Mailbox rules, forwarding, delegates, transport rules | Exchange audit / UAL |
| Partner relationships (GDAP/DAP) and cross-tenant access settings | Admin center, audit logs |
| Azure subscriptions: new owners, automation accounts, VMs | Azure activity log |
Tools: Microsoft Defender XDR advanced hunting, CISA **Untitled Goose Tool**, **Microsoft-Extractor-Suite**, Sentinel.

## Eradicate and recover
Remove persistence found, rotate secrets of all apps with high privileges, re-verify federation
configuration, restore CA policies from known-good (Git) copies, and monitor closely for 30+ days.

## Gotchas
- Revoking sessions does not invalidate already-issued access tokens (valid up to ~1 hour, longer for some apps) except where continuous access evaluation applies.
- Investigating with a compromised admin account tips off the attacker; use clean accounts.
- Logs have limited default retention; export early (see Unified Audit Log skill).

## Verify
- [ ] Re-hunt after eradication shows no new attacker activity for the monitoring period.
- [ ] Privileged role membership matches an approved list.
