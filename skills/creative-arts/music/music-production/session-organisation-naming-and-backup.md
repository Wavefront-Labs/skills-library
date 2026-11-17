---
id: creative-arts.music.music-production.session-organisation-naming-and-backup
name: session-organisation-naming-and-backup
category: creative-arts
field: music
product: music-production
tags: [music-production, session-organisation, session-backup, file-naming, folder-structure, 3-2-1-backup, save-as-versions, collect-all-and-save, save-copy-in, track-sheet, session-notes]
level: practitioner
status: draft
description: "Keep sessions organised and safe: folder structures, naming conventions, versioned saves, collecting all media, session notes, and a 3-2-1 backup routine for studio projects."
sources: ["https://www.grammy.com/ (Recording Academy P&E Wing - Recommendations for Delivery of Recorded Music Projects and file naming)", "https://www.ableton.com/en/live-manual/12/managing-files-and-sets/ (Collect All and Save)", "https://www.avid.com/pro-tools (Save Copy In)", "https://support.apple.com/guide/logicpro/ (project packages and consolidate)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Session organisation, naming and backup

**Goal:** any session can be opened, understood and restored by anyone, years later.

## 1. Folder structure
```
Artist/
  Song_Title/
    01_Session/        (DAW session + Audio Files)
    02_References/
    03_Lyrics_Charts/
    04_Bounces/        (roughs, mixes, stems)
    05_Admin/          (splits, credits, notes)
```

## 2. Naming
- Tracks named before recording ("Kick In", "Gtr Rhy L") so files are named meaningfully.
- Session versions: `Song_Title_v01_tracking`, `_v02_edits`, `_v03_mix` - **Save As** at each milestone instead of overwriting.
- Bounces: `Artist_Song_Mix_v04_2026-10-16.wav`; include version and date.

## 3. Self-contained sessions
- **Ableton**: File > Collect All and Save (copies samples/media into the project folder).
- **Pro Tools**: File > Save Copy In with "All audio files" (and plugin settings) for transfers.
- **Logic**: save as Package/Folder with Audio, Sampler, and other assets copied in (File > Project Management > Consolidate).

## 4. Session notes
- Track sheet/notes: musicians, instruments, mics, preamps, settings, tempo, key, takes chosen, comp decisions, plugin versions. Store as a text file in the session folder.
- Credits and splits (see split-sheet skill).

## 5. Backups (3-2-1)
- **3 copies, 2 media types, 1 off-site**: working drive + local backup drive (scheduled, e.g. nightly) + cloud or off-site drive.
- Back up at the end of every session before leaving.
- Test restores occasionally.

## 6. Archiving
- At project end: print stems/multitracks as plain WAVs from bar 1 (so they open in any DAW without plugins), plus the session; archive with notes.

## Gotchas
- Samples left in a system library: session opens with missing files on another computer.
- Single drive "backups" on the same disk as the session.

## Verify
- Copy the project folder to another computer: it opens with no missing files.
- Restore test from backup succeeds.
