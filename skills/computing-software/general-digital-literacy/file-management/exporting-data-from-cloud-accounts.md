---
id: computing-software.general-digital-literacy.file-management.exporting-data-from-cloud-accounts
name: exporting-data-from-cloud-accounts
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-backup, google-takeout, export-account-data, data-portability]
level: intro
status: docs-checked
description: "Download a full copy of your data from Google Takeout and Apple Data and Privacy, and keep the archive usable and safe."
sources:
  - https://support.google.com/accounts/answer/3024190
  - https://support.apple.com/en-us/102208
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Export data from cloud accounts

An account lockout, a ban or a closed service can take years of email and photos with it. Export before closing any
account and on a regular schedule.

## Google Takeout
- Use Google Takeout, choose the products, then the archive format and size. A 50 GB size limit is offered to reduce the
  chance the archive is split into parts.
- You can have Google email a download link or add the archive to Drive. The archive expires in about 7 days, after which
  you must create a new one.
- Special software may be needed to unpack a `.tgz` archive: choose `.zip` if you prefer.

## Apple
- Request a copy of your data from Apple's Data and Privacy page. Apple verifies the request, then posts the data to that
  page and notifies you. You have 14 days to download it, after which it is removed.
- Photos, videos and documents come in their original formats; contacts, calendars, bookmarks and mail come in formats such
  as `.vcf`, `.ics`, `.html` and `.eml`; some usage data is in `.json`, `.csv` or `.pdf`.
- Apple masks some details (payment and bank details) in the export.

## Other services
Microsoft, Facebook, Instagram, X, TikTok and LinkedIn each have a data-download feature in the account settings; the menu
paths change often, so search the service's help for "download your data" rather than following a remembered path.

## Keep it usable and safe
- Unzip and check that a few photos and emails open before you delete anything at the source.
- Exports contain everything (messages, location history): store on an encrypted drive and delete stray copies from Downloads.

## Verify
- [ ] The archive downloads fully, unzips without errors, and sample photos/emails open.

## Checked
2026-10-28. Confirmed (Google Account Help, Download your data; Apple Support, Request a copy of your data): 50 GB size limit
option, archive expiry about 7 days, add-to-Drive option, tgz software note, Apple 14-day download window, file formats, masked
details. Corrected: Apple "takes up to 7 days" (not stated; the page gives a 14-day download window). Removed: per-product
Google formats (MBOX, JSON metadata, converted Drive files), "Export once", Mac Download Originals, Microsoft and Facebook
menu paths (Facebook page unreadable), Thunderbird advice.
Method: documentation only; no commands were run.
