---
id: computing-software.digital-privacy-hygiene.password-managers.securing-the-vault-account-with-two-step-login
name: securing-the-vault-account-with-two-step-login
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-account-2fa, vault-account-security, bitwarden-two-step-login, 1password-two-factor, recovery-code, security-keys, new-device-verification]
level: practitioner
status: draft
description: "Turn on two-step login for the password manager account itself, with a security key or TOTP stored outside the vault and the recovery code printed."
sources:
  - "https://bitwarden.com/help/setup-two-step-login/"
  - "https://bitwarden.com/help/two-step-recovery-code/"
  - "https://support.1password.com/two-factor-authentication/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Two-step login on the vault account

**Goal:** stop someone who learns your master password (shoulder surfing, keylogger,
reuse) from downloading your vault onto their own device.

## What it protects (and doesn't)
- Protects the **login/download** step on a new device.
- Does **not** add protection to an already-stolen encrypted vault (that is master
  password + KDF only), and doesn't protect an unlocked vault on a compromised device.
- 1Password's Secret Key already blocks new-device login without the kit; 2FA is still
  worth adding.

## Bitwarden
1. Web vault > Settings > Security > **Two-step login**.
2. Best: **FIDO2 WebAuthn** (security key or passkey); register two keys. Alternative:
   authenticator app. Avoid email as the only method.
3. **View recovery code** immediately and print it. It disables all two-step methods
   if you lose them; Bitwarden support cannot bypass two-step login for you.
4. Note: Bitwarden also does new-device verification by email for accounts without
   two-step login; that is not a substitute.

## 1Password
Account > My Profile > More actions > Manage Two-Factor Authentication; add an
authenticator app and/or security keys. Store the TOTP in a **different** app than
1Password itself.

## The circular-dependency rule
The vault's second factor must not live **only** inside the vault. Keep:
- the TOTP seed in a separate authenticator app (or a hardware key), and
- the recovery code on paper with the emergency kit.

## Gotchas
- Prove you can log in again by signing in from a fresh browser profile while your
  main device stays signed in; only then trust the setup.
- Duo or email methods tie vault access to another account's security.

## Verify
- [ ] Fresh browser profile: login prompts for second factor and succeeds.
- [ ] Recovery code printed, stored with emergency kit, not in the vault.
