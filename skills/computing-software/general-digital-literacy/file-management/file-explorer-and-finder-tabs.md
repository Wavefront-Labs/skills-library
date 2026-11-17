---
id: computing-software.general-digital-literacy.file-management.file-explorer-and-finder-tabs
name: file-explorer-and-finder-tabs
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, file-explorer-tabs, finder-tabs]
level: intro
status: docs-checked
description: "Open, move and merge tabs in Windows 11 File Explorer and macOS Finder to work in several folders in one window, with the shortcuts and settings that control them."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.apple.com/guide/mac-help/use-tabs-in-windows-mchla4695cce/mac
  - https://support.apple.com/guide/mac-help/change-finder-settings-on-mac-mchlp2803/mac
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File Explorer and Finder tabs

## Windows 11 File Explorer
- `Ctrl+T` opens a new tab and switches to it, `Ctrl+W` closes the active tab (or the window if only one tab is open), `Ctrl+Tab` / `Ctrl+Shift+Tab` move to the next / previous tab, `Ctrl+1` to `Ctrl+9` jump to a tab by number.
- `Ctrl+N` opens a new window.
- No tab bar? Tabs need Windows 11 22H2 or later. Windows 10 reached end of support on 14 October 2025, so moving to Windows 11 is the supported route.

## macOS Finder
- Tabs come from the general Mac window feature: Window > **Merge All Windows** gathers the open Finder windows into one tabbed window; View > **Show Tab Bar** shows the bar; `Control+Tab` / `Control+Shift+Tab` go to the next / previous tab; `Shift+Command+T` shows or hides the tab bar in Finder windows.
- System Settings > Desktop & Dock > Windows > **Prefer tabs when opening documents** (In Full Screen, Always or Never) controls whether documents open in tabs. With it set to Always or In Full Screen, `Command+N` adds a tab in apps that support it; with Never, `Option+Command+N` does.
- Finder > Settings > General > **Open folders in tabs instead of new windows**: when ticked, Command-double-click on a folder opens it in a tab.

## Verify
- [ ] Two folders are open as tabs in one window and the shortcuts above switch between them.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (File Explorer table) and "File Explorer in Windows" (Windows 10 end of support note); Apple Mac User Guide "Use tabs in windows on Mac", "Change Finder settings on Mac" and "Mac keyboard shortcuts" (macOS 27 / Tahoe 26 pages, 2026). Confirmed the tab shortcuts, Merge All Windows, Show Tab Bar, the Prefer tabs setting, the Finder tabs option and Shift+Command+T. Removed unconfirmed claims (right-click Open in new tab, dragging tabs, same-drive move rules, snapping windows).
Method: documentation only; no commands were run.
