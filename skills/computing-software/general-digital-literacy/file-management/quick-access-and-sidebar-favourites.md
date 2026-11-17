---
id: computing-software.general-digital-literacy.file-management.quick-access-and-sidebar-favourites
name: quick-access-and-sidebar-favourites
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, quick-access, finder-sidebar, favourites, pin-to-quick-access]
level: intro
status: docs-checked
description: "Pin the folders you use most to Windows File Explorer Home and Quick access or the Mac Finder sidebar, and tidy what appears there."
sources:
  - https://support.microsoft.com/en-us/windows/experience/fileexplorer/file-explorer-in-windows
  - https://support.apple.com/guide/mac-help/customize-the-finder-sidebar-on-mac-mchl83c9e8b8/mac
  - https://support.apple.com/guide/mac-help/create-and-remove-aliases-on-mac-mchlp1046/mac
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Quick access favourites and sidebar

**Goal:** your project folders are one click away in File Explorer and the Finder sidebar.

## Windows File Explorer
- Right-click a folder > **Pin to Quick access**; right-click > **Unpin from Quick access** to remove it. Pinned folders show in File Explorer Home and in the left navigation pane.
- In Windows 11 version 22H2 and later the landing page is called **Home** (earlier: Quick access). To open File Explorer at This PC instead: See more (three dots) > **Options** > *Open File Explorer to* > This PC > Apply.
- Recent files and frequent folders are listed on Home. In Options, the **Privacy** section has check boxes to turn them off; with them cleared, Quick access shows only pinned folders. A single unwanted item can be removed with right-click > **Remove from Quick access**.
- Windows 11 no longer lists Desktop, Documents and the other default folders under This PC; they are pinned in Quick access by default.

## Mac Finder
- Drag a folder to the **Favourites** section of the sidebar, or select it and press `Control+Command+T`. Only the alias is added; the original is untouched.
- To remove an item, drag it out of the sidebar until the remove symbol appears; the original folder stays.
- Finder > Settings > **Sidebar**: choose which standard items appear (they also show in Open and Save dialogs).
- Finder > Settings > General > **New Finder windows show**: choose the folder new windows open to.

## Verify
- [ ] File > Open in any app shows your chosen folders in the sidebar.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "File Explorer in Windows" (Windows 11 22H2 Home, pin and unpin, Options, privacy check boxes); Apple Mac User Guide "Customise the Finder sidebar", "Create and remove aliases", "Change Finder settings" and keyboard shortcuts (macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims (Add to Favourites on files, disconnected-drive errors, cloud placeholders).
Method: documentation only; no commands were run.
