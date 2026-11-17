---
id: computing-software.digital-privacy-hygiene.device-hardening.backing-up-photo-libraries
name: backing-up-photo-libraries
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, photo-backup, icloud-photos, google-photos, backups]
level: practitioner
status: draft
description: "Back up iCloud and Google Photos libraries properly: full-resolution originals, a second independent copy, export tools, and avoiding optimise-storage traps."
sources:
  - "https://privacy.apple.com/"
  - "https://support.google.com/accounts/answer/3024190"
  - "https://immich.app/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Photo library backup

**Goal:** irreplaceable photos survive account loss, accidental deletion and a dead phone.

## The trap
iCloud Photos and Google Photos are **sync**: deleting on the phone deletes everywhere (after 30 days in Recently
Deleted/Trash). "Optimize Storage" means the phone holds thumbnails only; the originals exist only in the cloud.

## Second copy, independent of the first
| Source | Method |
|---|---|
| iCloud Photos | Mac Photos app with **Download Originals to this Mac**, then Time Machine/restic; or Windows iCloud app download; or privacy.apple.com data copy |
| Google Photos | Google Takeout (scheduled every 2 months for a year), or desktop sync via rclone |
| Android/iPhone direct | Self-hosted Immich, Nextcloud, or Syncthing to a home computer/NAS |
| End-to-end encrypted | Ente Photos as a second cloud copy |

## Routine
1. Ensure one computer or NAS holds full originals (check file sizes, not thumbnails).
2. Back that up with versioning to a second medium and off-site.
3. Quarterly, open a random sample from the backup to confirm it isn't corrupted.

## Gotchas
- Takeout exports JSON sidecars for dates and locations; tools like `exiftool` or immich-go restore them.
- Shared albums and partner sharing don't count as backup.
- Losing access to the account (forgotten password, ban, death) is a common way to lose photos; set a legacy contact.
