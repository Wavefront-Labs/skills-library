---
id: computing-software.cybersecurity-defensive.identity-access-management.adfs-hardening
name: adfs-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [adfs-hardening, ad-fs, adfs-migration, golden-saml, extranet-smart-lockout, federation-protocols, entra-id]
level: advanced
status: gated
description: "Harden AD FS (extranet smart lockout, token-signing key protection, auditing, WAP) and migrate apps and domains to Entra ID to retire it, closing Golden SAML risk."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/best-practices-securing-ad-fs", "https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/configure-ad-fs-extranet-smart-lockout-protection", "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/migrate-adfs-apps-stages", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-008a"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD FS hardening and migration

AD FS servers hold the token-signing key: steal it and you can forge SAML tokens for any user to any
federated app, including M365 (Golden SAML). Treat them as tier 0.

## Harden
- Tier 0: AD FS servers administered only from PAWs, same protection as DCs; no internet browsing.
- Web Application Proxy (WAP) in the DMZ; AD FS farm never exposed directly.
- Extranet Smart Lockout:
  ```
  Set-AdfsProperties -EnableExtranetLockout $true -ExtranetLockoutThreshold 15 `
    -ExtranetObservationWindow (New-TimeSpan -Minutes 30)
  Set-AdfsProperties -ExtranetLockoutMode AdfsSmartLockoutEnforce
  ```
  Threshold lower than the AD lockout threshold so AD accounts are not locked by internet sprays.
- Disable endpoints you do not use. Keep `/adfs/services/trust/2005/usernamemixed` and `/adfs/services/trust/13/usernamemixed` enabled on the proxy if hybrid or Entra joined devices need PRT renewal; windowstransport must not be exposed to the extranet.
- Auditing: `Set-AdfsProperties -AuditLevel Verbose` (the default is Basic), plus the local audit policy for application-generated events; forward the AD FS audit events to the SIEM.
- Token-signing key: protect it (HSM where supported) and lock down access to it.
- Patch promptly; monitor for unexpected relying party trust or claim rule changes.

## Migrate to Entra ID (retire AD FS)
1. Inventory relying parties and use the AD FS application activity report in Entra to check migration readiness.
2. Recreate apps as Entra enterprise apps (SAML/OIDC), translate claim rules, apply Conditional Access.
3. Move authentication for domains from federated to managed: password hash sync (+ Seamless SSO) or certificate-based auth; staged rollout by group.
4. Convert domains (Entra Connect or Microsoft Graph) and decommission AD FS, revoking its certificates.

## Gotchas
- After a suspected compromise, rotate the token-signing certificate twice and revoke tokens (gated: unconfirmed, source is paywalled or blocked).
- Federated domain conversion triggers re-authentication; schedule and communicate.

## Verify
- [ ] Extranet lockout in enforce mode; legacy endpoints disabled on the proxy.
- [ ] AD FS audit events in the SIEM.
- [ ] Migration plan with RP inventory and target date.

## Checked

2026-10-28. Confirmed against the AD FS extranet smart lockout page, the AD FS auditing levels page and the Entra PRT page: Set-AdfsProperties with ExtranetLockoutThreshold, ExtranetObservationWindow, AdfsSmartLockoutEnforce and AuditLevel (Basic default); usernamemixed endpoints are required on the proxy for PRT renewal and windowstransport must not be exposed to the extranet. Gated: rotate the token-signing certificate twice (CISA AA21-008A returned 403). Removed: SolarWinds attribution, event ids 1200-1203, DKM claim, ExtranetLockoutRequirePDC, cmdlet names for relying party inventory and domain conversion, and the incorrect advice to disable usernamemixed unconditionally.

Method: documentation only; no commands were run.
