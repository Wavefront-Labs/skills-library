---
id: computing-software.ux-hci-design.wcag-accessibility.captions-and-transcripts
name: captions-and-transcripts
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [captions-wcag, media-transcripts, wcag-time-based-media]
level: practitioner
status: docs-checked
description: "Supply captions for prerecorded and live synchronised media (SC 1.2.1, 1.2.2, 1.2.4) and alternatives for audio-only and video-only media."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
  - https://www.w3.org/TR/WCAG22/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Captions
- 1.2.1 (A) prerecorded audio-only: an alternative for time-based media with equivalent information. Prerecorded video-only: such an alternative or an audio track with equivalent information.
- 1.2.2 (A) captions for prerecorded synchronised media.
- 1.2.4 (AA) captions for live synchronised media.
- Captions include dialogue, identify who is speaking, and include non-speech information conveyed through sound (sound effects, music, laughter, location).
- HTML technique H95: use the `track` element to provide captions.

## Verify
- [ ] Mute playback: all dialogue and key sounds are understandable from the captions.

## Checked

- Date: 2026-11-09.
- Confirmed against WCAG 2.2 success criteria 1.2.1, 1.2.2 and 1.2.4 (levels and wording) and Understanding SC 1.2.2 Captions (Prerecorded): speaker identification, non-speech sounds, technique H95. The TR page was searched for the 1.2 criteria rather than read in full.
- Removed: the word "transcript" for 1.2.1 (the criterion says alternative for time-based media), the `track` attributes and WebVTT, and the gotchas on auto-generated and burned-in captions (not stated on the pages).

Method: documentation only; no commands were run.
