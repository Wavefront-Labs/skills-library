---
id: computing-software.digital-privacy-hygiene.two-factor-auth.passkeys-via-android-credential-manager
name: passkeys-via-android-credential-manager
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, android-credential-manager, platform-passkeys, google-password-manager-passkeys]
level: practitioner
status: draft
description: "Use Android's Credential Manager for passkeys: choose the provider, understand Google Password Manager sync and PIN, and fix apps that won't offer passkeys."
sources:
  - "https://developer.android.com/identity/sign-in/credential-manager"
  - "https://support.google.com/accounts/answer/13548313"
  - "https://security.googleblog.com/2024/09/passkeys-on-android-and-chrome-sync.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Passkeys via Android Credential Manager

**Goal:** passkeys on Android go to the provider you choose and sync where you expect.

## The pieces
- **Credential Manager** (Android 14+, backported via Play services) is the system sheet apps and Chrome call
  for passwords and passkeys.
- **Providers:** Google Password Manager (default) plus third-party managers (Bitwarden, 1Password, Proton Pass,
  Dashlane...).

## Set the provider
Settings > Passwords, passkeys & accounts (Samsung: General management > Passwords, passkeys and autofill):
**Preferred service** = your manager; keep Google as an additional provider if you want both.

## Google Password Manager passkeys
- End-to-end encrypted sync across Android and Chrome desktop. On new devices you unlock them with an
  existing device's screen lock or a **Google Password Manager PIN**; set that PIN when prompted and store it
  in your vault.
- Manage at passwords.google.com.

## Creating a passkey in an app
App's account settings > Create passkey > Credential Manager sheet > choose provider > screen lock.

## Troubleshooting
| Problem | Fix |
|---|---|
| Only Google offered | Third-party manager not enabled as provider, or app doesn't support passkeys yet |
| "No passkeys" on new phone | GPM passkeys not yet unlocked: enter the GPM PIN or old device screen lock |
| Work profile | Has its own provider setting |

## Gotchas
- Older Android versions route through Play services; update Play services and the provider app.
- Samsung Pass is another provider; disable it if you don't use it to avoid confusing prompts.
