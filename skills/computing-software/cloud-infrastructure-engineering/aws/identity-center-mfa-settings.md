---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-mfa-settings
name: identity-center-mfa-settings
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, identity-center, identity-center-mfa, mfa-enforcement-sso, passkeys-identity-center, sso, authentication]
level: practitioner
status: docs-checked
description: "Configure MFA for IAM Identity Center users: always-on vs context-aware prompting, allowed authenticator types, registration rules, and what changes with an external IdP."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/enable-mfa.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/mfa-types.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/how-to-configure-mfa-device-enforcement.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MFA in IAM Identity Center

## 1. Where MFA is enforced depends on the identity source
- **Identity Center directory** or **AD (AD Connector / Managed AD)**: Identity Center
  enforces MFA itself; settings below apply.
- **External IdP (Okta, Entra ID, Google...)**: MFA in Identity Center is not supported
  with an external IdP; the IdP enforces MFA. Configure conditional access there.
  Optionally require phishing-resistant factors in the IdP for the AWS app.

## 2. Settings (Identity Center console, Settings, Authentication, Multi-factor authentication)
**Prompt users for MFA:**
- *Every time they sign in (always-on)* - recommended for anything with production access.
- *Only when their sign-in context changes (context-aware)* - prompts on a new device or
  browser, or an unknown IP address; users can mark a device as trusted. Less friction, weaker.
- *Never (disabled)* - do not use.

**Users can authenticate with these MFA types:**
- *Security keys and built-in authenticators* (FIDO2/WebAuthn: YubiKeys, passkeys,
  Touch ID/Windows Hello). Phishing-resistant; prefer it.
- *Authenticator apps* (TOTP). Allow as fallback or disable for high-assurance orgs.

**If a user does not yet have a registered MFA device:**
- *Require them to register an MFA device at sign-in* - default for new orgs; good.
- *Require them to provide a one-time password sent by email* - not bound to a device, so it
  does not meet the bar for industry-standard MFA; transitional use only. Do not choose it if
  users need the access portal to read their email.
- *Block their sign-in* - strict; admins must register devices for users. With context-aware
  prompting, a user who ticks "This is a trusted device" is not prompted even when this is set;
  use always-on if that matters.
- *Allow them to sign in* - only during a rollout.

**Who can manage MFA devices:** allow users to register their own devices (usual), and
admins can remove a lost device from the user's account (console, Users, the user's MFA
devices); with "require registration at sign-in" the user then self-enrolls a new device at
next sign-in. A user can hold up to eight devices: two authenticator apps and six FIDO
authenticators.

## 3. Rollout plan
1. Communicate; ask users to self-register two authenticators (a security key + a
   platform passkey) before enforcement.
2. Switch "prompt" to always-on and "no device" to require registration.
3. After a grace period, disable authenticator apps if policy demands phishing resistance.
4. CLI users: all MFA types work with AWS CLI v2 and Identity Center. Session length is the
   access portal session duration (default 8 h).

## 4. Auditing
CloudTrail sign-in events `CredentialChallenge`, `CredentialVerification` and `UserAuthentication`
carry `userIdentity.additionalEventData.CredentialType` (`PASSWORD`, `TOTP`, `WEBAUTHN`,
`EXTERNAL_IDP`, `RESYNC_TOTP`, `EMAIL_OTP`; a successful `UserAuthentication` lists every type
verified, for example `PASSWORD,TOTP`). Query CloudTrail Lake for users authenticating with
EMAIL_OTP or TOTP after the cut-over date to find stragglers. MFA device management is an
Identity Store API function and is logged there; look up the exact event names in your trail.

## Gotchas
- FIDO credentials are unique to the website where they were created; re-test registered keys
  after changing the access portal URL.
- Context-aware mode trusts a device, browser and IP combination; shared jump hosts make it
  close to never prompting.
- If you use RADIUS MFA through AWS Managed Microsoft AD, enabling Identity Center MFA overrides it
  for portal sign-in only; if Identity Center MFA is disabled, RADIUS MFA governs portal sign-in.
- MFA here is separate from IAM user MFA and root MFA; audit those independently.

## Verify
- [ ] Settings show always-on, FIDO allowed, registration required (for Identity Center directory and AD sources).
- [ ] A test user without a device is forced to register before reaching the portal.
- [ ] CloudTrail Lake query shows no EMAIL_OTP authentications in the review window (if disallowed).
- [ ] Lost-device procedure documented and tested.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages on MFA for Identity Center users, configure MFA, available MFA types, configure MFA device enforcement and understanding sign-in events:
- MFA in Identity Center is not supported for external identity providers; it applies to the Identity Center directory, AWS Managed Microsoft AD and AD Connector.
- Device limits (two authenticator apps, six FIDO authenticators), FIDO and TOTP descriptions, RADIUS interaction.
- The four "no registered device" options and the trusted-device exception for Block their sign-in.
- Sign-in event names and `CredentialType` values (the earlier value `FIDO` is `WEBAUTHN`).
Removed because no page confirmed them: MFA device event names and the effect of a custom portal URL on passkeys (rewritten as a re-test step).

Method: documentation only; no commands were run.
