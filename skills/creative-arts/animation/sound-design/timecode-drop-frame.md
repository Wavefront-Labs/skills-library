---
id: creative-arts.animation.sound-design.timecode-drop-frame
name: timecode-drop-frame
category: creative-arts
field: animation
product: sound-design
tags: [drop-frame, timecode, audio-sync, non-drop-frame, 29-97, smpte-12m, session-start, timecode-offset, 23-976-timecode]
level: practitioner
status: draft
description: "Get timecode right across picture and sound: drop-frame vs non-drop, 23.976 counting, session start times like 00:59:58:00, and computing offsets between systems."
sources:
  - https://www.smpte.org/
  - https://ffmpeg.org/ffmpeg-filters.html#drawtext-1
  - https://www.avid.com/learn-and-support
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timecode and drop-frame

**Goal:** picture editorial, sound and delivery agree on what "01:02:13:04" means, so spotting notes, AAF
turnovers and QC reports point at the same frame.

## Counting rules

- Timecode counts frames in hours:minutes:seconds:frames at an integer **nominal** rate (24, 25, 30).
- 23.976 fps uses **24-frame non-drop** counting: timecode runs 0.1% slower than the wall clock (an hour of TC
  lasts 1 h 3.6 s real time).
- 29.97 fps can be **drop-frame (DF)**: skips frame numbers 00 and 01 at the start of every minute except every
  tenth minute, so TC matches clock time. Written with a semicolon: `01:00:00;00`. Non-drop uses colons.
- Drop-frame drops **numbers**, never actual frames.
- 59.94 DF drops 4 numbers per minute similarly.
- There is no drop-frame for 23.976 or 25.

## Conventions

- Programme starts at **01:00:00:00**; sessions often start at 00:59:52:00 or 00:59:58:00 to hold leader and
  2-pop (pop at 00:59:58:00 for a 2-second pre-roll).
- Reels for features: reel 1 at 01:00:00:00, reel 2 at 02:00:00:00, etc.

## Frames from timecode (non-drop)

```python
def tc_to_frames(tc, fps):            # fps = nominal integer rate, e.g. 24 for 23.976
    h, m, s, f = map(int, tc.replace(";", ":").split(":"))
    return ((h*60 + m)*60 + s)*fps + f
offset = tc_to_frames("01:02:13:04", 24) - tc_to_frames("01:00:00:00", 24)   # 53116 frames into the show
```
For DF, use a library (e.g. `timecode` on PyPI) rather than hand-rolled maths.

## Mismatch symptoms

| Symptom | Likely cause |
|---|---|
| sound lands 1 hour off | session start TC differs (00:00:00:00 vs 01:00:00:00) |
| offset grows ~3.6 s per hour | 23.976 vs 24 real-time mix-up |
| offsets of a couple of frames each minute | DF vs NDF confusion at 29.97 |

## Verify

Pick three events (2-pop, a mid-programme cut, the last frame of action) and confirm their TC is identical in
the NLE, the DAW session and the delivery file's burn-in.
