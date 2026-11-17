---
id: computing-software.general-digital-literacy.file-management.managing-cloud-storage-quota
name: managing-cloud-storage-quota
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-cloud-storage, cloud-storage-quota, storage-full, google-one, icloud-storage, onedrive-storage]
level: intro
status: docs-checked
description: "See what fills your Google storage, clear the biggest items safely, and know what happens when it is full; same approach for other cloud services."
sources:
  - https://support.google.com/drive/answer/6374270
  - https://support.google.com/googleone/answer/9312312
  - https://support.google.com/drive/answer/2375102
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manage cloud storage quota

**Goal:** stop "storage full" warnings that block email, backups and photo sync.

## What the quota covers (Google)
A Google Account has up to 15 GB shared across Gmail (including Spam and Trash), Drive and Photos. Hidden app data and items left in Drive Trash also count.

## When it is full
You cannot upload or create files in Drive, send or receive email in Gmail, or back up photos. Google says it might delete content if you stay over quota for 2 years.

## Biggest wins
1. Empty Gmail Trash and Spam, Drive Trash and Photos Trash: items in them count until permanently cleared. Allow time (Google says up to 48-72 hours) for the figure to update.
2. Gmail: search `has:attachment larger:10M`, or `older_than:2y has:attachment`, and delete the big ones.
3. Drive: the Storage page lists files largest first. Drive has no built-in duplicate finder; sort by name and look for "(1)" or "Copy of".
4. Files moved to Drive Trash are deleted forever after 30 days; non-owners can only Remove a file, not delete it.

## Other services
iCloud, OneDrive and Dropbox each have their own meter and plan sizes: look them up on the vendor's help pages, and see the vendor's pricing page before buying. Clean up first so you do not pay to store junk.

## Gotchas
- Download originals somewhere else before deleting them from the cloud.
- With Drive for desktop, files you trash in a mirrored or streamed folder are trashed everywhere.

## Verify
- [ ] Storage meter has room; trash emptied; important originals kept elsewhere first.

## Checked
2026-11-01. Confirmed on Google's "Manage your storage in Drive, Gmail & Photos", "How your Google storage works" and "Delete files in Google Drive": 15 GB shared quota, full-account effects, 2-year warning, trash behaviour and 30-day Drive trash, Gmail search operators, Storage page, duplicates advice, Drive for desktop trash. Removed (no page read): iCloud, OneDrive and Dropbox free sizes and menu paths, Messages retention, tier suggestions and the 80% target.

Method: documentation only; no commands were run.
