---
id: computing-software.general-digital-literacy.file-management.file-properties-and-get-info
name: file-properties-and-get-info
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, file-properties, get-info, file-size, read-only]
level: intro
status: docs-checked
description: "Read a file's details in Windows Properties (Alt+Enter, Unblock) and Mac Get Info (Command+I), and show the Finder path and status bars."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.microsoft.com/en-us/windows/security/information-about-the-attachment-manager-in-microsoft-windows
  - https://support.apple.com/guide/mac-help/get-file-folder-and-disk-information-on-mac-mchlp1774/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File properties and Get Info

## Windows
- Select the item and press `Alt+Enter` (or right-click > Properties) to open its Properties dialog.
- **Unblock:** for a file downloaded from the internet, Microsoft's Attachment Manager guidance is to open Properties, look for the security message near the bottom of the General tab and select **Unblock**, only for files from a source you trust. If there is no Unblock option, an organisation policy may be blocking it; ask your IT administrator.

## macOS
- Select an item and choose File > **Get Info** or press `Command+I`. For several items, hold Control and choose File > **Get Summary Info**.
- View > **Show Status Bar** shows the item count and free disk space.
- View > **Show Path Bar** (or hold Option) shows the folders containing the item; Control-click a folder in the path bar to choose Copy "folder" as Pathname.
- View > Show View Options > **Show item info** adds size and similar details under icons (Icon view only).

## Verify
- [ ] You can state a file's location and size using Properties or Get Info.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (Alt+Enter) and "Information about the Attachment Manager in Microsoft Windows" (Unblock); Apple Mac User Guide "Get file, folder and disk information on Mac" (macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims about the other Windows tabs (Details, Security, Previous Versions), Size on disk, read-only and locked flags, and Open with Change All.
Method: documentation only; no commands were run.
