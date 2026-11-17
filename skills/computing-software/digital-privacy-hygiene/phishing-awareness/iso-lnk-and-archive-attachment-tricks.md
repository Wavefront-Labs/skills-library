---
id: computing-software.digital-privacy-hygiene.phishing-awareness.iso-lnk-and-archive-attachment-tricks
name: iso-lnk-and-archive-attachment-tricks
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, iso-lnk-attachments, malicious-attachments, macros]
level: practitioner
status: draft
description: "Recognise malicious attachment containers (ISO, IMG, VHD, LNK, password ZIPs, HTML smuggling, OneNote) and show file extensions so disguises fail."
sources:
  - "https://learn.microsoft.com/microsoft-365/security/office-365-security/anti-malware-protection-about"
  - "https://www.cisa.gov/news-events/cybersecurity-advisories"
  - "https://support.microsoft.com/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ISO, LNK and archive attachment tricks

**Goal:** spot attachments designed to sneak malware past filters and Office macro blocks.

## Formats attackers favour
| Format | Trick |
|---|---|
| `.iso`, `.img`, `.vhd(x)` | Disk images that mount with a double-click; historically dodged Mark-of-the-Web warnings |
| `.lnk` (shortcut) | Looks like a document icon; runs PowerShell/cmd hidden in its target |
| Password-protected `.zip`/`.7z` (password in email) | Filters can't scan inside |
| `.html`/`.htm` attachment | HTML smuggling: builds and downloads a payload, or shows a fake login page offline |
| `.one` (OneNote) | Embedded scripts behind "double-click to view" buttons |
| `.js`, `.vbs`, `.hta`, `.wsf`, `.scr`, `.bat`, `.cmd`, `.msi` | Scripts/executables |
| `invoice.pdf.exe` | Double extension hidden when extensions are off |

## Show extensions (Windows)
File Explorer > View > Show > **File name extensions**. Now `invoice.pdf.lnk` shows its true type.

## Rules
- Don't open disk images, shortcuts, scripts or HTML files from email. Ask the sender to share via a known cloud
  service if it's real.
- A password-protected archive from someone you don't know = assume malicious.
- "Enable content/Enable editing" in Office files from email: don't.

## If opened
See "opened a malicious attachment" response.

## Gotchas
- Mac users: `.dmg`, `.pkg` and `.app` in zips carry the same risk; Gatekeeper warnings are the cue.
- Mail providers block many types; attackers then link to the file on a cloud drive instead.
