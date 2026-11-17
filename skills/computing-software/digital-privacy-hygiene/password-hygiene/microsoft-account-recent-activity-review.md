---
id: computing-software.digital-privacy-hygiene.password-hygiene.microsoft-account-recent-activity-review
name: microsoft-account-recent-activity-review
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, microsoft-recent-activity, microsoft-account, sign-in-activity]
level: practitioner
status: draft
description: "Read Microsoft account Recent activity, tell normal sign-ins from attacks, use This wasn't me, and lock down access after unfamiliar sign-ins."
sources:
  - "https://support.microsoft.com/account-billing"
  - "https://account.live.com/activity"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microsoft account recent activity review

**Goal:** know whether anyone signed in to the account that holds your Outlook mail, OneDrive and Windows keys.

## Open it
account.microsoft.com > **Security** > **Sign-in activity** (or account.live.com/activity). Expand each entry to see
the date, location, browser/app, platform and whether it succeeded.

## Read entries
- **Successful sign-in** from an unfamiliar country or device: treat as compromise unless it is your VPN exit or
  mobile carrier's IP.
- **Unsuccessful sign-in / incorrect password**: someone has your email address and is guessing or credential
  stuffing; not a compromise by itself but a reason to check for reuse.
- **Unusual activity** flagged by Microsoft with a prompt to secure the account.
- Sync activity from Outlook mobile, Windows or Xbox appears as separate app entries; that is normal.

## If it wasn't you
1. Click **Secure your account** (or "This wasn't me") and follow the password change.
2. Security > Advanced security options: remove unknown phone numbers, emails and authenticator apps; delete **app
   passwords**; turn on two-step verification.
3. Sign out everywhere: Advanced security options > **Sign out everywhere**.
4. Check Outlook rules and forwarding, and OneDrive sharing.
5. Consider going passwordless (remove the password, use Authenticator or passkeys) to stop password spraying.

## Gotchas
- Location is IP-based and often wrong by a region; focus on the device and browser too.
- A continuous stream of failed sign-ins can be stopped by adding a sign-in alias and blocking sign-in with the
  primary email (Manage how you sign in).
