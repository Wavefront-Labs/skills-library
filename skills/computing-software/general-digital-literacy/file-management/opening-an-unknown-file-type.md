---
id: computing-software.general-digital-literacy.file-management.opening-an-unknown-file-type
name: opening-an-unknown-file-type
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-formats, unknown-file-type, file-extension, open-with, file-signature]
level: intro
status: draft
description: "Work out what an unfamiliar file is from its extension and source, pick a safe app to open it, and avoid running disguised executables."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open an unknown file type safely

**Goal:** open a file with an unfamiliar icon or extension without infecting the computer.

## Identify it
1. Show extensions (Windows File Explorer › View › Show › **File name extensions**; Mac Finder Settings › Advanced › *Show all filename extensions*).
2. Note the extension and look it up at the operating system vendor's or a reputable file-extension reference.
3. Ask: where did it come from? Expected from someone you know?

## Common surprises
| Extension | What it is | Open with |
|---|---|---|
| `.heic`, `.webp` | images | Photos / Preview / browser |
| `.eml`, `.msg` | saved emails | mail app, Outlook |
| `.ics` | calendar invite | calendar app |
| `.vcf` | contact card | Contacts |
| `.odt`, `.ods` | OpenDocument | LibreOffice, Word, Google Docs |
| `.pages`, `.numbers` | Apple iWork | Pages/Numbers, iCloud.com |
| `.7z`, `.rar` | archives | 7-Zip, Windows 11, The Unarchiver |
| `.dat` (winmail.dat) | Outlook rich-text attachment wrapper | ask sender to resend as PDF |

## Never double-click when in doubt
- Executable or script types: `.exe`, `.msi`, `.scr`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.js`, `.jar`, `.app`, `.dmg`, `.pkg`, `.lnk`, `.iso`, `.img`.
- Double extensions like `invoice.pdf.exe` are a classic disguise.
- Upload suspicious files to VirusTotal only if they contain nothing private.

## Open safely
- Right-click › **Open with** › choose a viewer (Notepad/TextEdit shows the raw content harmlessly for text-based files).
- Use a browser or Google Drive preview for documents from unknown sources.
- Don't install a random "file opener" program from search ads.

## Verify
- [ ] File type confirmed and opened in a known app; nothing executable launched.
