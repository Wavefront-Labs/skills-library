---
id: computing-software.cybersecurity-defensive.authentik.stage-authenticator-webauthn
name: stage-authenticator-webauthn
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, webauthn, passkeys, fido2, resident-key, device-type-restrictions]
level: practitioner
status: docs-checked
description: "Configure the authentik WebAuthn/FIDO2/Passkeys authenticator setup stage: user verification, resident keys, attachment, hints, duplicates and device type allowlists."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_webauthn/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let users enrol security keys (YubiKey, Titan), platform authenticators (Windows Hello, Touch ID, Face ID) and passkeys. Enrolled devices are used later through an Authenticator Validation stage allowing the **WebAuthn** class.

## Options
**User verification** (require, prefer, discourage), **Resident key requirement**, **Authenticator Attachment**, **Hints**, **Device type restrictions**, **Maximum registration attempts** (0 = no limit), **Authenticator type name**, **Configuration flow**.

- For passwordless passkey login set Resident key requirement to **Preferred** or **Required** so the credential is discoverable.
- Authenticator Attachment: unset sends no preference; **Platform** prefers built-in; **Cross-platform** prefers roaming keys. If unset and hints are chosen, attachment is inferred: only Security key and/or Hybrid gives `cross-platform`; only Client device gives `platform`; both client-device and cross-platform gives none.
- Hints are advisory and order matters.

## Duplicates
authentik sends the user's existing credentials in `excludeCredentials`, so an authenticator already holding a credential for that account refuses a second; other users can still enrol the same device. The **Prevent duplicate devices** option was removed in 2026.8 with no replacement and needs no action on upgrade.

## Device type restrictions
Allowlist from FIDO MDS data and bundled AAGUID metadata. Empty means any. Once you select entries, newly added metadata entries are not allowed automatically, so review after upgrades. The special `authentik: Unknown devices` entry allows authenticators whose AAGUID is not in the metadata; authenticators returning no AAGUID cannot satisfy any restriction.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_webauthn/.
Removed as not confirmed by that page: signature algorithm list and FIPS mode section.
Method: documentation only; no commands were run.
