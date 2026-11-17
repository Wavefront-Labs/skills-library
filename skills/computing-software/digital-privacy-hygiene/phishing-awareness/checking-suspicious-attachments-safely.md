---
id: computing-software.digital-privacy-hygiene.phishing-awareness.checking-suspicious-attachments-safely
name: checking-suspicious-attachments-safely
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, attachment-scanning, malicious-attachments, virustotal, mark-of-the-web, macros, dangerzone, phishing]
level: practitioner
status: draft
description: "Handle suspicious email attachments: recognise dangerous file types, show extensions, check hashes or scan safely, use Protected View and sandboxes, and never enable macros."
sources:
  - "https://www.virustotal.com/"
  - "https://learn.microsoft.com/en-us/microsoft-365-apps/security/internet-macros-blocked"
  - "https://dangerzone.rocks/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checking suspicious attachments safely

**Goal:** most malware and many credential phish arrive as attachments. Decide without executing them.

## Dangerous types
- Executables and scripts: `.exe`, `.msi`, `.scr`, `.js`, `.vbs`, `.hta`, `.bat`, `.ps1`, `.lnk`.
- Containers that bypass warnings: `.iso`, `.img`, `.vhd`, password-protected `.zip`/`.rar`/`.7z` ("password is 1234").
- Office with macros: `.docm`, `.xlsm`, old `.doc`/`.xls` asking to "Enable Content"; OneNote `.one` with buttons.
- `.html`/`.htm`/`.svg` attachments: open a local fake login page.
- PDFs whose only content is a link or QR code to "view the document".

## Before opening
- Windows: File Explorer > View > Show > **File name extensions** on, so `invoice.pdf.exe` is visible.
- Were you expecting it? Confirm with the sender by phone or a new message, not by replying.
- Preview in the webmail viewer (Gmail/Outlook preview renders server-side) rather than downloading.

## Check
- Hash first (does not share the file):
  ```powershell
  Get-FileHash .\file.docx -Algorithm SHA256
  ```
  Search the hash on VirusTotal. Uploading the file shares it with security vendors and researchers: never upload
  confidential documents.
- Right-click > Scan with Microsoft Defender.
- Open untrusted documents through **Dangerzone** (converts to a safe pixel PDF) or in **Windows Sandbox**/a VM.

## Built-in protections to keep on
- Mark of the Web + Office **Protected View**; Office blocks macros in files from the internet by default. Never click
  "Enable Editing"/"Enable Content" for an unexpected file.
- SmartScreen/Smart App Control for executables.

## If you opened it
Disconnect from the network, run a full Defender scan, and follow the infected-computer cleanup; change passwords from
another device if you typed any into a page it opened.

## Verify
- [ ] Extensions visible; macros from the internet blocked; you know how to hash-check a file.
