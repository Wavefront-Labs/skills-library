---
id: computing-software.digital-privacy-hygiene.password-hygiene.reviewing-email-sessions-and-devices
name: reviewing-email-sessions-and-devices
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, email-session-review, account-security, gmail, session-management]
level: practitioner
status: draft
description: "List and sign out active sessions and devices on Gmail, Outlook, iCloud and Proton, read the activity details, and spot a persistent attacker session."
sources:
  - "https://support.google.com/mail/answer/45938"
  - "https://myaccount.google.com/device-activity"
  - "https://support.microsoft.com/account-billing"
  - "https://proton.me/support/log-out-all-devices"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reviewing active sessions and devices on email

**Goal:** confirm nobody else is signed in to the account that can reset all your other accounts.

## Where to look
| Provider | Path |
|---|---|
| Gmail / Google | myaccount.google.com > Security > **Your devices** > Manage all devices; Gmail web footer > **Last account activity: Details** (IP, access type, concurrent sessions) |
| Outlook / Microsoft | account.microsoft.com > Devices; Security > Sign-in activity |
| iCloud | Settings > [name] > device list; appleid.apple.com > Devices |
| Proton | Settings > Security and privacy > **Session management** |
| Yahoo / AOL | Account security > Recent activity |
| Fastmail | Settings > Privacy & Security > Connected apps and sessions |

## What to look for
- Devices or browsers you don't own, unfamiliar cities or ISPs (VPN exits look odd; consider your own VPN use).
- IMAP/POP/"mail client" access types you don't use: an attacker can sync your mail with an app password.
- App passwords and third-party app access that you didn't create.

## Clean up
1. Change the password first (from a clean device), then **sign out all other sessions** (Gmail Details page
   "Sign out all other web sessions"; Proton "Revoke all other sessions"; Google remove each device).
2. Delete app passwords and revoke third-party access.
3. Check forwarding, filters and delegation, which survive a password change.
4. Re-enable or tighten 2FA; prefer passkeys/security keys.

## Habit
Review quarterly and after travel, a lost device, or any phishing click.
