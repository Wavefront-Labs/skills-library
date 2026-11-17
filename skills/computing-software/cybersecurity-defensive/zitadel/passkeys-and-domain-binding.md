---
id: computing-software.cybersecurity-defensive.zitadel.passkeys-and-domain-binding
name: passkeys-and-domain-binding
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, passkeys, webauthn, fido2, custom-domain, passwordless]
level: practitioner
status: docs-checked
description: "Roll out ZITADEL passkeys with the domain-binding caveat, user self-service management and native app association files."
sources:
  - https://zitadel.com/docs/concepts/features/passkeys
  - https://zitadel.com/docs/guides/manage/console/default-settings
  - https://zitadel.com/docs/guides/manage/console/applications-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Passkeys give passwordless login based on public-key cryptography, in the family of FIDO2 and WebAuthn. Users prove themselves with a device biometric or PIN. They resist phishing, and a password login remains available for people without a passkey.

Two types exist. Device-bound ones depend on the device, such as fingerprint, face recognition or Windows Hello. Independent ones are hardware tokens such as a Yubikey or Solokey. In the login settings, passkeys need U2F with PIN enabled under multifactors; the documentation states there is no other option at the moment.

Users register, view and delete their passkeys in ZITADEL's self-service interface. Administrators can create a passkey registration link through the API.

Key operational point: passkeys are bound to your domain. Configure a custom domain before you set up passkeys, as the documentation recommends.

Native iOS and Android apps that use platform passkey APIs also need domain association files. Configure these on the OIDC application under Native App Links, and ZITADEL publishes `/.well-known/apple-app-site-association` (iOS: Team ID and Bundle ID) and `/.well-known/assetlinks.json` (Android: package name and SHA-256 certificate fingerprints).

Check browser and platform support for your audience, as passkey support is still evolving.

## Checked

2026-11-08. Read in full: the passkeys concept page, the default settings page and the applications page. The native app links filenames are confirmed on the applications page.

Method: documentation only; no commands were run.
