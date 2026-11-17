---
id: computing-software.digital-privacy-hygiene.two-factor-auth.reviewing-sign-in-alerts-and-activity
name: reviewing-sign-in-alerts-and-activity
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, sign-in-activity-review, revoke-sessions, account-recovery]
level: practitioner
status: draft
description: "Read sign-in alerts and security activity logs for Google, Microsoft, Apple and social accounts, tell real alerts from phishing, and act on them."
sources:
  - "https://support.google.com/accounts/answer/3067630"
  - "https://support.microsoft.com/account-billing/what-is-the-recent-activity-page-9f6a3a83-9bb3-4b77-9e2b-3f8ac1f2d6a7"
  - "https://support.apple.com/en-us/102664"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reviewing sign-in alerts and activity

**Goal:** catch account takeovers early by actually reading the logs that big providers keep.

## Where to look
| Account | Path |
|---|---|
| Google | myaccount.google.com > Security > Recent security activity; Your devices |
| Microsoft | account.microsoft.com > Security > Sign-in activity (account.live.com/activity) |
| Apple | Settings > [your name] > device list; appleid.apple.com > Devices |
| Facebook/Instagram | Accounts Center > Password and security > Where you're logged in |
| GitHub | Settings > Security log; Sessions |
| Password manager | Bitwarden: Settings > Security > Devices; 1Password: Settings > Devices |

## Reading entries
- Location from IP is approximate; VPN/mobile carriers show odd cities. Check device type and time instead.
- "Unsuccessful sign-in" with correct password but failed 2FA = someone has your password: change it.
- New recovery email/phone added you didn't add = takeover in progress.

## Real alert vs phishing
Never click the alert's link; open the account directly (typed URL or app) and check activity there.

## Act
1. Change password from a trusted device.
2. Sign out all other sessions/devices.
3. Remove unknown recovery methods and app passwords/OAuth grants.
4. Check email forwarding rules.

## Gotchas
- Logs have limited retention (often 28-30 days); review monthly.
- Family members' devices on a shared account look like "unknown" sessions; name your devices.
