---
id: computing-software.digital-privacy-hygiene.two-factor-auth.synced-vs-device-bound-passkeys
name: synced-vs-device-bound-passkeys
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, syncable-authenticators, platform-passkeys, device-bound-passkey, passkeys, nist-800-63b, aal2, aal3, sync-fabric, security-keys]
level: practitioner
status: draft
description: "Decide per account between synced passkeys (convenient, recoverable, AAL2) and device-bound passkeys on a security key (no cloud root, AAL3), per NIST 800-63B-4."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://fidoalliance.org/passkeys/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Synced vs device-bound passkeys

**Goal:** know what you're trusting with each kind.

## Definitions
- **Synced (syncable) passkey**: private key copied, end-to-end encrypted, across your
  devices by a sync fabric (iCloud Keychain, Google Password Manager, a password manager).
- **Device-bound passkey**: private key never leaves one piece of hardware (security
  key, some Windows Hello/TPM setups, enterprise-managed authenticators).

## NIST SP 800-63B-4 view
Syncable authenticators are acceptable at **AAL2** when the sync fabric protects the
keys (encryption, authenticated access to the sync account). **AAL3** requires a
non-exportable key, i.e. device-bound hardware.

## Trade-off table
| | Synced | Device-bound |
|---|---|---|
| Lose a phone | Still have it on other devices | Gone; need backup authenticator |
| Phishing resistance | Yes | Yes |
| New root of trust | Your Apple/Google/vault account | Physical possession of the key |
| Account takeover of the sync account | Attacker may restore all passkeys | No effect |
| Cost/hassle | Free, automatic | Buy 2+ keys, register each |

## Rule of thumb
- Most accounts: synced passkeys, with the sync account itself protected by
  **device-bound** keys (security keys on the Apple/Google account and vault account).
- Crown jewels (email, sync account, registrar, crypto exchange, admin consoles): device-
  bound security keys (two), optionally plus a synced passkey for convenience if your
  threat model accepts it.

## Gotchas
- Some sites request attestation and reject synced passkeys; that's the site enforcing
  device-bound.
- A synced passkey is only as strong as the weakest device that can sync it (an old
  tablet with a 4-digit passcode).

## Verify
- [ ] The accounts that sync your passkeys are protected by device-bound keys.
- [ ] Each device-bound-only account has two keys registered.
