---
id: computing-software.digital-privacy-hygiene.password-hygiene.checking-mailbox-delegation-and-shared-access
name: checking-mailbox-delegation-and-shared-access
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, mailbox-delegation, email-account-security, mail-forwarding-rules]
level: practitioner
status: draft
description: "Find and remove mailbox delegates, forwarding addresses, filters and app access that give someone continuing access to your email."
sources:
  - "https://support.google.com/mail/answer/138350"
  - "https://support.google.com/mail/answer/10957"
  - "https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/give-mailbox-permissions-to-another-user"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mailbox delegation and shared access

**Goal:** catch the access paths that survive a password reset: delegates, forwarding and rules.

## Gmail
- Settings > **Accounts and Import** > "Grant access to your account": delegates can read, send and delete mail without
  your password. Remove anyone you don't expect.
- Settings > **Forwarding and POP/IMAP**: remove unknown forwarding addresses; turn off POP/IMAP if unused.
- Settings > **Filters and Blocked Addresses**: look for filters that forward, delete, or skip the inbox for mail
  containing "password", "security", "invoice", or your bank's name.
- Google account > Security > third-party apps with Gmail access.

## Outlook / Microsoft 365
- Outlook.com: Settings > Mail > **Forwarding** and **Rules**.
- Work (Microsoft 365): an admin can grant Full Access, Send As or Send on Behalf; in Outlook, File > Account
  Settings > Delegate Access shows delegates you added. Ask IT to check mailbox permissions and inbox rules if you
  suspect compromise; attackers add rules that move replies to RSS Feeds or Archive.

## Apple iCloud Mail
icloud.com > Mail > Settings > **Rules** and forwarding.

## Legitimate sharing
For an assistant or partner, use delegation (revocable, logged) rather than sharing your password. Review the list
when relationships or jobs change.

## Verify
After cleanup, send yourself a test message containing "password reset" and confirm it lands in the inbox and is not
forwarded.
