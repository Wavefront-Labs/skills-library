---
id: computing-software.general-digital-literacy.email-clients.rich-text-vs-plain-text-email
name: rich-text-vs-plain-text-email
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-composing, plain-text-email, html-email, message-format]
level: intro
status: draft
description: "Choose between HTML, rich text and plain text email in Outlook, Gmail and Apple Mail, switch formats per message or by default, and know what each breaks."
sources:
  - https://support.microsoft.com/en-us/outlook
  - https://support.google.com/mail
  - https://support.apple.com/guide/mail/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Rich text vs plain text email

## The three formats
- **HTML**: fonts, colours, inline images, tables, signatures with logos. Default nearly everywhere.
- **Plain text**: characters only. Smallest, most compatible, readable by screen readers and mailing lists; links show as raw URLs.
- **Rich Text (RTF)**: Outlook-only. Recipients on other systems get a `winmail.dat` attachment. Avoid for external mail.

## Switch
- **Outlook (classic)**: in a new message **Format Text > HTML / Plain Text / Rich Text**. Default: File > Options > Mail > *Compose messages in this format*. New Outlook/web: *Options > Switch to plain text*.
- **Gmail**: in compose, three-dot menu > **Plain text mode** (strips formatting from that message).
- **Apple Mail**: **Format > Make Plain Text** (Shift+Cmd+T); default under Settings > Composing > *Message format*.
- Reading all mail as plain text (Outlook Trust Center > Email Security > *Read all standard mail in plain text*) is a strong anti-phishing setting: hidden link targets become visible.

## When to use plain text
- Mailing lists, technical mailing lists, and some ticket systems that mangle HTML.
- Sending code or configuration (no smart quotes or auto-formatting).
- When a recipient reports garbled formatting.

## Gotchas
- Switching to plain text drops formatting and inline images from that draft permanently.
- Replying keeps the original message's format; switch explicitly if needed.
- Big HTML signatures with images can push mail into spam or show as attachments.

## Verify
- [ ] Send a test to another account and view on desktop and phone.
