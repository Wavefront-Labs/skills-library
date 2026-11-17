---
id: computing-software.digital-privacy-hygiene.two-factor-auth.microsoft-account-two-step-verification
name: microsoft-account-two-step-verification
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, microsoft-account-2fa, mfa-rollout, multi-factor-authentication, microsoft-authenticator, recovery-code, outlook-com, security-info]
level: intro
status: docs-checked
description: "Turn on two-step verification on a personal Microsoft account (Outlook, Xbox, OneDrive), keep three pieces of security info and use app passwords for old apps."
sources:
  - "https://support.microsoft.com/en-us/account-billing/how-to-use-two-step-verification-with-your-microsoft-account-c7910146-672f-01e9-50a0-93b4585e7eb4"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft account two-step verification

**Goal:** lock down a consumer Microsoft account, which often holds OneDrive files,
Outlook mail and device recovery information.

## Steps
1. Sign in at `account.microsoft.com/security` and choose **Manage how I sign in**.
2. Under Additional security and **Two-step verification**, choose **Turn on** and follow
   the screen. You will be given a QR code to scan to set up the Authenticator app, which
   confirms you physically hold the device.
3. Register security info: an email address (Microsoft suggests two different ones, your
   usual address and a backup), a phone number, or any authenticator app.
4. Microsoft strongly recommends having **three pieces of security info** on the account.

## What changes
- With two-step verification on, you get a security code by email, phone or authenticator
  app every time you sign in on a device that is not trusted.
- You always need two forms of identification: if you forget the password you need two
  contact methods, and if you lose your contact method the password alone will not get
  you back in. Regaining access can take 30 days, and you may lose the account.
- Microsoft is phasing out SMS as an authentication and recovery method for personal
  accounts, so do not make a phone number your only method.

## Password reset with 2SV on
You can reset the password if Microsoft has two ways to contact you; you will receive two
security codes instead of one.

## App passwords
Some apps (mail apps on some phones) and devices (Xbox 360) cannot use security codes. If
you see "incorrect password" after turning on 2SV, create an app password for that app.
App passwords exist only while 2SV is on. Create them only when needed.

## Related
- Going fully passwordless:
  `computing-software.digital-privacy-hygiene.two-factor-auth.going-passwordless-on-a-microsoft-account`

## Verify
- [ ] Two-step verification shows as on in Manage how I sign in.
- [ ] Three pieces of security info are registered.

## Checked
Checked 2026-11-08 against the Microsoft support page "How to use two-step verification
with your Microsoft account". The recent sign-in activity source returned 404 and was
removed with the sign-in activity section. Removed: the printed recovery code step and
BitLocker recovery key details, which the cited page does not cover.

Method: docs-only read of cited pages, 2026-11-08
