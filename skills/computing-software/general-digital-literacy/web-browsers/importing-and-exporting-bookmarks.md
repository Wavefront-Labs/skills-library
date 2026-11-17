---
id: computing-software.general-digital-literacy.web-browsers.importing-and-exporting-bookmarks
name: importing-and-exporting-bookmarks
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, bookmarks, import-bookmarks, export-bookmarks, bookmarks-html, switch-browser, migrate-bookmarks, backup-bookmarks]
level: intro
status: docs-checked
description: "Move bookmarks between Chrome and Safari with their import and export tools, using a bookmarks HTML file as the common format, and handle exported files safely."
sources:
  - https://support.google.com/chrome/answer/96816
  - https://support.google.com/chrome/answer/188842
  - https://support.apple.com/guide/safari/import-bookmarks-and-passwords-ibrw1015/mac
  - https://support.apple.com/guide/safari/export-browsing-data-ibrwebf10132/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing and exporting bookmarks

**Goal:** switch browsers or computers without losing bookmarks.

## Chrome
- **Import:** export your old browser's bookmarks as an HTML file, then in Chrome choose More > **Bookmarks and lists** > **Import bookmarks and settings** > **Choose file**, pick the file and select Open > Done.
- **Where they land:** if Chrome had no bookmarks, imports appear on the bookmarks bar; otherwise they go into an "Other bookmarks" folder at the end of the bar.
- **Export:** More > Bookmarks and lists > **Bookmark Manager** > More (top) > **Export Bookmarks**. Chrome writes an HTML file that other browsers can import.

## Safari (Mac)
- **Import from Chrome or Firefox:** File > **Import From Browser** > Google Chrome or Firefox (the browser must be installed). Imported bookmarks appear after your existing ones. HTML bookmark files exported from Firefox, Edge, Chrome and some others can also be imported.
- **Export:** File > **Export Browsing Data to File**, choose what to export (bookmarks, history, extensions, credit cards, passwords; with profiles you choose one or All Profiles), click Download, Save. The result is a **.zip** file.
- Apple warns the export is **not encrypted**: delete it after importing it elsewhere.

## Easier: sync
Signing in to the same browser account on the new computer brings bookmarks across (Chrome: sign in with your Google Account). Use an HTML file or export when changing browser brands.

## Gotchas
- A Safari export that includes passwords or cards is an unencrypted file: delete it after import.
- Edge and Firefox import and export menus are not covered here (see Checked).

## Verify
- [ ] Bookmark count and folders in the new browser match the old.

## Checked
2026-10-27. Chrome Help (Import Chrome bookmarks and settings; Create, find and edit bookmarks) and Apple's Safari User Guide (import from another browser; export Safari data) were read. Confirmed the Chrome and Safari menu paths, where Chrome imports land and that Safari's export is an unencrypted zip. Edge and Firefox are not covered because those pages could not be confirmed. Method: documentation only; no commands were run.
