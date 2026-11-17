---
id: computing-software.general-digital-literacy.office-suites.mail-merge-to-email
name: mail-merge-to-email
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, mail-merge, email-merge, personalised-email, outlook-merge]
level: practitioner
status: docs-checked
description: "Send personalised individual emails from a Word mail merge through Outlook, with subject line, HTML format and the limits that trip people up."
sources:
  - https://support.microsoft.com/en-us/word/use-mail-merge-in-word-to-send-bulk-email-messages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mail merge to email

**Goal:** each person gets their own email ("Dear Sam, your booking is 14 May") instead of one
message with 200 people in To/Cc.

## Before you start
- A MAPI-compatible email program (such as Outlook) must be installed and set as the default email
  program; otherwise the email merge option is unavailable.
- To use Outlook contacts as the list, Outlook must be the default email program and the same version
  as Word.

## Steps (Word for Windows)
1. Excel list with an **Email** column (an address for every recipient) and the personalised fields;
   format ZIP/postal codes as text.
2. Word › **Mailings › Start Mail Merge › E-mail Messages**.
3. **Select Recipients** › choose the list; edit, sort or filter recipients as needed.
4. Write the message; **Greeting Line** or **Insert Merge Field** for names, dates, amounts.
5. **Preview Results** and step through a few records.
6. **Finish & Merge › Send E-mail Messages** › To: the *Email* column; Subject line; Mail format:
   **HTML** (default) or Plain text › Send records: All, Current record, or From/To › OK.

## Limits and gotchas
- Word sends one individual message per address: **no Cc/Bcc** and **no attachments** (include
  links instead).
- Bulk sending is subject to your mail provider's sending limits and spam filtering; send in batches,
  and use a mailing service with unsubscribe handling for newsletters.
- Test by filtering the list to your own address first (Send records: From/To or Current record).
- Saving the main document keeps its connection to the list for reuse.

## Verify
- [ ] Your test email shows your name and correct field values; Sent Items holds one message per
  recipient.

## Checked
2026-10-27 against Microsoft Support "Use mail merge in Word to send bulk email messages" (Word for
Microsoft 365, 2024, 2021, Windows and macOS tabs). Confirmed: MAPI program requirement, default email
program requirement, E-mail Messages steps, To/Subject/Mail format/Send records options, no Cc/Bcc or
attachments. Removed unconfirmed claims about new Outlook and Outlook on the web, specific
Microsoft 365 recipient limits and Gmail merge features. Method: documentation only; no commands were run.
