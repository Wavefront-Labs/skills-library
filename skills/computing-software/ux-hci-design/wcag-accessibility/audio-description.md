---
id: computing-software.ux-hci-design.wcag-accessibility.audio-description
name: audio-description
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [audio-description, wcag-1-2-5]
level: practitioner
status: docs-checked
description: "Provide audio description for prerecorded video at AA, or media alternative at AAA."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audio description
- 1.2.3 (A): audio description or media alternative for prerecorded video.
- 1.2.5 (AA): audio description for prerecorded video (the AA requirement).
- Describe actions, characters, scene changes and on-screen text that the main soundtrack does not convey; standard description goes in existing pauses in dialogue.
- Extended audio description pauses the video; it is used only when the sense of the video would be lost and the pauses are too short.
- Sufficient techniques: a second user-selectable audio track with descriptions (G78), a version of the movie with descriptions (G173), or narration incorporated in the soundtrack (G226). A static text alternative can describe a talking-head video (G203).
- Failure F113: not using available pauses in dialogue for descriptions of important visual content.

## Gotchas
- If all important information in the video track is already conveyed in the audio track, no additional description is necessary (1.2.3, 1.2.5, 1.2.7).

## Verify
- [ ] Listening without video, the plot and key actions are understandable.

## Checked

- Date: 2026-11-09.
- Read Understanding SC 1.2.5 Audio Description (Prerecorded) (Level AA), including its notes on 1.2.3, 1.2.5 and 1.2.8, sufficient techniques, failure F113 and the key terms for audio description and extended audio description.
- Removed: the level given for 1.2.7, the "described transcript" wording and the "still document it" advice (not stated on the page).

Method: documentation only; no commands were run.
