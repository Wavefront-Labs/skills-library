---
id: computing-software.it-support-helpdesk.desktop-support.moving-a-user-to-a-new-phone
name: moving-a-user-to-a-new-phone
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, mobile-device-support, phone-migration, microsoft-authenticator, authenticator-backup, quick-start, intune-enrollment, esim-transfer, device-retire, mfa]
level: intro
status: draft
description: "Swap a user to a new phone without MFA lockout: move authenticator accounts first, transfer data, re-enrol in MDM, move eSIM, then retire and wipe the old device."
sources:
  - "https://support.microsoft.com/en-us/account-billing/back-up-and-recover-account-credentials-in-the-authenticator-app-bb939936-7a8d-4e88-bc0b-1a4c4ea3a6c5"
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://learn.microsoft.com/en-us/intune/intune-service/remote-actions/devices-wipe"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# moving-a-user-to-a-new-phone

Goal: the user walks away with a working new phone and no "I can't sign in"
call the next morning.

## Order matters
1. **MFA first, while the old phone still works.**
   - Microsoft Authenticator: on the new phone install Authenticator; user
     goes to https://aka.ms/mysecurityinfo from a PC → Add sign-in method →
     Authenticator → scan QR with new phone → set as default → delete the old
     device entry. Cloud backup restore works for personal/TOTP accounts;
     work accounts usually need re-verification anyway.
   - Third-party TOTP (Google Authenticator export QR, etc.) — move all, not
     just work.
   - Passkeys in Authenticator are device-bound — register a new one.
2. **Transfer data**: iPhone Quick Start (old and new side by side) or iCloud
   backup; Android "Copy apps & data" with cable or Google backup. Corporate-
   managed devices: managed app data doesn't migrate — it re-syncs from
   cloud.
3. **MDM enrolment**: corporate device — through ADE/zero-touch it enrols at
   setup; BYOD — install Company Portal / sign into Outlook to get app
   protection.
4. **eSIM / SIM**: eSIM transfer during setup (iOS "Transfer from nearby
   iPhone", carrier-dependent on Android) or carrier app; physical SIM swap.
5. **Check**: email, Teams, VPN, Wi-Fi certificate profile, MFA prompt,
   corporate apps.
6. **Old phone**: sign out of work apps, remove from Authenticator list,
   Intune **Retire** (BYOD — removes company data) or **Wipe** (corporate),
   remove Activation Lock / Google account (FRP) before it leaves your hands,
   update asset register.

## Gotchas
- Wiping the old phone before step 1 = MFA lockout → needs a Temporary
  Access Pass (identity verification).
- Banking/other personal 2FA apps are the user's responsibility — remind
  them.
- WhatsApp/Signal history needs their own transfer tools.

## Verify
User completes an MFA sign-in using the new phone, old device absent from
security info and Intune (or marked retired), asset record updated.
