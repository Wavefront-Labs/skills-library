---
id: creative-arts.literary-writing.scrivener.syncing-ios-and-external-folders
name: syncing-ios-and-external-folders
category: creative-arts
field: literary-writing
product: scrivener
tags: [literary-writing, scrivener, scrivener-ios-sync, external-folder-sync, scrivener, scrivener-3, sync, ios, dropbox, plain-text, conflicts]
level: practitioner
status: draft
description: "Sync a Scrivener project with Scrivener for iOS or with an external folder of text or RTF files, and avoid the conflicts and corruption that careless syncing causes."
sources: ["https://www.literatureandlatte.com/learn-and-support/user-guides", "https://www.literatureandlatte.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Syncing with iOS and external folders

**Goal:** edit on phone or tablet, or in another text editor, without damaging the project. Menu names below follow Scrivener 3; shortcuts and exact labels differ between the Mac and Windows editions and by version, so confirm in the app's Help or the official user guide.

## Principles
- **Do not edit the same live Scrivener project from two devices through a shared cloud folder.** Cloud services can create conflicted copies of the project's internal files, which can corrupt it. Use Scrivener's own sync features instead.
- **Close the project before syncing** and allow the sync to finish before opening it elsewhere.
- Keep a backup (`creative-arts.literary-writing.scrivener.automatic-backups-and-restoring`).

## Sync with Scrivener for iOS
1. In the desktop app, use **File > Sync > with Mobile Devices** (Mac) or the equivalent in the Windows version, and choose the sync folder, set up through a service the iOS app supports (Dropbox has long been supported; check the current user guide for other supported services).
2. In the iOS app, link the same service and folder and the project appears.
3. Edit on iOS; then sync on iOS before returning to the desktop; sync on the desktop to merge. The sync merges at the document level.
4. If both sides changed the same document, Scrivener keeps a copy of one version (a conflict handling mechanism, often as a snapshot); check the result and reconcile by hand.

## Sync with an external folder
1. **File > Sync > with External Folder...** and choose a folder. Choose the **format** (plain text, RTF, Markdown where offered) and which parts of the binder sync (typically the Draft).
2. Files in the folder are editable by apps like a plain-text editor or a note app.
3. Sync again after editing: changed files update the project.
4. Use it when you want text in an external editor, a version control tool, or a plain-text format for archive.

## Gotchas
- External-folder sync is text-only; rich formatting and metadata are limited.
- Renaming files in the external folder can create duplicates; edit content, not names.
- Sync after each device session, not at the end of the week.

## Verify
- [ ] Project closed before sync.
- [ ] After sync, word counts match across devices.
- [ ] Conflicts reconciled and a backup taken.
