---
id: creative-arts.animation.sound-design.music-cue-sheets
name: music-cue-sheets
category: creative-arts
field: animation
product: sound-design
tags: [cue-sheet, music-cue-sheet, pro, performance-royalties, ascap, bmi, prs, rapidcue, music-post, deliverables]
level: practitioner
status: draft
description: "Prepare the music cue sheet for an episode or film: cue numbering, timings, usage codes, composers, publishers and PRO shares, filed so royalties flow and deliverables pass."
sources:
  - https://www.ascap.com/help/music-business-101
  - https://www.bmi.com/
  - https://www.prsformusic.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Music cue sheets

**Goal:** a complete record of every music use in the final programme, required by broadcasters and streamers
and used by performing rights organisations (PROs) to pay composers and publishers.

## Contents per cue

| Field | Example |
|---|---|
| Cue number | 1M04 (reel/episode 1, music cue 4) |
| Title | "Night Drive" |
| Usage | BI background instrumental, BV background vocal, VI visual instrumental, VV visual vocal, MT main title, ET end title |
| Timing in / out and duration | 00:14:22 - 00:15:03, 0:41 |
| Composer(s) with PRO and share | J. Smith (ASCAP) 100% |
| Publisher(s) with PRO and share | Show Music Publishing (ASCAP) 100% |
| Source | score / library (library name + track ID) / commercial |

Header: production title, episode title and number, production company, air/release date, duration, distributor.

## Method

1. Export a list of music clips with timecodes from the final mix session or the locked timeline (the music stem
   track's clip list).
2. Merge consecutive uses of the same cue separated only by an edit into one entry; separate uses get separate
   entries.
3. Durations to the second, from the **final** programme (not the mix session with handles).
4. Fill composer/publisher data from the score contract and library metadata.

## Filing

The producer or distributor files with the PROs (in the US, ASCAP/BMI accept submissions; cue-sheet services such
as RapidCue or Soundmouse automate filing). Deliver the cue sheet with the deliverables package; many streamer
specs list it as mandatory.

## Verify

Total music time on the cue sheet equals music time measured on the final music stem; every cue has composer and
publisher shares adding to 100% and a licence reference (`creative-arts.animation.sound-design.music-licensing-sync-and-master`).
