---
id: computing-software.digital-privacy-hygiene.password-managers.vault-timeout-and-biometric-unlock-settings
name: vault-timeout-and-biometric-unlock-settings
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-timeout, biometric-unlock, pin-unlock, lock-vs-logout, bitwarden, keepassxc, auto-lock]
level: practitioner
status: docs-checked
description: "Set Bitwarden session timeout, lock versus log out action, PIN and biometric unlock, plus KeePassXC Quick Unlock, so the vault is locked when you are away."
sources:
  - "https://bitwarden.com/help/vault-timeout/"
  - "https://bitwarden.com/help/biometrics/"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault timeout and unlock settings

**Goal:** keep the vault from staying unlocked while you are away, without making unlocking so
painful you turn the protection off.

## Bitwarden session timeout
- Set it per account under Settings > Security or Account security (macOS: Bitwarden > Settings;
  Windows or Linux desktop: File > Settings). Inactivity is time since you last interacted with
  Bitwarden, not system idle time. Closing the desktop app locks or logs out per your action.
- Options vary by app: Immediately, Time passed, Custom (hours and minutes), On system lock (device
  locked or screensaver activates), On browser restart (extension), On app restart (mobile), On
  system idle, On system sleep, On restart (desktop), On browser refresh (web app), Never.
- **Never** stores your encryption key unencrypted on the device; Bitwarden strongly recommends
  another option.
- An Enterprise organisation may set a session timeout policy that removes options.
- Popped-out browser extensions do not observe the timeout setting.
- Edge: On browser restart only fires if Startup Boost and "Continue to run background
  extensions and applications after Microsoft Edge is closed" are off. On Chromebooks and snap
  Firefox it fires only when the device restarts.
- Web app: refreshing locks it; closing the tab logs it out. Closing the browser window logs out
  the web app and times out the extension.

## Timeout action
- **Lock** (default) keeps vault data on the device; unlock works offline with master password,
  PIN or biometrics, and no two-step login.
- **Log out** removes all vault data from the device; logging back in needs the master password,
  any active two-step login method, and a connection.
- With trusted devices you must enable biometrics or a PIN, otherwise a timeout always logs out.

## PIN
- The extension normally requires the master password after the browser window closes. To use the
  PIN instead, uncheck "Lock with master password on browser restart" when setting the PIN.

## Bitwarden biometrics
- Biometric data never goes to Bitwarden; native OS APIs validate on the device. Settings are per
  account.
- Desktop: Windows Hello (Settings > Security > Unlock with Windows Hello; the Microsoft Store
  install does not support it), macOS Touch ID, Linux needs a polkit agent. Optional "Require
  master password or PIN on app restart" (Windows) controls whether biometrics works after a
  restart; after first opening or restarting, unlock once with the master password or PIN.
- Browser extension biometrics need the desktop app running and logged in, with biometrics set
  up there first. Supported: Chromium browsers, Firefox 87+ (not ESR), Safari 14+. Chromium
  browsers may need "Allow access to file URLs" on. Enable under Account security > Unlock with
  biometrics, and allow the native-application permission prompt.
- "Require verification for browser integration" in the desktop app asks for the fingerprint
  each time the integration activates.
- Mobile: Touch ID or Face ID; Android needs a Class 3 biometric.

## KeePassXC Quick Unlock
On Windows and macOS (hardware permitting), credentials are stored for biometric unlock, enabled
by default (Windows Hello; Touch ID or Apple Watch). Disable it in Application Settings >
Security. It is set up after you unlock with full credentials; a hardware key must still be
connected to unlock.

## Verify
- [ ] Lock the OS or let the timeout expire: the vault is locked on return.
- [ ] After restarting the app or browser, the setting you chose (master password or PIN) is asked.

## Checked

Date 2026-11-08. Pages read: Bitwarden Automatic Logout or Lock, Bitwarden Unlock with Biometrics, KeePassXC User Guide (Quick Unlock section). Removed as not on those pages: the recommended baseline table and its timings, the 1Password auto-lock section (the cited page could not be read), the KeePassXC "lock after N seconds" and lid-closed settings, the claim that PIN is brute-forceable after reboot, and the advice to audit partners' enrolled biometrics.

Method: docs-only read of cited pages, 2026-11-08
