---
id: computing-software.general-digital-literacy.email-clients.confidential-mode-and-encrypted-email
name: confidential-mode-and-encrypted-email
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, email-encryption, confidential-mode, microsoft-purview-encryption, s-mime, send-sensitive-information]
level: intro
status: docs-checked
description: "Send sensitive information by email using Gmail confidential mode or Outlook Encrypt and S/MIME, and know what each does and does not protect."
sources:
  - https://support.google.com/mail/answer/7674059
  - https://support.google.com/mail/answer/6584
  - https://support.microsoft.com/en-us/outlook/mail/send-s-mime-or-microsoft-purview-encrypted-emails-in-outlook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Confidential mode and encrypted email

**Goal:** sensitive details (bank, ID, health) reach only the intended person.

## Gmail confidential mode (computer)
- Compose > **Toggle confidential mode** at the bottom of the window; if already on, click **Edit** at the bottom of the message.
- Set an expiration date from the drop-down. Choose **No SMS passcode** (Gmail recipients open it directly; non-Gmail recipients get the passcode by email) or **SMS passcode** (passcode sent by text; enter the recipient's number, not yours). Save.
- Expiry and passcode apply to the message text and attachments. You can remove access at any time: Sent > open the message > **Remove access**.
- Recipients cannot copy, paste, download, print or forward the text or attachments, but Google states they can still take screenshots or photos, and recipients with malicious programs may still copy or download your messages.
- On a work or school account, ask your admin whether confidential mode is enabled.

## Outlook
- In a message choose **Options** > **Encrypt**, then pick the restriction you want, such as **Encrypt** or **Do Not Forward**, finish the message and Send.
- Microsoft Purview message encryption needs the right license (Microsoft's page names Office 365 Enterprise E3); if you do not have it, encrypt with **S/MIME**. Set up Outlook for encryption and digital signatures first; in classic Outlook, S/MIME encrypts a single message or all outgoing messages, and recipients need your digital ID to decode them.

## Simple alternatives
- Use the organisation's secure upload portal when one is offered.
- Never email passwords or full card numbers; share a password by a separate channel.

## Verify
- [ ] Recipient confirmed they could open it; any password sent by a different channel.

## Checked
2026-10-27. Google Gmail Help "Send and open confidential emails" and "Send attachments"; Microsoft Support "Send S/MIME or Microsoft Purview encrypted emails in Outlook". Confirmed the Gmail controls, limits and screenshot warning, and the Outlook Encrypt and S/MIME steps. Removed unconfirmed claims: expiry range, in-transit TLS, Apple Mail S/MIME, Microsoft 365 Family coverage, zip encryption and national portals.
Method: documentation only; no commands were run.
