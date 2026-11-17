---
id: computing-software.digital-privacy-hygiene.two-factor-auth.windows-hello-passkeys
name: windows-hello-passkeys
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, windows-hello-passkeys, passkey-enrollment, platform-passkeys, passkeys, windows-hello, device-bound-passkey, windows-11]
level: intro
status: docs-checked
description: "Use passkeys with Windows Hello on Windows 11, know the device-bound versus synced difference, and plan a second authenticator in case the PC is lost."
sources:
  - "https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422"
  - "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Hello passkeys

**Goal:** use passkeys on a Windows PC knowing their recovery limits.

## How they work
A passkey is a key pair: the private key stays on your device and the public key is
registered with the site. To sign in, the device signs a challenge after you unlock the
private key with Windows Hello (PIN, fingerprint or face) and the site checks the
signature. Windows Hello credentials are asymmetric and generated within the isolated
environment of the device's TPM; the PIN never leaves the device. Biometric data stays on
the local device. Passkeys are tied to the site's domain, so they resist phishing.

## Device-bound or synced
- **Device-bound:** stored only on the device where it was created and not synced. If you
  lose the device you lose the passkey unless you have another recovery method or a backup
  passkey.
- **Synced:** saved in a credential manager such as Microsoft Password Manager (rolling
  out, Edge version 142 or newer with a personal profile) or a third-party provider, and
  available on your other devices.
- Cross-device sign-in lets a passkey on a phone sign you in on another device through a QR
  code, with a proximity check.
- Work or school devices and accounts may limit options. Newer passkey features need
  Windows 11 and updates.

## Recovery planning
Microsoft's tip: save passkeys to a synced credential manager where possible; if you keep
one on one device, create passkeys on your other devices too as a digital spare key. For
each site also keep a second authenticator (a phone passkey, a FIDO2 hardware security key)
or recovery codes.

## Windows Hello and local accounts
Windows Hello with a local account is not backed by an asymmetric key and offers a lower
level of security than with a Microsoft account or a FIDO2 identity provider.

## Verify
- [ ] The site shows the passkey registered and sign-in prompts Windows Hello.
- [ ] Every site that relies on a device-bound passkey has a second authenticator registered.

## Checked
Checked 2026-11-08 against Microsoft's passkeys support page and the Windows Hello for
Business overview. Removed: Settings menu paths for managing passkeys, the claim that
clearing the TPM destroys Hello keys and needs a BitLocker key, and third-party provider
names, which the pages do not state.

Method: docs-only read of cited pages, 2026-11-08
