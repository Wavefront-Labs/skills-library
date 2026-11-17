---
id: creative-arts.animation.sound-design.session-archiving-and-consolidation
name: session-archiving-and-consolidation
category: creative-arts
field: animation
product: sound-design
tags: [session-archive, daw-session, consolidation, archiving, backup, handover, stems]
level: practitioner
status: draft
description: "Archive a finished audio session: consolidate or copy media, print stems, record settings and versions, verify the archive reopens and store it with a manifest."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Session archiving and consolidation

A session that cannot be reopened in two years is lost work. Archive deliberately at the end of each reel and episode.

## What an archive contains
- The session file and all media it references (copy the media; do not rely on links to a work drive).
- Printed stems and the final mix masters (see `m-and-e-mix.md`, `final-mix.md`).
- Reference video file used and the editorial turnover (EDL/AAF) it was conformed from.
- Plug-in list with versions, sample rate, bit depth, frame rate and start timecode in a text file.
- The cue sheet and any music/SFX licence notes (see `music-cue-sheets.md`).

## Steps
1. Finish and save the session; keep a copy of the pre-archive version in case the clean-up goes wrong.
2. **Save a copy** (for example Pro Tools "Save Copy In", or REAPER "Save project as" with the copy-media option) to a new folder, copying all media. Using "copy" avoids breaking the working session.
3. Consolidate only where it reduces file count without destroying edit handles. Keep handles on clips if the dialogue editor might need them.
4. Remove unused media and unused takes, but keep alternate takes (see `take-logging-and-circle-takes.md`) until the delivery is accepted.
5. Render or print the stems, and name them with show, episode, version, date and layout.
6. Write a text manifest and compute checksums (see `checksum-fixity.md` in encode-delivery).
7. **Test**: open the archived copy on another machine and check that all media is online and the picture lines up.
8. Store on two media in different places (see `backup-strategy-3-2-1.md`) and record the location.

## Gotchas
- Plug-ins that are not installed on the future machine will show as inactive; commit rendered stems as the safety net.
- Proprietary session formats change with DAW versions, so keep the stems and an AAF/OMF export as the neutral copy (see `aaf-audio-turnover.md`).

## Verify
- [ ] Archived copy opens elsewhere with all media online.
- [ ] Stems, masters and manifest are in the archive folder.
- [ ] Two copies stored in separate locations.
