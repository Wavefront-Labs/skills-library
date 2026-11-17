---
id: computing-software.general-digital-literacy.file-management.compression-and-archive-formats
name: compression-and-archive-formats
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, compression, zip, 7z, rar, tar-gz, password-protected-zip, archive-formats, split-archive, extract, compress-to-zip, large-file-sharing, encrypted-zip, 7-zip]
level: intro
status: docs-checked
description: "Zip and extract files on Windows/macOS, password-protect an archive properly, split large ones, and pick between zip, 7z, rar and tar.gz."
sources:
  - https://support.microsoft.com/en-us/windows/zip-and-unzip-files-8d28fa72-f2f9-712f-67df-f80cf89fd4e5
  - https://support.apple.com/guide/mac-help/zip-and-unzip-files-and-folders-on-mac-mchlp2528/mac
  - https://www.7-zip.org/7z.html
  - https://support.google.com/mail/answer/6584
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Compression and archive formats — bundle, shrink, and protect a group of files

**Goal:** turn many files into one, shrink them for upload or email, lock an archive
with a password that actually means something, and know when to reach for a format
beyond the built-in zip.

## 1. Compress and extract with what's already installed
- **Windows**: right-click the file or folder › **Show more options** › **Send to** ›
  **Compressed (zipped) folder**. Extract: open the zipped folder and drag items out, or
  right-click it › **Extract All...**.
- **macOS**: Control-click the file or folder in Finder › **Compress**.
- No extra software is needed for plain zip, which covers most everyday use (email
  attachments, sending a folder of photos).

## 2. Password-protecting an archive
- Windows' built-in zip support does not handle encrypted archives; Microsoft's page
  points to tools such as 7-Zip or WinRAR for those. Do not zip files that are already
  encrypted: they are stored unencrypted once extracted from the zipped folder.
- **7-Zip** supports encryption with the AES-256 algorithm in its 7z format. Pick that
  format and set a password at creation.
- Send the password through a **different channel** than the archive itself (a text
  message if the archive went by email) — sending both together defeats the point.
- Treat a lost password as unrecoverable: write it down somewhere safe if it matters.

## 3. Large files
- Gmail removes attachments over its 25 MB personal-account limit and inserts a Google
  Drive link instead; Workspace admins set the limit for work and school accounts.
- A cloud-storage link (see organising-files-and-folders, section 6) is usually simpler
  than splitting an archive into parts. If you do split, keep every part together:
  a single missing part makes the archive unextractable.

## 4. Choosing a format
| Format | When |
|---|---|
| `.zip` | Default. Windows and macOS both create and open it without extra software. |
| `.7z` | 7-Zip's own format, with AES-256 encryption available. Needs 7-Zip or a compatible tool to open. |
| `.rar`, `.tar.gz` | Usually only met when you receive one: open it with a tool that supports it rather than choosing it yourself for everyday sharing. |

## 5. Gotchas
- Compressing an already-compressed format (JPG photos, MP4 video, most PDFs) barely
  shrinks the file further — zip is for bundling many files into one, not for making
  photos/videos smaller.

## Verify
- [ ] You can zip and extract without installing anything extra.
- [ ] A password-protected archive you created uses real AES encryption (7-Zip `.7z`).
- [ ] The archive password was sent through a different channel than the file.
- [ ] You picked `.zip` by default and only reached for another format for a specific
      reason (encryption or because that's what was received).

## Checked
2026-11-01. Confirmed from the Microsoft zip/unzip page (Windows menu path, no encrypted
archive support, 7-Zip/WinRAR suggestion, encrypted-file warning), Apple Mac help
(Control-click › Compress), the 7-Zip 7z page (AES-256) and the Gmail attachment page
(25 MB, Drive link). Removed: Windows 11 wording, Keka, split-size examples, Outlook
limit, RAR licensing, tar command and `__MACOSX` notes, which no page read here states.
Method: documentation only; no commands were run.
