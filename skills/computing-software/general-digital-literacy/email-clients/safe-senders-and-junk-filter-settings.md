---
id: computing-software.general-digital-literacy.email-clients.safe-senders-and-junk-filter-settings
name: safe-senders-and-junk-filter-settings
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, safe-senders, junk-email-filter, not-spam, blocked-senders]
level: intro
status: docs-checked
description: "Stop real mail landing in junk: Outlook safe senders and contacts trust, Gmail Not spam, contacts and filters, and checking Spam and Junk regularly."
sources:
  - https://support.microsoft.com/en-us/outlook/mail/add-recipients-to-the-safe-senders-list-in-outlook
  - https://support.microsoft.com/en-us/outlook/filter-junk-email-and-spam-in-outlook
  - https://support.google.com/mail/answer/1366858
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Safe senders and junk filter settings

## Outlook
- Safe senders are never treated as junk, regardless of content. By default, addresses in your Outlook contacts count as safe senders; replying to someone who is not a contact does not add them automatically.
- New Outlook / Outlook on the web: Settings > **Mail** > **Junk email** > Senders > **Safe senders and domains** tab > **+ Add safe sender**, enter the address, OK, Save.
- To stop contacts being trusted automatically: Settings > Mail > Junk email > Security options > clear **Trust email from my contacts**.
- Outlook.com keeps junk email for 30 days before automatic deletion, and it is not recoverable.

## Gmail
- Remove a message from Spam: More > Spam > tick the email > **Not spam**; future mail from that sender will not go to Spam.
- Add the sender to Google Contacts, or create a filter to label their mail as important or another option.
- Blocking a sender means Gmail still flags their mail as spam even if you remove it from Spam.
- Spam warnings (spoofed address, phishing, unconfirmed sender) explain why a message was filtered; do not click links until you verify.

## Habits
- Check Junk and Spam regularly, especially after signing up for something.
- Do not use Report spam to leave newsletters you signed up for; use Unsubscribe.
- Work accounts: if mail never arrives, ask your admin; they may mark some mail as spam.

## Verify
- [ ] A test message from the sender lands in Inbox.

## Checked
2026-10-27. Microsoft Support "Add recipients to the Safe Senders List in Outlook" and "Filter junk email and spam in Outlook"; Google Gmail Help "Report spam in Gmail". Confirmed paths, contacts default, 30-day retention and Gmail behaviours. Removed unconfirmed classic Junk E-mail Options levels, Apple Mail, Gmail spam retention, quarantine and malware-bypass claims.
Method: documentation only; no commands were run.
