---
id: computing-software.general-digital-literacy.email-clients.multiple-accounts-and-auto-reply
name: multiple-accounts-and-auto-reply
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, multiple-accounts, email-aliases, send-as, email-signature, auto-reply, vacation-responder, out-of-office, outlook-rules, gmail-aliases, unified-inbox]
level: intro
status: docs-checked
description: "Send from the right address with Gmail Send mail as, and set Gmail vacation responder and Outlook automatic replies with end dates and the right audience."
sources:
  - https://support.google.com/mail/answer/22370
  - https://support.google.com/mail/answer/25922
  - https://support.microsoft.com/en-us/outlook/send-automatic-out-of-office-replies-from-outlook-com-or-outlook-on-the-web
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple accounts and auto-reply

**Goal:** avoid replying from the wrong address, and set an out-of-office that behaves as expected.

## Sending as the right address (Gmail)
- Settings > See all settings > **Accounts and import** > **Send mail as** > Add another email address (verify by the confirmation link). Up to 99 addresses.
- In a message, click the **From** line and choose the address before sending. To make one the default use Make default; replies go to your Gmail address unless you also set a different reply-to address.
- Starting January 2027 Gmail no longer supports Send as for third-party addresses (for example @yahoo.com, @outlook.com); Google Workspace aliases and other Gmail addresses you own are not affected.

## Auto-reply
- **Gmail vacation responder:** Settings > See all settings > General > **Vacation responder** > turn on, set the date range, subject and message. Tick the checkbox under the message to reply only to your contacts. Save Changes. It starts at 12:00 AM on the start date and ends at 11:59 PM on the end date; a banner shows and **End now** turns it off. Your signature shows below the reply.
- Gmail usually replies to a person once, but again if they write after four days while it is on, or after you edit the reply. It does not reply to mail in Spam or sent to a mailing list you subscribe to.
- **Outlook.com / Outlook on the web:** Settings > Accounts > **Automatic replies** > turn on, tick **Send replies only during a time period** and enter start and end times; tick **Send replies outside your organization** if senders outside should get it. The reply is sent only once to each person. Without a time period it stays on until you turn it off.
- Use an end date so a stale "on leave" message does not linger.

## Verify
- [ ] The From field is checked before sending when several addresses exist.
- [ ] Any auto-reply has an end date and the intended audience.

## Checked
2026-10-27. Google Gmail Help "Send emails from a different address or alias" and "Send an automatic reply when you're out of office"; Microsoft Support "Send automatic out-of-office replies from Outlook.com or Outlook on the web". Confirmed the paths and behaviours above. Removed unconfirmed unified-inbox, per-account signature, bounce-loop and Outlook From-field claims.
Method: documentation only; no commands were run.
