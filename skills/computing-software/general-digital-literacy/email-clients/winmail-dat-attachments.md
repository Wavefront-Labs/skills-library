---
id: computing-software.general-digital-literacy.email-clients.winmail-dat-attachments
name: winmail-dat-attachments
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, attachments, winmail-dat, tnef, rich-text-format]
level: practitioner
status: docs-checked
description: "Understand why Outlook Rich Text messages arrive with winmail.dat, and how the sender stops it by changing the message format."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/outlook/message-body/how-tnef-affects-email-messages
  - https://support.microsoft.com/en-us/outlook/change-the-message-format-to-html-rich-text-format-or-plain-text-in-outlook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# winmail.dat attachments

**Symptom:** you receive an email with a `winmail.dat` attachment instead of the expected file.

## Cause
Outlook's **Rich Text** message format uses Transport Neutral Encapsulation Format (TNEF) to package message information. Recipient systems that are not based on Microsoft Exchange might not be able to interpret it; if the recipient's system cannot process TNEF, a file named Winmail.dat is added to the message. A TNEF message contains a plain text version plus a binary attachment (usually Winmail.dat) holding the formatted text and other parts.

## Sender fix
Send in HTML or plain text instead of Rich Text; Microsoft's "Change the message format to HTML, Rich Text Format, or plain text in Outlook" page gives the steps for your Outlook version. The format you choose affects how the message looks to the recipient, whose mail program may convert it.

## Privacy note
The path of your personal folders (.pst) file and your sign-in name are embedded in the Winmail.dat file; password information is not revealed.

## Recipient
Ask the sender to resend in HTML or plain text, or to share the file by link. Open attachments only from senders you expected.

## Verify
- [ ] A test message from the sender arrives with the real attachment name.

## Checked
2026-10-27. Microsoft Learn "How TNEF affects email messages" and Microsoft Support "Change the message format". Confirmed the Rich Text and TNEF cause, the Winmail.dat contents and the privacy note. Removed unconfirmed menu paths, contact-level setting, autocomplete cache and third-party viewer names.
Method: documentation only; no commands were run.
