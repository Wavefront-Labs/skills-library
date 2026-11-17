---
id: creative-arts.animation.voice-tts.take-logging-and-circle-takes
name: take-logging-and-circle-takes
category: creative-arts
field: animation
product: voice-tts
tags: [take-logging, circle-takes, vo-recording, script-supervisor, take-notes, voice-over]
level: practitioner
status: draft
description: "Log every VO take against the script: take numbering, circle takes, ratings, alt reads, wild lines and a log format that editorial can import."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Take logging and circle takes

The take log is what turns a pile of WAVs into an edit. Someone (a script coordinator, the producer or the engineer) logs live while the director directs.

## What to log per take
| Field | Example |
|---|---|
| Line ID | `S014_L07` (scene and line, matching the script and the file-naming scheme) |
| Take number | 3 (restart at 1 for each new line ID) |
| Marker/timecode | session timecode where the take starts |
| Result | **circle** (preferred), good, alt, NG |
| Note | "warmer", "slight clip on 'now'", "cut off at end" |
| Alt/wild | alt read, wild line, pickup |

## Conventions
- **Circle takes** are the director's preferred performance(s); they get cut first in editorial. The term comes from film script supervision where preferred takes were circled in the notes. More than one take can be circled for a line if the director wants to pick between two.
- **Alts** are deliberate variations. Mark them as alts so editorial knows these are not mistakes.
- **NG** takes (not good) are kept in the log (and the session) but marked so nobody cuts them by accident.
- **Wild lines**: efforts and reactions recorded without a script line are logged with their own IDs and a note on the context.
- Record the director's verbal comments ("great, use that one") immediately; do not rely on memory at the end of the day.

## Format
- A shared spreadsheet or the production tracker with one row per take is enough. Export a CSV that editorial can match to files by line ID and take.
- Name files with the same ID and take: `<show>_<ep>_<lineID>_t<take>.wav` (see `vo-file-naming.md`).
- Embed markers in the session at each take start; many DAWs export marker lists that can be pasted into the log.

## Gotchas
- A take log written after the session has errors. Log during.
- Do not renumber takes after the session: file names, notes and the editorial cut all depend on them.

## Verify
- [ ] Every line ID in the script has at least one logged take or an explicit "missed".
- [ ] Circle takes are marked in the file names or metadata as well as the log.
