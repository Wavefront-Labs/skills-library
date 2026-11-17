---
id: computing-software.cybersecurity-defensive.identity-access-management.enterprise-password-manager-rollout
name: enterprise-password-manager-rollout
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [password-policy, enterprise-password-manager, bitwarden, 1password, keeper, shared-vaults, sso-integration, credential-hygiene, passkeys]
level: practitioner
status: draft
description: "Roll out an enterprise password manager: product requirements, SSO and recovery design, shared vaults for teams, migration from browsers and spreadsheets, and offboarding."
sources: ["NIST SP 800-63B (password managers and paste)", "CISA guidance - Use a password manager", "CIS Control 5.2 (unique passwords)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enterprise password manager rollout

**Goal:** every employee uses unique, generated passwords for everything not covered by SSO,
and teams share credentials through controlled vaults instead of chat and spreadsheets.

## Requirements to check in the product
- End-to-end encryption with zero-knowledge architecture; published security audits.
- SSO integration (SAML/OIDC) for unlock or login, with a recovery design that does not let the provider or a single admin read vaults.
- SCIM provisioning and deprovisioning from the IdP.
- Shared collections/vaults with role-based permissions and access logs.
- Admin policies: enforce master password strength / passkey unlock, MFA, block personal vault export, restrict browser extension to company accounts.
- Event logs to SIEM; passkey storage support.

## Rollout
1. Pilot with IT and security; build shared vaults for admin credentials first (with PAM for the most privileged).
2. Define vault structure: per team, owners, who can view vs view-and-reveal.
3. Migrate: import from browser stores, then disable browser password saving by policy
   (Chrome `PasswordManagerEnabled=false`, Edge `PasswordManagerEnabled=false`).
4. Train with a short how-to; champions per department.
5. Track adoption (active users, weak/reused password reports from the product).

## Recovery and offboarding
- Account recovery via admin-approved recovery or organisation recovery keys; test it.
- Offboarding: SCIM deactivation; rotate any shared credentials the leaver could see (the product's access log tells you which).

## Gotchas
- Personal and work vaults mixed in one account create offboarding disputes; use separate organisation accounts.
- Browser extension auto-fill on look-alike or compromised pages: require exact domain matching, disable auto-fill on page load.
- A password manager is not a PAM: no just-in-time, no session recording for domain admin credentials.

## Verify
- [ ] Adoption above target (e.g. 90% of staff active monthly).
- [ ] Browser built-in password saving disabled on managed devices.
- [ ] Leaver test shows deprovisioning and shared credential rotation list.
