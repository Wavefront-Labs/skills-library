---
id: computing-software.cybersecurity-defensive.identity-access-management.hardware-security-key-rollout
name: hardware-security-key-rollout
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [mfa, hardware-security-keys, fido2, webauthn, phishing-resistant-mfa, yubikey, passkeys]
level: practitioner
status: docs-checked
description: "Roll out FIDO2 hardware security keys for phishing-resistant MFA: key selection, attestation and AAGUID restrictions, enrolment, backups, conditional access and lifecycle."
sources: ["https://fidoalliance.org/fido2/", "https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-enable-passkey-fido2", "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware security keys

**Goal:** phishing-resistant MFA (FIDO2/WebAuthn) for admins and high-risk users first,
then broadly, so AiTM phishing kits cannot relay authentication.

## Why keys
FIDO2 binds the credential to the site origin: a phishing proxy on a look-alike domain
cannot get a valid assertion. Hardware keys add non-exportable private keys and a physical
presence check. NIST SP 800-63B AAL3 is based on proof of possession of a key through a cryptographic protocol.

## Choose keys
- FIDO2 certified, with USB-A/USB-C and NFC as needed (phones), optional biometric models.
- Stick to a small number of models and record their **AAGUIDs**.
- Issue **two keys** per user (primary + backup stored safely) to avoid help-desk recovery.

## IdP configuration
- Entra: Authentication methods > Passkey (FIDO2): enable for groups; **enforce attestation**
  and **restrict to specific AAGUIDs** so only approved hardware keys register (device-bound
  passkeys in Authenticator can be allowed separately).
- Other IdPs (Okta, Google Workspace): check each vendor's documentation for FIDO2 enforcement.
- Conditional access: authentication strength "Phishing-resistant MFA" required for admin
  roles, admin portals, and sensitive apps; later for all users.

## Enrolment
- Pre-registered keys (provisioned by IT, shipped to users) or self-service with a Temporary
  Access Pass. Require PIN on the key (user verification).
- Windows sign-in with security keys: see the Entra passkey (FIDO2) article for device and policy requirements.

## Lifecycle
- Track key serial/AAGUID per user in the IdP; revoke on loss (delete the method) and on
  leaving.
- Lost key: user signs in with the backup key and registers a replacement; no fallback to SMS.
- Remove weaker methods (SMS, voice, OTP) for users with keys, or they remain the phishable path.

## Gotchas
- Legacy protocols and apps not supporting modern auth bypass FIDO entirely; block legacy auth.
- Shared workstations and VDI need USB redirection support for keys.
- Mobile-only users may be better served by device-bound passkeys.

## Verify
Sign-in logs show phishing-resistant methods for all admin sign-ins; a test login through an
AiTM lab proxy fails; users in the enforced groups have no SMS/voice methods registered.

## Checked

2026-10-28. Confirmed against the Entra passkey (FIDO2) page, the FIDO Alliance page and NIST SP 800-63B: attestation enforcement and key restrictions by AAGUID in passkey profiles, device-bound passkeys, origin-bound credentials, AAL3 based on proof of possession of a key. Removed: CISA claim (page returned 403), Okta and Google Workspace configuration bullet, Windows sign-in and Kerberos cloud trust requirement bullet.

Method: documentation only; no commands were run.
