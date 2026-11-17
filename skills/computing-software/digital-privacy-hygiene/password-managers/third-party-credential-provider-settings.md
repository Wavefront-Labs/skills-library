---
id: computing-software.digital-privacy-hygiene.password-managers.third-party-credential-provider-settings
name: third-party-credential-provider-settings
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, credential-provider-settings, mobile-autofill-service, passkeys]
level: practitioner
status: draft
description: "Set a third-party password manager as the system credential provider for passwords and passkeys on iOS, Android 14+, macOS and Windows 11."
sources:
  - "https://support.apple.com/guide/iphone/automatically-fill-in-strong-passwords-iphf9219d8c9/ios"
  - "https://developer.android.com/identity/sign-in/credential-manager"
  - "https://bitwarden.com/help/auto-fill-ios/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Third-party credential provider settings

**Goal:** apps and browsers offer your password manager's logins and passkeys, not only the OS keychain.

## iOS / iPadOS 17+
Settings > General > AutoFill & Passwords (iOS 18+; older: Settings > Passwords > Password Options).
- Turn on your manager under "AutoFill From"; you can keep Passwords (iCloud Keychain) on too.
- Passkey creation offers the enabled providers; pick yours.

## Android 14+
Settings > Passwords, passkeys & accounts (wording varies by OEM).
- Set the **Preferred service** to your manager; Google Password Manager can remain as an additional provider.
- Chrome: Settings > Autofill services > "Autofill using another service" so Chrome uses the system provider.

## macOS 14+
System Settings > General > AutoFill & Passwords > enable the manager's app extension. Safari passkey prompts
then include it.

## Windows 11
Settings > Accounts > Passkeys > Advanced options: enable a supported third-party passkey manager plug-in where
available (recent Windows 11 builds). Otherwise passkeys go to Windows Hello unless the browser extension
intercepts.

## Verify
- Create a test passkey on webauthn.io from a native browser: your manager's sheet appears.
- In a native app with a login form, the keyboard bar shows your manager's suggestion.

## Gotchas
- After reinstalling the manager app the provider toggle is often reset; recheck.
- Work profiles on Android have a separate provider setting.
