---
id: computing-software.web-development.web-accessibility.audio-description
name: audio-description
category: computing-software
field: web-development
product: web-accessibility
tags: [time-based-media, audio-description, extended-audio-description, wcag-1-2-5, video]
level: practitioner
status: docs-checked
description: "Meeting WCAG 1.2.3 and 1.2.5 with audio description: when it's needed, writing descriptions for pauses, extended description, text-track descriptions and integrated scripting."
sources:
  - https://www.w3.org/WAI/media/av/description/
  - https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html
  - https://www.rfc-editor.org/rfc/rfc8216
  - https://ableplayer.github.io/ableplayer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audio description

## 1. Requirement
1.2.5 (AA): prerecorded video needs audio description of important visual information not conveyed in the soundtrack. (At A, 1.2.3 allows a descriptive transcript instead.) Needed when visuals carry meaning: on-screen text, demonstrations, actions, charts, scene changes, who is speaking when not named.

## 2. Best approach: integrated description
Script the video so narration describes what matters ("I'm clicking Export in the top right; a dialog lists PDF and CSV"). No separate track needed - cheapest and best for everyone. Plan this in the script stage for product demos and training.

## 3. Separate description track
- Describer writes descriptions that fit in natural pauses; voiced by a narrator or TTS.
- Deliver as an alternate version of the video ("Audio described version" link/toggle) or an alternate audio track (in HLS, an `EXT-X-MEDIA` AUDIO rendition with `CHARACTERISTICS="public.accessibility.describes-video"`, RFC 8216).
- **Extended audio description** (1.2.7 AAA) pauses the video when pauses are too short.
- Text-based description (WebVTT, usually `<track kind="descriptions">`) only works where the player reads it aloud, for example Able Player, which can also pause the video for it; otherwise provide a voiced version.

## 4. Writing descriptions (W3C media guide)
- Describe what's seen, present tense, objectively: "Maria hands him the key." Not interpretations ("Maria seems sad" -> describe the expression).
- Include text shown on screen (titles, names, links) in the main audio or the description, and describe the essential actions; skip what is already audible.
- Don't talk over dialogue or important sounds.

## 5. Player
Provide an accessible control to choose the described version, keyboard-operable and labelled.

## Verify
Listen without watching: can you follow the content and complete the task the video teaches? Review the script against on-screen text and key actions.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 success criteria text, W3C WAI media guide (description page), RFC 8216, Able Player README.
- Confirmed: 1.2.3 is Level A (audio description or media alternative), 1.2.5 is AA, 1.2.7 extended audio description is AAA; integrated, separate-track and text-based description approaches; describe objectively in present tense; `kind="descriptions"` exists on `<track>` (MDN); `public.accessibility.describes-video` is an AUDIO `CHARACTERISTICS` value in RFC 8216; Able Player reads WebVTT description aloud and can pause the video.
- Removed (no longer reachable or unconfirmed): the dead ACB guidelines link and the "name characters once introduced" rule.
Method: documentation only; no commands were run.