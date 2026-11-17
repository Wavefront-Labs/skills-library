---
id: computing-software.general-digital-literacy.file-management.preview-pane-and-quick-look
name: preview-pane-and-quick-look
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, preview-pane, quick-look, details-pane, file-preview]
level: intro
status: docs-checked
description: "Peek inside files without opening them using the File Explorer preview and details panes on Windows and Quick Look (Space bar) on Mac."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.microsoft.com/en-US/servicing/os/windows/docs/2025/10/file-explorer-automatically-disables-the-preview-feature-for-files-downloaded-from-the-internet
  - https://learn.microsoft.com/en-us/windows/powertoys/peek
  - https://support.apple.com/guide/mac-help/view-and-edit-files-with-quick-look-mh14119/mac
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preview pane and Quick Look

**Goal:** check which of ten similarly named files is the right one without opening each in its app.

## Windows
- **Preview pane:** `Alt+P` shows or hides it. **Details pane:** `Alt+Shift+P`.
- Since the Windows security updates of 14 October 2025, File Explorer disables preview for files marked as downloaded from the internet (Mark of the Web) and for files on an Internet Zone file share; the pane shows a "could harm your computer" message. Microsoft's fix for a trusted file is right-click > Properties > **Unblock**; for a file share, add its address to Local intranet or Trusted sites in Internet Options (this relaxes security for everything on that share).
- Microsoft PowerToys **Peek** previews the file selected in File Explorer from a keyboard shortcut. The activation shortcut can be changed in PowerToys settings; check it there.

## Mac
- Select a file and press **Space** for Quick Look; press Space again to close. With several items selected the last one shows first; arrow keys or the on-screen arrows move between them; `Command+Return` shows them in a grid.
- Quick Look window tools: Markup, rotate (hold Option to rotate the other way), trim audio or video, **Open with** the default app, Share, and Command-Plus / Command-Minus to zoom.
- Finder **Preview pane:** View > **Show Preview** or `Shift+Command+P`.

## Verify
- [ ] A photo previews without launching its app; a PDF you made yourself previews too.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (Alt+P, Alt+Shift+P) and "File Explorer automatically disables the preview feature for files downloaded from the internet" (updates from 14 October 2025); Microsoft Learn PowerToys Peek page; Apple Mac User Guide "View and edit files with Quick Look on Mac" and keyboard shortcuts (macOS 27 / Tahoe 26, 2026). Fixed a stale claim: downloaded files no longer preview by default on updated Windows. Removed unconfirmed Office and PDF preview handler claims, the macro safety claim and the Option+Space shortcut.
Method: documentation only; no commands were run.
