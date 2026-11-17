---
id: computing-software.general-digital-literacy.email-clients.spotting-dangerous-attachments
name: spotting-dangerous-attachments
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, attachments, suspicious-attachments, malicious-attachment, macros, enable-content, file-extensions, html-attachment, iso-attachment, phishing]
level: intro
status: draft
description: "Recognise dangerous email attachments (executables, macro documents, HTML, ISO, password-protected zips) and handle unexpected files safely."
sources:
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - https://www.cisa.gov/secure-our-world
  - https://support.google.com/mail
  - https://support.microsoft.com/en-us/outlook
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spotting dangerous attachments

**Goal:** never be the person who opened the malware.

## High-risk file types
| Type | Why |
|---|---|
| `.exe .scr .msi .bat .cmd .js .vbs .ps1 .lnk` | Programs or scripts: run code when opened |
| `.docm .xlsm`, or any Office file asking to **Enable Content / Enable Macros** | Macros install malware |
| `.html .htm .shtml` | Opens a fake login page in your browser |
| `.iso .img .vhd` | Disk images used to sneak programs past filters |
| Password-protected `.zip .7z .rar` with the password in the email | Hides contents from scanners |
| `invoice.pdf.exe` | Double extension; Windows hides the real one by default |

Turn on file extensions (File Explorer › View › Show › File name extensions) so you see them.

## Warning signs
- You weren't expecting it, even if the sender is someone you know (accounts get hacked).
- Urgency: "overdue invoice", "your parcel", "payslip", "voicemail".
- Generic greeting, mismatched sender address, odd timing.

## What to do
1. Don't open it. Check with the sender **through another channel** (phone, a new message), not by
   replying.
2. Preview safely: Gmail/Outlook web previews open in the browser without running macros.
3. Never click *Enable Editing* / *Enable Content* on a document from email unless you are sure.
4. Report it (Report phishing button) and delete.
5. Opened something suspicious? Disconnect from the network, run a full antivirus scan, tell IT.

## Verify
- [ ] File extensions are visible on your computer; you know your Report phishing button.
