---
id: computing-software.general-digital-literacy.office-suites.password-protect-and-restrict-editing
name: password-protect-and-restrict-editing
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, document-setup, password-protect-document, restrict-editing, encrypt-document, mark-as-final]
level: practitioner
status: docs-checked
description: "Encrypt a Word document with an open password, restrict editing, or mark it final, and know which protections are real."
sources:
  - https://support.microsoft.com/en-us/word/protect-a-word-document-with-a-password
  - https://support.microsoft.com/en-us/word/make-a-document-read-only-in-word
  - https://support.microsoft.com/en-us/office/collab-files/help-prevent-changes-to-a-final-version-of-a-file
  - https://support.google.com/drive/answer/7166529
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Password-protect and restrict editing

Different jobs; people mix them up.

| Need | Feature | Strength |
|---|---|---|
| Nobody without the password can open it | **Encrypt with Password** | Encryption |
| People can open but edits are limited | **Restrict Editing** | Honest-user control; a password is optional |
| Signal that it is finished | **Mark as Final** | Not a security feature; anyone can remove it |

## Encrypt (open password)
- **Windows:** File > Info > Protect Document > **Encrypt with Password**, enter and confirm, save.
- **Mac:** Review > Protect > **Protect Document**; under Security require a password to open, to modify, or both.
- If you forget it, Word cannot recover it; IT may help only if a recovery tool (DocRecrypt) was deployed before the password was set. Keep it in a password manager and send it by a different channel from the file.
- Word for the web cannot apply password encryption or edit an encrypted document; use Open in Word.

## Restrict editing
**Review > Restrict Editing**: tick **Allow only this type of editing in the document** and choose **No changes (Read only)** (or another type listed), optionally tick **Everyone** under Exceptions for a selected part, then **Yes, Start Enforcing Protection**. Without a password anyone can click Stop Protection.

## Mark as Final
File > Info > Protect > **Mark as Final** makes the file read-only and sets its Status to Final, but it is not security: anyone can remove it.

## Google Docs equivalent
Share with the **Viewer** or **Commenter** role. In Share > Settings you can untick the options that let people download, copy and print. The sharing role is the real control.

## Verify
- [ ] Close and reopen: an encrypted file prompts for a password; a restricted one opens with the Restrict Editing pane.

## Checked

2026-10-27. Microsoft Support 'Protect a Word document with a password', 'Make a document read only in Word' and Mark as Final pages, plus Google Drive sharing help (read 2026-10-27). Confirmed Windows and Mac encryption paths, no-recovery and DocRecrypt note, Word for the web limits, Restrict Editing steps, Mark as Final. Removed: AES claim, Mac Restrict Editing path, co-authoring and Outlook/Teams preview claims, old .doc and PDF password notes (not confirmed).

Method: documentation only; no commands were run.
