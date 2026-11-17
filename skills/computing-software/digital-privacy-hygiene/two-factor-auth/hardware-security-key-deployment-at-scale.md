---
id: computing-software.digital-privacy-hygiene.two-factor-auth.hardware-security-key-deployment-at-scale
name: hardware-security-key-deployment-at-scale
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, fido2, security-keys, yubikey, resident-credentials, discoverable-credentials, webauthn, pin-policy, key-revocation, lost-key-response, family-key-rollout, nfc-security-key]
level: advanced
status: draft
description: "Deploy FIDO2 hardware security keys across several accounts or several people: resident vs non-resident credentials, PIN policy choices, and what to actually do when a key is lost."
sources:
  - "https://developers.yubico.com/YubiKey/Concepts/"
  - "https://fidoalliance.org/fido2/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware security key deployment at scale

**Goal:** roll out FIDO2 hardware keys across a real number of accounts (and,
for a family, across several people) with a deliberate choice about credential
storage and PIN policy, and a tested response for the inevitable lost or broken
key — not just "buy two keys" left unexplained, as covered at the basic level in
`computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`.

## 1. Resident (discoverable) vs. non-resident credentials
- **Non-resident credential**: the key stores an encrypted blob the *relying
  party* (the website) hands back to the key on each login; the credential
  itself isn't enumerable by just having the key. This was the original FIDO
  U2F model and most keys can store effectively unlimited non-resident
  credentials across sites.
- **Resident (discoverable) credential**: the key stores the credential
  itself, enabling **passwordless** sign-in (the site just asks "who are you,"
  the key supplies username + credential together) without typing a username
  first. Most consumer keys (e.g. YubiKey 5 series) have a **limited slot count**
  for resident credentials (commonly around 25, varies by model/firmware) —
  this matters once you're registering a key across many accounts for
  passwordless/passkey-style sign-in specifically, as opposed to using it as a
  pure second factor layered on a password, which doesn't consume a resident
  slot.
- Practical implication: if you want one key to be a true passkey across dozens
  of accounts, check the model's resident-credential limit before committing,
  or accept that older-style "password + security key as 2FA" doesn't hit this
  limit at all.

## 2. FIDO2 PIN policy
- Setting a PIN on the key itself (prompted on first use with most managers) is
  what makes the key a true **two-factor** device — "something you have" (the
  key) plus "something you know" (the PIN) — rather than just a bearer token
  anyone who finds it could use.
- A forgotten PIN typically requires a **factory reset of the key**, which
  erases all stored resident credentials on it — this is why every account
  needs a **second** registered method (another key, or a platform passkey)
  before you lean on PIN-protected resident credentials as your only path in.
- Repeated wrong PIN attempts can lock a key, sometimes permanently (varies by
  vendor/model) — treat the PIN with the same care as a short password, written
  down securely, not improvised at the login prompt.

## 3. The two-key minimum, properly executed
- Register **both** keys on **every** account at setup time, not "key one now,
  key two later" — many sites make adding a second key clunky once you're
  already logged in with the first, and some don't let you add a key at all
  without already having one registered method active, creating a chicken-and-egg
  problem if you only bought one.
- Store the keys in genuinely different locations (on your person vs. a fire
  safe at home, or with a trusted person) — "both in the same desk drawer"
  defeats the redundancy's actual purpose (fire, theft, loss of the one bag
  that had both).
- For NFC-capable keys used with phones, verify NFC actually works with each
  account's login flow before relying on it exclusively — some sites' WebAuthn
  implementations handle NFC smoothly, others are USB-only in practice despite
  claiming FIDO2 support.

## 4. Rolling out across a family or small team
- Buy keys **in bulk from one batch/vendor** so firmware behaviour is
  consistent, and label them physically (a key's own LED/branding rarely
  distinguishes "Mum's backup key" from "Dad's backup key" once several are in
  a drawer).
- Keep a simple written (non-digital, or in the password manager as a note —
  never as a plain list left in an inbox) record of **which key is registered
  on which account for which person** — when a key is lost, you need to know
  exactly what to revoke without guessing.
- For a small team/organisation requiring keys (e.g. GitHub, Google Workspace
  admin console, a cloud provider's root account), budget for a **spare pool**
  of pre-provisioned keys so a lost key doesn't leave someone locked out while a
  replacement ships.

## 5. Lost or broken key — the actual response
1. **Revoke that specific key's registration** on every account it was
   registered to, immediately — don't wait to see if it turns up; a key that's
   lost (not just misplaced at home) should be assumed found by someone else.
2. Sign in using the **second** registered key or backup method to do the
   revocation — this is exactly why step 3 of section 3 (both keys registered
   from day one) matters; without it you're stuck in account-recovery flows
   instead of a clean revoke.
3. Register a new replacement key on the same accounts once acquired, restoring
   the two-key minimum.
4. A PIN-protected key found by a stranger is far less exploitable than an
   unprotected one (section 2) — but still revoke; don't rely on the PIN alone
   as the response.

## Gotchas
- Confusing "I lost a key" with "I'll just use my remaining one factor forever"
  — a single remaining key is itself now a single point of failure; replace it
  promptly.
- Factory-resetting a key to fix a forgotten PIN erases resident credentials
  silently — know this before you reset one that's registered anywhere as a
  passwordless/resident credential.
- Uncertain: resident-credential slot counts and PIN-lockout behaviour vary by
  specific key model and firmware version — check the vendor's current specs
  for the model actually purchased.

## Verify
- [ ] Every account has two keys registered from day one, not a plan to add a
      second one "later."
- [ ] A FIDO2 PIN is set on every key, recorded securely, and known not to be
      recoverable if forgotten.
- [ ] The two keys per account are stored in genuinely separate physical
      locations.
- [ ] A written record exists of which key maps to which account/person,
      stored securely, so a loss triggers a clean revoke rather than a guess.
