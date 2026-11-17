---
id: computing-software.general-digital-literacy.email-clients.attachment-will-not-open
name: attachment-will-not-open
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, attachments, attachment-wont-open, protected-view, file-association, blocked-attachment]
level: intro
status: draft
description: "Diagnose email attachments that will not open: no app for the file type, Protected View, blocked types, corrupt downloads, encrypted files and phones."
sources:
  - https://support.microsoft.com/en-us/outlook
  - https://support.google.com/mail
  - https://support.apple.com/guide/iphone/welcome/ios
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Attachment will not open

Work through by symptom.

| Symptom | Fix |
|---|---|
| "How do you want to open this file?" / unknown icon | No app for that type: check the extension (show file extensions). Install a viewer (e.g. free Adobe Acrobat Reader for PDF, LibreOffice for docx/odt) or open in the web version of Gmail/Outlook preview |
| Opens read-only with a yellow **Protected View** bar | Normal for internet files. Click *Enable Editing* only if you trust the sender |
| Outlook: "blocked access to the following potentially unsafe attachments" | .exe/.js/.bat etc. are blocked on purpose. Ask the sender to share via OneDrive/zip only if it is legitimately needed |
| Gmail: "This attachment is blocked" / virus warning | Google detected malware or an executable; do not try to bypass |
| "File is corrupt" / 0 KB | Re-download; ask sender to resend; check mailbox didn't strip it |
| Password prompt | Encrypted file: password should come by another channel |
| `winmail.dat` | Sender used Rich Text format (see winmail-dat skill) |
| .zip that won't extract on phone | Use the Files app (iPhone: tap the zip to expand) |
| .heic photo on Windows | Install HEIF Image Extensions or ask for JPG |
| Office file on phone opens blank | Install the free Word/Excel app or open in the Gmail/Outlook preview |

## Safety
An unexpected attachment, even from a known contact, that urges you to *Enable Content* (macros) is
the classic malware route. Confirm by phone first.

## Verify
- [ ] File opens in an appropriate app with the expected content.
