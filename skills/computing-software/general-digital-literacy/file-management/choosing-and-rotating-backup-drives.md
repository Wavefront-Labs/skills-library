---
id: computing-software.general-digital-literacy.file-management.choosing-and-rotating-backup-drives
name: choosing-and-rotating-backup-drives
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-backup, backup-drive, 3-2-1-backup, offsite-backup, drive-rotation]
level: intro
status: draft
description: "Pick an external backup drive of the right size and type, rotate two drives so one is always off-site, and replace drives before they fail."
sources:
  - https://www.cisa.gov/sites/default/files/publications/data_backup_options.pdf
  - https://www.backblaze.com/blog/the-3-2-1-backup-strategy/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Choose and rotate an external backup drive

## Choosing
- **Size:** at least **2× the data you back up** (versioned backups like File History/Time Machine keep old copies). 1 TB used → 2-4 TB drive.
- **HDD** (cheap, large, fragile when dropped) for desk backups; **portable SSD** (tough, fast, pricier) if it travels.
- USB-C/USB 3; a drive that powers from the cable is simpler. Avoid the oldest unknown-brand "16 TB for £20" sticks — fake capacity is common (test with H2testw / F3).
- Format for the backup tool: NTFS for Windows File History or imaging; APFS for Time Machine (it reformats).

## 3-2-1 and rotation
- 3 copies, 2 different media, 1 off-site. A drive next to the PC dies with it in a fire, flood or burglary, and ransomware encrypts a drive left plugged in.
- Two drives, A and B: A at home doing backups, B at work/a relative's. Swap monthly (or weekly for busy data). Label them with the date of last swap.
- Unplug the home drive between backups, or use cloud backup as the off-site copy.
- Both Time Machine and Windows imaging tools accept multiple drives and alternate automatically.

## Lifespan
- Replace drives every 4-5 years or on first warning: clicking, slow copies, SMART warnings (CrystalDiskInfo on Windows, Disk Utility › First Aid on Mac).
- Restore-test a file from each drive at every swap.

## Verify
- [ ] Two drives each hold a backup less than a month old, one of them away from home.
