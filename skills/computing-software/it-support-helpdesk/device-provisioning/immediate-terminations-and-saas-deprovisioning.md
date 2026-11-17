---
id: computing-software.it-support-helpdesk.device-provisioning.immediate-terminations-and-saas-deprovisioning
name: immediate-terminations-and-saas-deprovisioning
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, immediate-termination, saas-deprovisioning, credential-rotation, offboarding, hostile-termination, access-revocation]
level: practitioner
status: draft
description: "Offboard hostile or urgent terminations: coordinated cut-off, session revocation, SaaS deprovisioning beyond SSO, and rotating shared credentials the leaver knew."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access"
  - "https://learn.microsoft.com/en-us/entra/identity/app-provisioning/how-provisioning-works"
  - "https://www.cisa.gov/topics/physical-security/insider-threat-mitigation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# immediate-terminations-and-saas-deprovisioning

## Coordinate timing with HR
For terminations with risk (misconduct, disgruntled, access to sensitive data), IT acts
at the moment HR tells the person, not after. Agree a time, a named HR contact, and
whether to preserve data for legal hold. Keep the ticket restricted (not visible to the
whole desk).

## Cut-off sequence (minutes, not days)
1. Disable the account in AD (and Entra for cloud-only); hybrid: also disable in Entra
   or wait for sync is too slow, so do both.
2. **Revoke sessions**: `Revoke-MgUserSignInSession -UserId user@contoso.com`; refresh
   tokens die immediately, access tokens within up to an hour (Continuous Access
   Evaluation shortens it for supporting apps).
3. Reset password (twice for on-prem Kerberos considerations), remove MFA methods and
   registered devices; disable or wipe mobile devices (selective wipe for BYOD).
4. Block VPN/remote access, remove from privileged groups and PIM eligibility.
5. Disable badge (facilities) at the same time.
6. Collect hardware in the meeting where possible.

## SaaS deprovisioning beyond SSO
- SSO-protected apps are blocked once the account is disabled, but existing app sessions
  and **local accounts** (apps with their own passwords, API tokens, personal access
  tokens) remain.
- Use SCIM deprovisioning where available (disables/deletes the app account).
- Maintain an app inventory with owners and "how to remove access" per app; walk the
  list for each leaver (or let identity governance tools do it).
- Transfer ownership of data in SaaS (shared drives, repositories, CRM records) before
  deletion.

## Rotating shared credentials
- Any secret the leaver knew must be rotated: shared admin accounts, Wi-Fi PSK (if
  shared), service account passwords, vault entries they accessed, door codes, alarm
  codes, social media accounts, API keys they created.
- The password vault's access history shows which entries they viewed.
- Hostile cases: review recent activity (mail forwarding rules, mass downloads, new
  OAuth app consents, new accounts created) and report to security.

## Verify
Sign-in logs show no successful sign-ins after cut-off, the SaaS inventory shows each app
deprovisioned, and the rotation list is complete with dates.
