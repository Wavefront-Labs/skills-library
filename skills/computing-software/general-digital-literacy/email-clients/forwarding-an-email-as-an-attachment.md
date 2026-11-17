---
id: computing-software.general-digital-literacy.email-clients.forwarding-an-email-as-an-attachment
name: forwarding-an-email-as-an-attachment
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-attachments, forward-as-attachment, eml-file, report-phishing]
level: intro
status: docs-checked
description: "Forward an email as an attachment in Gmail and classic Outlook so the original message is kept for IT or abuse reports, and download Gmail messages as .eml."
sources:
  - https://support.google.com/mail/answer/9261412
  - https://support.google.com/mail/answer/29436
  - https://support.microsoft.com/en-us/outlook/reply-to-or-forward-an-email-message
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Forward an email as an attachment

Plain forwarding rewrites the message and loses the headers (routing, sender authentication). Security teams and abuse desks may ask for the original as an attachment.

## Gmail (computer)
- Tick the checkbox next to each email, then **More** > **Forward as attachment**. Add recipients, subject and a message, then Send. You can also right-click an email, or drag it into the body of a message.
- Each email becomes an `.eml` file; you can attach as many as you like, and if the total is over 25 MB it attaches through Google Drive.
- Alternative: open the email > More > **Download message**; you need a desktop mail client to open the downloaded EML file. Or More > **Show original** to copy the full header.

## Classic Outlook
- Select the message in the list, then on the main ribbon choose **More Respond Actions** > **Forward as Attachment**.

## Gotchas
- If your organisation provides a Report phishing button, use that rather than forwarding suspicious mail to colleagues.
- Do not click links in a suspect message while handling it.

## Verify
- [ ] The sent email contains an attachment that opens with full headers visible.

## Checked
2026-10-27. Google Gmail Help "Download and send emails as attachments" and "Trace an email with its full header"; Microsoft Support "Reply to or forward an email message in classic Outlook". Confirmed steps, .eml output, 25 MB Drive behaviour and the classic Outlook command. Removed unconfirmed new Outlook, keyboard shortcut, .msg viewer, Apple Mail and phone claims.
Method: documentation only; no commands were run.
