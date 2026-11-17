---
id: computing-software.general-digital-literacy.email-clients.troubleshooting-email-delivery
name: troubleshooting-email-delivery
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-delivery, bounce-message, spam-folder, blocked-sender, sync-issues, mailbox-full, email-not-sending, email-not-receiving, undeliverable, nondelivery-report]
level: intro
status: docs-checked
description: "Diagnose email that never arrives or never sends: read a bounce message, check the spam folder and blocked senders, fix sync lag and a full mailbox."
sources:
  - https://knowledge.workspace.google.com/admin/support/troubleshooting/gmail-smtp-errors-and-codes
  - https://support.google.com/mail/answer/6584
  - https://support.google.com/mail/answer/78892
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting email delivery — find where the message actually got stuck

**Goal:** work out whether a missing email is a sending problem, a receiving problem, a
filtering problem or a sync delay, using what the client tells you rather than guessing
and resending blindly.

## 1. First split: did it send, or did it arrive?
- Check the **Sent** folder. If the message isn't there, it never left your client — a
  sending problem (section 2). If it is there, it left you and the question is on the
  receiving end (section 3).
- Ask the recipient to check **Spam/Junk** before assuming it never arrived.

## 2. It won't send
- A stuck "Sending..." status can mean a large attachment or a flaky connection. Gmail's
  personal-account attachment limit is 25 MB (above it Gmail inserts a Google Drive
  link). Remove the attachment and send it as a cloud link instead.
- Check you're online and the client isn't in an offline mode.
- A **bounce/non-delivery report** arriving back in your own inbox contains the real
  reason in its body — read past the first line. Google's SMTP error reference describes:
  `550` (permanent rejection, e.g. the recipient account does not exist, a policy block
  or suspected spam), `552` (permanent: message too large, or the recipient's inbox out
  of storage), `421` (temporary refusal, e.g. server busy or rate limiting; retry) and
  `450` (temporary: the recipient is receiving mail too quickly; resend later). Other
  providers' wording may differ.

## 3. It sent, but they never got it
- Check for a **typo in the address** first; a bounce report will confirm a nonexistent
  address.
- Ask the recipient whether you're blocked or caught in their junk filters. A message
  can also be rejected by an organisation's own gateway; if you suspect this, ask the
  recipient to check with their IT team.
- If they rarely hear from you, ask them to add you to their contacts.

## 4. Sync lag across devices
- A message appears on one device but not another: trigger a manual refresh in the
  client and confirm the device is online and not in airplane mode.
- With IMAP, deleting from a client folder does not remove the message from Gmail; it
  stays in the All Mail label. Gmail's IMAP page advises letting Gmail do the spam
  sorting instead of turning on a client's junk filter.

## 5. Mailbox full (yours or theirs)
- A full mailbox can cause rejections. Check your account's storage page and clear large
  attachments (in Gmail, search `has:attachment larger:10M`).
- A bounce saying the **recipient's** inbox is out of storage is their problem; reach
  them another way.

## Verify
- [ ] You checked Sent (did it leave?) before concluding anything is broken.
- [ ] A bounce message's body was read in full, not just its subject line.
- [ ] Spam/junk and blocked-sender lists were checked on the receiving end, where
      possible.

## Checked
2026-11-01. Confirmed from Google's Gmail SMTP errors and codes page (421, 450, 550,
552), the Gmail attachment page (25 MB, Drive link) and Gmail IMAP help (deleted
messages stay in All Mail; skip client junk filters). Removed: Outlook 20 MB and Work
Offline toggle, F9 and Apple Mail menu paths, POP-versus-IMAP behaviour claims,
storage-warning timing, and the "552 means mailbox full" simplification.
Method: documentation only; no commands were run.
