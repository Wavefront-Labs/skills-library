---
id: computing-software.digital-privacy-hygiene.privacy-configuration.exporting-data-with-google-takeout
name: exporting-data-with-google-takeout
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, google-takeout, data-portability, google, backups, google-photos, account-deletion]
level: intro
status: docs-checked
description: "Export Google account data with Takeout: choose products, delivery, one-off or scheduled export, file type and size, Photos metadata, and store the archive securely."
sources:
  - "https://support.google.com/accounts/answer/3024190"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting data with Google Takeout

**Goal:** a complete, usable copy of what Google holds, for backup, migration or before deleting an account.

## Run an export
1. Open Takeout (linked from the Google Account Help page). Products you use are pre-selected; uncheck the ones you
   do not want. Some products have an **All data included** button to exclude specific items.
2. **Delivery**: an emailed download link, or send the archive to Google Drive, Dropbox, Microsoft OneDrive or Box.
3. **Export type**: a one-time archive, or a scheduled export that creates an archive every 2 months for one year
   (the first archive is created immediately). For Google Photos, scheduled exports work only if Photos is the
   only product selected, and they are not available under the Advanced Protection Program.
4. **File type and size**: Zip or Tgz (Tgz may need extra software on Windows). Data over the size limit is split
   into several archives; Google recommends the 50 GB limit to reduce splitting.
5. Wait: creation takes from a few minutes to a few days. Archives expire in about 7 days and each can be
   downloaded 5 times, so download promptly.

## Google Photos metadata
The original capture timestamp stays in the file's embedded metadata, though your operating system may stamp the
downloaded file with a new date. Extra metadata not in the original file, such as comments, goes into a secondary
JSON file. Check the result before importing the photos elsewhere.

## Store safely
The archive is your whole digital life: keep it on an encrypted drive, delete the downloaded archives from
Downloads once moved, and remove copies from cloud destinations you no longer need.

## Before deleting an account
Verify the export opens (sample emails, photos with right dates) before using Google's account-deletion option.

## Verify
- [ ] Archive downloaded within the expiry window, extracts without errors, stored encrypted.

## Checked
2026-11-01. Confirmed against Google Account Help "Download your data": pre-selected products, All data included,
delivery destinations, one-time vs every 2 months for one year, Photos-only scheduling rule, Advanced Protection
note, Zip/Tgz, 50 GB recommendation, creation time, 7-day expiry, 5 downloads, Photos metadata behaviour. Removed
as unconfirmed: Deselect all button, per-product format table, 2-50 GB range, third-party merge tools and the
other source URLs (not read).
Method: documentation only; no commands were run.
