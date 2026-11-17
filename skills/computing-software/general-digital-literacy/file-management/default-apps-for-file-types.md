---
id: computing-software.general-digital-literacy.file-management.default-apps-for-file-types
name: default-apps-for-file-types
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-formats, default-apps, open-with, file-associations, always-use-this-app, pdf-default-app]
level: intro
status: docs-checked
description: "Change which app opens a file type on Windows (Settings > Apps > Default apps) and macOS (Get Info > Open with), and fix files that open in the wrong program."
sources:
  - https://support.microsoft.com/en-us/windows/change-default-programs-in-windows-e5d82cad-17d1-c53b-3505-f10a32e1894d
  - https://support.apple.com/guide/mac-help/choose-an-app-to-open-a-file-on-mac-mh35597/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Changing the default app for a file type

**Goal:** double-clicking a PDF opens your PDF reader, photos open your viewer, and so on.

## Windows
- Settings > Apps > **Default apps**. Use *Set a default for a file type or link type* to choose the app for an extension; selecting an app also lists the file and link types it can open, and you can change each one.

## macOS
- Select a file in Finder, choose File > **Get Info** (or Control-click > Get Info), expand **Open with**, pick the app, then apply it to all files of that type. Skip that last step if only the one file should change.
- One-off: File > **Open With**, or drag the file onto an app icon in the Finder or Dock.

## Gotchas
- If the file has the wrong extension, changing the default app will not fix it.

## Verify
- [ ] Double-click a file of that type; it opens in the chosen app.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Change default programs in Windows" (Settings > Apps > Default apps, file type setting); Apple Mac User Guide "Choose an app to open a file on Mac" (as returned by Apple search, 2026). Removed unconfirmed claims: right-click Open with > Always flow on Windows, Android and iPhone defaults, installer takeover and Office per-extension notes.
Method: documentation only; no commands were run.
