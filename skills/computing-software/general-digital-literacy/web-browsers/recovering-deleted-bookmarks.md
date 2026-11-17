---
id: computing-software.general-digital-literacy.web-browsers.recovering-deleted-bookmarks
name: recovering-deleted-bookmarks
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, bookmarks, history, recover-bookmarks, bookmarks-backup, restore-bookmarks]
level: practitioner
status: gated
description: "Get back deleted bookmarks: what Chrome's help says, why an exported HTML backup matters, and the browser-specific recovery routes that could not be confirmed."
sources:
  - https://support.google.com/chrome/answer/188842
  - https://support.google.com/chrome/answer/96816
  - https://support.apple.com/guide/safari/export-browsing-data-ibrwebf10132/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recover deleted bookmarks

Act fast and **do not close the browser** if you can undo. Turn sync off before restoring any file so the deletion does not sync back to the restored copy.

## What the documentation confirms
- **Chrome:** Chrome's help states that after you delete a bookmark you cannot get it back from the bookmark manager. Recovery therefore relies on a backup you made earlier or on another device that has not yet synced.
- **Backups you can make now:** Chrome: Bookmark Manager > More > **Export Bookmarks** writes an HTML file. Safari: File > **Export Browsing Data to File** writes an unencrypted .zip that includes bookmarks (delete it after use).
- **Restore from a backup:** import the HTML file (Chrome: More > Bookmarks and lists > Import bookmarks and settings > Choose file).

## Routes that could not be confirmed
- Undo with Ctrl+Z in the bookmark manager (Chrome, Edge, Firefox) (gated: unconfirmed, source is paywalled or blocked). Try it immediately after deleting.
- Chrome or Edge profile-folder method using the `Bookmarks.bak` file next to `Bookmarks` (gated: unconfirmed, source is paywalled or blocked). It is a manual file swap with the browser closed; keep a copy of the current file before replacing anything.
- Firefox dated bookmark backups under the Library window's Import and Backup menu (gated: unconfirmed, source is paywalled or blocked). The Firefox support site could not be read.
- Edge "Restore deleted favourites" (gated: unconfirmed, source is paywalled or blocked).
- Safari iCloud bookmark restore and Time Machine restore of the Safari bookmarks file (gated: unconfirmed, source is paywalled or blocked).

## Prevent
Export bookmarks to HTML now and then and store the file somewhere safe; keep sync on.

## Verify
- [ ] The missing folder reappears after import; then re-enable sync and confirm it stays.

## Checked
2026-10-27. Chrome Help (Create, find and edit bookmarks; Import Chrome bookmarks and settings) and Apple's Safari User Guide (Export Safari data) were read. Confirmed that Chrome offers no restore for deleted bookmarks and the export and import steps above. The undo, Bookmarks.bak, Firefox, Edge and Safari/iCloud recovery routes are marked gated. Method: documentation only; no commands were run.
