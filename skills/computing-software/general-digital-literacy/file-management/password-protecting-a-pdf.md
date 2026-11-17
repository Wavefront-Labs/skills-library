---
id: computing-software.general-digital-literacy.file-management.password-protecting-a-pdf
name: password-protecting-a-pdf
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-scanning, protect-pdf, pdf-password, pdf-encryption]
level: intro
status: draft
description: "Encrypt a PDF with an open password in Acrobat, Mac Preview, Word export or LibreOffice, share the password safely, and know what permissions passwords do not stop."
sources:
  - https://helpx.adobe.com/acrobat/using/securing-pdfs-passwords.html
  - https://support.apple.com/guide/preview/password-protect-a-pdf-prvw587/mac
  - https://support.microsoft.com/en-us/office/save-or-convert-to-pdf-or-xps-in-office-desktop-apps-d85416c5-7d77-4fd6-a216-6f4bf7c7c110
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Password-protect a PDF

## Ways to add an open password
- **Word / Excel / PowerPoint (Windows):** File › Save As › PDF › **Options** › tick *Encrypt the document with a password* (AES-256).
- **Mac Preview:** File › Export › tick **Encrypt** › password. (Or File › Print › PDF › Save as PDF › Security Options.)
- **Adobe Acrobat:** Tools › **Protect** › *Protect Using Password* › Viewing.
- **LibreOffice:** File › Export as PDF › Security › *Set passwords*.

## Two kinds of password
- **Open (user) password:** encrypts the file; needed to view. This is the protection.
- **Permissions (owner) password:** restricts printing/copying/editing. Many apps ignore it and it is trivially removed; do not rely on it for secrecy.

## Sharing the password
- Send it by a different channel (text message or phone call), never in the same email.
- Use a long passphrase (4+ random words). Short passwords on PDFs are cracked offline quickly.

## Gotchas
- Forgotten open password = file is lost; keep the original unencrypted copy somewhere safe.
- Some online forms and e-signature tools reject encrypted PDFs; send unencrypted via a secure portal instead.
- Encrypting a PDF does not hide its file name or email subject.

## Verify
- [ ] Opening the file asks for the password; the wrong password fails; the right one opens it.
