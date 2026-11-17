---
id: computing-software.general-digital-literacy.internet-navigation.authenticator-apps
name: authenticator-apps
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, passwords, two-factor-authentication, authenticator-app, totp, google-authenticator, microsoft-authenticator, number-matching, mfa-fatigue]
level: intro
status: docs-checked
description: "Set up an authenticator app (Microsoft, Google Authenticator, Authy, password managers) for two-step sign-in, back it up, move it to a new phone and avoid MFA fatigue tricks."
sources:
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - https://www.cisa.gov/secure-our-world
  - https://support.google.com/accounts/answer/1066447
  - https://support.microsoft.com/en-us/authenticator/back-up-your-accounts-in-microsoft-authenticator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticator apps

**Goal:** stronger two-step verification than text messages, without getting locked out.

## Why
SMS codes can be stolen by SIM-swap fraud and phishing. Authenticator apps generate a 6-digit
code every 30 seconds on your phone (TOTP), or show a push prompt to approve.

## Set up
1. Install one: **Microsoft Authenticator**, **Google Authenticator**, Authy/Twilio, or the TOTP
   feature in a password manager (1Password, Bitwarden).
2. On the website: Security settings › Two-step verification › Authenticator app › a **QR code** appears.
3. In the app: + › scan the QR code › type the 6-digit code shown back into the website.
4. Save the **backup/recovery codes** the site offers (print or password manager).
5. Google: a newly added authenticator can take up to 7 days to appear as a sign-in option; this delay is deliberate security.

## Back up and new phones
- Google Authenticator: sign in to the app with your Google Account and codes sync to the new phone, or on the old phone use Menu › **Transfer codes** › **Export codes**, then Import codes on the new phone by scanning the QR. Using the app without an account keeps codes on that device only.
- Microsoft Authenticator: Settings › turn on **Cloud Backup** (Android: a Microsoft personal account; iOS: iCloud Drive, iCloud Keychain and iCloud Backup must be on), then restore on the new phone. You can only restore on the same device type (iOS to iOS, Android to Android). Passwordless credentials and work or school accounts are not backed up: you sign in again. Microsoft says Android backup moves to Google One from January 2027.
- Before wiping the old phone, check every account works on the new one.

## Push approvals
- Only approve a prompt if **you** are signing in right now. Repeated unexpected prompts = someone
  has your password (MFA fatigue attack): deny, then change the password.
- Number matching (type the number shown on screen into the app) prevents blind approvals.

## Verify
- [ ] Sign out and back in to an important account using the app; recovery codes stored safely.

## Checked

Checked 2026-10-27 against Google Account Help (Google Authenticator, answer 1066447) and Microsoft Support (back up one-time password codes in Microsoft Authenticator). Confirmed: Google Authenticator code sync by signing in, Menu > Transfer codes > Export codes, the up-to-7-day delay for a new authenticator; Microsoft Cloud Backup steps, same-device-type restore, passwordless and work or school credentials not backed up, and the January 2027 Android change.

Method: documentation only; no commands were run.
