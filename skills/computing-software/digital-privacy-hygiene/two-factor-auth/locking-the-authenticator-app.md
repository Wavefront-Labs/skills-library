---
id: computing-software.digital-privacy-hygiene.two-factor-auth.locking-the-authenticator-app
name: locking-the-authenticator-app
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, authenticator-app-lock, authenticator-app, aegis, phone-theft, stolen-device-protection]
level: intro
status: docs-checked
description: "Protect 2FA codes from a thief who knows your phone passcode: use an authenticator with its own vault lock and turn on iPhone Stolen Device Protection."
sources:
  - "https://getaegis.app/"
  - "https://support.apple.com/en-us/120340"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locking the authenticator app

**Goal:** close the gap where someone who has your phone and has seen your passcode can read every 2FA code or
change your account settings.

## Lock the authenticator itself
- Choose an authenticator whose vault is encrypted and locks separately from the phone. Aegis (Android) describes
  its token vault as encrypted, with optional biometric unlock, and asks for a PIN or biometrics to lock the app.
- Where an app offers its own PIN or password, use one different from the phone passcode, because the threat is
  someone who already knows the passcode.
- Look in each app's own settings for lock, tap-to-reveal or screenshot-blocking options; menu names differ by app
  and version.

## Pair with OS-level protection (iPhone)
Apple's Stolen Device Protection (iOS 17.3 or later; must be on before the phone is lost or stolen) adds
requirements when the iPhone is away from familiar locations such as home or work:
- Some actions, such as accessing stored passwords and credit cards, need Face ID or Touch ID with no passcode
  fallback.
- Some actions, such as changing your Apple Account password, need a one-hour security delay and a second biometric
  check.
- Turn it on in Settings > Face ID (or Touch ID) & Passcode > Stolen Device Protection. It needs two-factor
  authentication on the Apple Account, a passcode, Face ID or Touch ID, Significant Locations and Find My.
- Choosing "Always" under Require Security Delay applies the extra measures even at familiar locations.
- Turn it off before you sell, give away or trade in the phone.

## Gotchas
- A biometric lock that falls back to the passcode is only as strong as the passcode a thief has watched you type.

## Verify
- [ ] With the phone unlocked, opening the authenticator asks for its own PIN or biometric.
- [ ] Stolen Device Protection shows as on (iPhone).

## Checked
2026-11-01. Confirmed on Apple Support "About Stolen Device Protection for iPhone" and the Aegis site (encrypted
vault, optional biometric unlock, PIN/biometric lock). Removed: per-app menu paths for Aegis, Ente, 2FAS, Google and
Microsoft authenticators, Android Theft protection and Identity Check, auto-lock timings, widget claim (not in the
pages read; the Ente help page was a stub).
Method: documentation only; no commands were run.
