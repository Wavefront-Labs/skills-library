---
id: computing-software.general-digital-literacy.internet-navigation.locked-out-of-an-account
name: locked-out-of-an-account
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-authentication, account-lockout, lost-2fa, backup-codes]
level: intro
status: docs-checked
description: "Get back into an account after a lost phone, a broken authenticator or too many wrong passwords, using backup codes and official recovery flows, and avoid recovery scams."
sources:
  - https://support.google.com/accounts/answer/185834
  - https://support.microsoft.com/en-us/accounts-billing/manage/how-to-recover-a-hacked-or-compromised-microsoft-account
  - https://support.apple.com/en-us/102656
  - https://support.google.com/accounts/answer/1187538
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Locked out of an account

## Too many wrong passwords
- Temporary lock: wait for the time the service states, then use *Forgot password*. Microsoft explains locked accounts at https://support.microsoft.com/en-us/accounts-billing/manage/microsoft-account-has-been-locked.

## Lost phone / broken authenticator
1. **Backup codes**: the printed or saved codes from setup (Google backup codes need 2-Step Verification to be on). Microsoft's separate account recovery code is 25 digits; creating a new one invalidates the old one.
2. **Other methods**: on the sign-in screen choose *Try another way* (Google). Google lists another signed-in phone, another phone number, a backup code, a security key or a passkey on another device. Apple: choose *Forgot password?* and follow the prompts to a trusted device or recovery factors. Microsoft: use the sign-in helper.
3. **Authenticator restore**: Microsoft Authenticator restores from cloud backup on the same device type if backup was on; Google Authenticator syncs codes when you sign in with your Google Account, or can transfer via QR export.
4. **New phone, same number**: SMS still works once the SIM/eSIM is moved.
5. Last resort: the service's **account recovery** route (Google account recovery, Microsoft sign-in helper and recovery form, Apple iforgot.apple.com). Use a familiar device and location. Expect delays: Google says up to 3-5 business days when 2-Step Verification needs extra checks; Apple says several days or more.

## Work or school accounts
- The IT help desk resets MFA; you can't self-recover usually.

## Scams
- "Account recovery experts" on social media, ads or phone numbers who ask for payment or your codes are scammers. Official recovery is free.

## Prevent next time
- Save backup codes in your password manager and on paper.
- Two methods per important account (authenticator + security key/passkey, or a second phone).
- Turn on cloud backup in the authenticator app.

## Verify
- [ ] Back in; new 2FA set up; fresh backup codes saved; old device removed from the account.

## Checked

Checked 2026-10-27 against Google Account Help (answers 1187538, 185834, 6103523), Apple Support 102656 and Microsoft Support (hacked or compromised account, locked account). Confirmed: Google alternatives list and Try another way, 3-5 business day delay, Apple Forgot password flow and several-day recovery wait, iforgot.apple.com, Microsoft sign-in helper and 25-digit recovery code.

Method: documentation only; no commands were run.
