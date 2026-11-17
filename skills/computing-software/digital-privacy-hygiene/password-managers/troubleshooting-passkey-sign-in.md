---
id: computing-software.digital-privacy-hygiene.password-managers.troubleshooting-passkey-sign-in
name: troubleshooting-passkey-sign-in
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, passkey-troubleshooting, passkeys, hybrid-transport]
level: practitioner
status: draft
description: "Fix passkey sign-ins that fail: wrong provider prompt, missing credential, QR hybrid flow not connecting, Bluetooth off, and safe fallback steps."
sources:
  - "https://bitwarden.com/help/storing-passkeys/"
  - "https://support.google.com/accounts/answer/13548313"
  - "https://support.apple.com/en-us/102195"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Troubleshooting passkey sign-in

**Goal:** sign in when the passkey flow misbehaves, without reverting to SMS.

## Symptom > cause > fix
| Symptom | Likely cause | Fix |
|---|---|---|
| OS dialog appears, your manager doesn't | Extension locked or passkey setting off | Unlock the manager, enable passkey handling, retry |
| "No passkeys available for this site" | Passkey saved in a different provider or a different account | Check the other provider; use "Use another device"/QR |
| QR scan on phone spins forever | Bluetooth off on either device, or no internet | Turn Bluetooth on both; hybrid needs BLE proximity plus internet |
| Prompt asks for a security key you don't have | Site only knows a hardware-key credential | Use the backup key or password+other MFA |
| Works in Chrome, not Firefox | Browser lacks provider integration | Use the extension or switch browser for that site |
| Passkey deleted at provider, site still offers it | Site remembers credential ID | Remove it in the site's security settings and re-create |

## Native app sign-in
Apps use the OS credential provider; set your manager as preferred (credential provider settings).

## Fallbacks in order
1. Another passkey (different device/provider) registered on the account.
2. Security key.
3. Password + TOTP.
4. Account recovery flow.
Make sure at least two of these exist before deleting a password.

## Gotchas
- Corporate devices may block BLE, breaking hybrid; use a security key.
- Clearing browser data doesn't remove passkeys from a manager but can remove Chrome profile passkeys
  if they were local-only.
