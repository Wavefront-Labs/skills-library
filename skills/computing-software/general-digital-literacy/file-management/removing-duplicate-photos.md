---
id: computing-software.general-digital-literacy.file-management.removing-duplicate-photos
name: removing-duplicate-photos
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-media, duplicate-photos, photo-library-cleanup, storage]
level: intro
status: draft
description: "Find and remove duplicate and near-duplicate photos with Apple Photos' Duplicates album, Google Photos, Windows tools and careful manual checks, without deleting the only copy."
sources:
  - https://support.apple.com/guide/photos/welcome/mac
  - https://support.google.com/photos
  - https://www.digikam.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Remove duplicate photos

## Apple Photos (iOS 16+, macOS Ventura+)
- **Utilities > Duplicates** album lists exact copies and copies with different resolution or metadata.
- **Merge** keeps the best-quality version and combines metadata (captions, keywords, favourites); the rest go to Recently Deleted (30 days).

## Google Photos
- Byte-identical uploads are skipped automatically. Near-duplicates (bursts, edited copies) aren't merged; the *Photo stacks* feature groups similar shots so you can pick the best and delete the others.

## Windows and folders of files
- Windows Photos has no duplicate finder. Use a reputable tool: **dupeGuru** (free, open source, picture mode for near-matches) or **digiKam** (*Tools > Find Duplicates*).
- Sort by size and date in File Explorer to spot obvious copies like `IMG_0001 (1).jpg`.

## Safe method
1. **Back up first** (a full copy elsewhere).
2. Compare candidates at full size; "similar" may be different moments.
3. Keep the original/highest resolution; delete copies from messaging apps (smaller, stripped metadata).
4. Empty Recently Deleted/Recycle Bin only after a week of checking.

## Why duplicates happen
- Importing the same card twice; syncing both iCloud and Google Photos to one PC; WhatsApp saving media to the gallery (turn off *Media visibility*).

## Verify
- [ ] Library count dropped and spot checks show one good copy of each photo remains.
