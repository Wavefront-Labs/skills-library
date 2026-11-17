---
id: creative-arts.music.dj-performance.preparing-usbs-and-exporting-libraries
name: preparing-usbs-and-exporting-libraries
category: creative-arts
field: music
product: dj-performance
tags: [dj-performance, rekordbox, cdj, usb-export, rekordbox-export, export-mode, fat32, exfat, device-library-plus, pro-dj-link, backup-usb, playlists-on-usb, cdj-3000, xdj]
level: practitioner
status: draft
description: "Prepare USB drives for club CDJs: rekordbox Export mode, drive formats, Device Library vs Device Library Plus, syncing playlists and cues, backup USBs and pre-gig checks."
sources: ["https://rekordbox.com/en/download/#manual (rekordbox manual - Export mode, devices)", "https://www.pioneerdj.com/ (CDJ-3000 operating instructions - supported media)", "https://rekordbox.com/en/support/faq/ (USB format and Device Library Plus FAQ)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preparing USBs and exporting libraries

**Goal:** USB drives that load instantly on any club setup with all cues, grids and playlists.

## 1. Drive and format
- Use reliable, fast USB drives or SSDs (two of them). Format **FAT32** for widest compatibility (older CDJs) or **exFAT** where supported (CDJ-3000, newer players, and needed for files over 4 GB); check the venue's player models.
- Some older players don't support exFAT or drives over certain sizes; check the manual.

## 2. Export with rekordbox
- In rekordbox **Export mode** (or Performance mode with the device sidebar), plug in the USB, drag playlists to the device. rekordbox writes tracks plus analysis (grids, waveforms, cues, My Tags) into the device library.
- **Device Library** (legacy, for older CDJs) and **Device Library Plus** (newer, faster, for CDJ-3000/Opus Quad and later firmware): enable the right one(s) in Preferences > Devices; export both if you play various setups.
- Use **Sync Manager** (Device) to keep USB playlists updated with collection changes.
- Analysis on the computer before export (BPM, key, phrase analysis, beat grids checked).

## 3. Serato / Engine / Traktor
- Serato DJ: USB drives for Denon/Engine players via Engine DJ desktop library export; Traktor uses its own export via Traktor or third-party tools. Rekordbox remains the club standard for Pioneer CDJs.

## 4. Pre-gig checks
- Plug the USB into a player (or rekordbox device view) and open playlists; confirm cues and grids.
- Keep a **backup USB** with the same export; carry headphones adapter and spare drive.
- Know Pro DJ Link: one USB can serve linked players; still bring two drives.

## Gotchas
- Copying files manually onto USB (Finder/Explorer): players see files without analysis or cues.
- Old firmware on venue players not supporting Device Library Plus or exFAT.
- Ejecting USB without unmounting: corrupted library.

## Verify
- Test the USB on the same player model as the venue (or check the rider) before the gig.
- Random track from each playlist loads with grid and cues on a CDJ.
