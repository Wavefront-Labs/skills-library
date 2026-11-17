---
id: creative-arts.animation.editorial.leaders-and-two-pops
name: leaders-and-two-pops
category: creative-arts
field: animation
product: editorial
tags: [two-pop, leader, tail-pop, sync-pop, countdown, smpte-leader, picture-lock, av-sync, conform]
level: practitioner
status: draft
description: "Build head leaders with a 2-pop and tail pops on every reel or episode so picture and sound sync can be checked and fixed at every hand-off."
sources:
  - https://www.smpte.org/
  - https://partnerhelp.netflixstudios.com/hc/en-us
  - https://ffmpeg.org/ffmpeg-filters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leaders and 2-pops

**Goal:** a universal sync reference at the head and tail of every reel, so any department can prove picture and
sound are aligned.

## Standard layout (24 fps, programme at 01:00:00:00)

| Timecode | Picture | Sound |
|---|---|---|
| 00:59:50:00 | leader start (countdown from 8, SMPTE or Academy style) | silence |
| 00:59:58:00 | single frame with the "2" (or a white flash frame) | **1 frame of 1 kHz tone at -20 dBFS** (the 2-pop) |
| 00:59:58:01 to 00:59:59:23 | black | silence |
| 01:00:00:00 | first frame of action (FFOA) | programme |
| LFOA + 2 s | one flash frame | 1 frame tail pop |

The 2-pop is exactly **2 seconds before** first frame of action, hence the name. Some deliverables (e.g. platform
IMF or ProRes masters) specify their own head build such as bars and tone then black; follow the spec for the final
master, but keep pops on every internal hand-off (turnovers, AAFs, mix stems).

## Making one

- NLEs ship countdown generators (Premiere *Universal Counting Leader*, Resolve Generators); make sure the beep
  frame is exactly 2 s before FFOA at the project frame rate.
- ffmpeg can generate a pop for a test: `ffmpeg -f lavfi -i "sine=f=1000:d=0.0417" -af volume=-20dB pop.wav`
  (one frame at 24 fps is 1/24 s = 0.0417 s).

## Using it

- Sound posts its stems with the same pops; in the DAW, line up the pop with the flash frame on video
  (see `creative-arts.animation.sound-design.video-sync-in-the-daw`).
- When sync is in doubt, measure the offset at the head pop and tail pop: equal offsets mean a slip; different
  offsets mean a rate problem (see `creative-arts.animation.encode-delivery.av-sync-offset-correction`).

## Verify

Scrub to 00:59:58:00: the flash frame and the 1-frame tone coincide exactly on head and tail, in the cut and in every
stem returned from the mix.
