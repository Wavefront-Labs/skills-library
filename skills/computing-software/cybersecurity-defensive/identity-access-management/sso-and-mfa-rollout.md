---
id: computing-software.cybersecurity-defensive.identity-access-management.sso-and-mfa-rollout
name: sso-and-mfa-rollout
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [identity-access-management, iam, sso, single-sign-on, saml, oidc, openid-connect, mfa, phishing-resistant-mfa, fido2, webauthn, passkeys, conditional-access, entra-id, okta, break-glass-accounts, emergency-access, legacy-authentication, scim, provisioning, number-matching, aitm, token-theft]
level: practitioner
status: draft
description: "Roll out SSO (SAML/OIDC) and phishing-resistant MFA with conditional access, break-glass accounts, legacy auth blocked and SCIM provisioning, without locking anyone out."
sources: ["NIST SP 800-63B Digital Identity Guidelines - Authentication", "CISA - Implementing Phishing-Resistant MFA fact sheet", "Microsoft Entra ID documentation - Conditional Access and emergency access accounts", "OASIS SAML 2.0 and OpenID Connect Core 1.0 specifications", "RFC 7644 SCIM Protocol"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSO and MFA rollout — one front door, hard to phish

**Goal:** put every application behind the identity provider (IdP), require MFA that
survives adversary-in-the-middle phishing for everyone who matters, and close the
side doors (legacy protocols, local accounts) — while keeping a tested way back in.

## 1. Inventory and sequence
Export sign-in logs (Entra ID sign-in logs, Okta System Log, Google Workspace audit)
for 30 days. List apps, auth protocol, user counts, and who uses legacy protocols
(IMAP/POP/SMTP AUTH, ActiveSync basic, NTLM-only apps). Order: admins first, then
high-risk groups (finance, HR, execs, IT), then everyone.

## 2. Create break-glass accounts first
- Two cloud-only emergency accounts (not synced from on-prem AD), on the tenant's
  default domain, with the top admin role, long random passwords split and stored
  offline (safe) or protected by FIDO2 keys held in separate locations.
- Exclude them from conditional access policies that could lock you out (or, per
  current Microsoft guidance, require phishing-resistant MFA for them — check docs,
  since Entra now enforces MFA on admin portals).
- Alert on *any* sign-in by these accounts. Test them quarterly and log the test.

## 3. Integrate apps with SSO
- **OIDC** for modern/web/mobile apps: authorisation code flow with PKCE; validate
  `iss`, `aud`, `exp`, `nonce`; short ID token lifetimes.
- **SAML 2.0** for enterprise SaaS: signed assertions (SHA-256), validate audience and
  recipient, NameID stable (immutable ID, not email if emails change), certificate
  rollover reminders 60 days before expiry.
- Turn off local/password logins in each app once SSO works, keeping one local admin
  as that app's break-glass if the vendor allows.
- **SCIM 2.0** provisioning from the IdP so leavers are deprovisioned automatically;
  SSO alone doesn't kill existing app sessions or API tokens.

## 4. Choose MFA methods by strength
1. **Phishing-resistant:** FIDO2 security keys, platform passkeys (Windows Hello for
   Business, Touch ID/Face ID, Android), certificate-based auth / smart cards. Bound
   to the origin, so an AiTM proxy can't relay them.
2. **Acceptable interim:** push with number matching and app context, TOTP.
3. **Avoid:** SMS and voice — retire them except as a monitored recovery option.
Require phishing-resistant methods for admins and high-risk groups; offer passkeys to all.

## 5. Conditional access baseline (Entra names; Okta has equivalents)
- Require MFA for all users, all cloud apps (start in *report-only*, review 1–2 weeks).
- Require authentication strength "phishing-resistant MFA" for admin roles.
- **Block legacy authentication** (client apps: Exchange ActiveSync and Other clients).
- Require compliant or hybrid-joined device for sensitive apps.
- Block or require step-up for high sign-in/user risk (needs Entra ID P2 or equivalent).
- Secure MFA registration itself: require trusted location or Temporary Access Pass for
  first registration — attackers register their own MFA on stolen passwords.
Exclude break-glass accounts and documented service accounts (move those to workload
identities/managed identities rather than excluding indefinitely).

## 6. Roll out to users
Pilot group (IT) → 10% → departments, with comms 2 weeks ahead, a self-service
registration campaign, helpdesk script for identity verification on resets (call
back on a known number, manager approval — never reset MFA on caller say-so).

## Gotchas
- Report-only mode hides nothing — read it. Unknown service accounts and printers using SMTP AUTH surface there.
- MFA does not stop token theft; enable token protection / session binding where
  available, shorten session lifetimes for admins, and revoke sessions on incident.
- Helpdesk social engineering is the main bypass of strong MFA; harden the reset process.
- Federated domains: if MFA is done on-prem (AD FS), conditional access may trust
  the claim — verify where MFA actually happens.
- SAML apps that also expose an API key or app password bypass SSO entirely.

## Verify
- [ ] Two break-glass accounts exist, are excluded/protected correctly, alert on use, and were tested this quarter.
- [ ] Legacy authentication sign-ins over the last 30 days are zero (or each has a dated exception).
- [ ] All admins can only sign in with phishing-resistant MFA.
- [ ] Apps behind SSO have local logins disabled and SCIM deprovisioning tested with a leaver.
- [ ] MFA registration requires a trusted context or Temporary Access Pass.
- [ ] Helpdesk MFA-reset procedure includes out-of-band identity verification.

Related: computing-software.cybersecurity-defensive.security-architecture.zero-trust-segmentation
