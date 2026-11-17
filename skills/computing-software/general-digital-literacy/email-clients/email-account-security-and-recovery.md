---
id: computing-software.general-digital-literacy.email-clients.email-account-security-and-recovery
name: email-account-security-and-recovery
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, two-factor-authentication, recovery-email, recovery-phone, account-recovery, compromised-account, password-reset, app-passwords, security-checkup, gmail-security, outlook-security, suspicious-login, backup-codes]
level: intro
status: docs-checked
description: "Set up two-factor authentication and real recovery options on an email account before you need them, and move fast when you suspect it's been hacked."
sources:
  - https://support.google.com/accounts/answer/185839
  - https://support.google.com/accounts/answer/1187538
  - https://support.google.com/mail/answer/45938
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Email account security and recovery — your email is the master key

**Goal:** harden the account that nearly every other password-reset flow points to, and
know the exact steps if it shows signs of compromise — because a hacked email account
lets an attacker reset passwords on everything else you own. Steps below are for a
Google account; for Microsoft, Apple or another provider, use that provider's own help.

## 1. Why email security matters more than any other account
Almost every "forgot password" flow for banking, shopping and social accounts sends a
reset link to email. Losing control of email is effectively losing control of
everything connected to it — treat it as the highest-priority account to secure.

## 2. Two-factor authentication, done properly
- Google Account: Security & sign-in › turn on 2-Step Verification and follow the
  prompts. Work or school accounts may need an administrator.
- Google lists these second steps: passkey, Google prompts (recommended), hardware
  security key, authenticator or verification-code app, text/voice codes, QR code and
  backup codes. It notes text and voice codes are more vulnerable to phone-number-based
  hacks than other options, and that a hardware key helps protect against phishing.
  Prefer those other options where offered.
- **Backup codes:** each set has 10 single-use codes; creating a new set makes the old
  one inactive. Google suggests printing them and keeping them with important
  documents, or downloading them, and never sharing them. Get them under 2-Step
  Verification › Backup codes. Store them somewhere other than the inbox they protect.

## 3. Recovery information that actually works
Add a recovery phone and a separate recovery email, and keep them current: recovery
relies on proof of ownership, and stale details are what lock people out. Check your
provider's help for the exact settings and its security checkup tool.

## 4. Recognising a compromised account
Watch for: password reset emails you didn't request, sent-mail you don't recognise,
contacts reporting spam "from you," a login notification from an unfamiliar location or
device, or being logged out unexpectedly. In Gmail on a computer, click **Details** in
the bottom right corner to open "Activity on this account": it shows concurrent
sessions, the access type (browser, device or mail server such as POP or IMAP) and the
last 10 IP addresses with approximate locations. Several locations can be normal (POP/
IMAP clients, Mail Fetcher, phone carriers can look unfamiliar).

## 5. If it's compromised — act in this order
1. **If you still have access:** change the password immediately (to something new, not
   a variant of the old one), then check recent activity and connected apps, then
   confirm 2FA and recovery info weren't altered.
2. **Check your mail filters and forwarding settings** for rules you didn't create, and
   delete them. Look up the exact location in your provider's help.
3. **If locked out:** use the provider's account recovery flow from its sign-in page.
4. Warn contacts through another channel that the account was compromised, since the
   attacker may message them "as you" before you regain control.

## Verify
- [ ] 2FA is on, via a passkey, prompts, key or authenticator app rather than SMS where
      available.
- [ ] Backup codes are stored somewhere other than the inbox itself.
- [ ] Recovery phone and recovery email are both current, not stale.
- [ ] You know where to check forwarding rules and recent sign-in activity on this
      provider before you ever need to.

## Checked
2026-11-01. Confirmed from Google Account Help (2-Step Verification options and SMS
caveat, backup codes: 10 per set, single use, storage advice) and Gmail Help (Details
link, Activity on this account contents, change password if unrecognised). Removed:
Microsoft and Apple paths, SIM-swap wording, app-specific passwords, Gmail forwarding
menu paths, Outlook rules, account.live.com recovery URL and the Google recovery-phone
page, which returned 404.
Method: documentation only; no commands were run.
