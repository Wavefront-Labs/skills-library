---
id: computing-software.web-development.web-accessibility.transcripts-for-audio-and-video
name: transcripts-for-audio-and-video
category: computing-software
field: web-development
product: web-accessibility
tags: [time-based-media, transcripts, podcasts, wcag-1-2-1, wcag-1-2-8]
level: practitioner
status: docs-checked
description: "Producing transcripts for audio-only and video-only media under WCAG 1.2.1, and descriptive transcripts for video: structure, placement, speaker labels and visual information."
sources:
  - https://www.w3.org/WAI/media/av/transcripts/
  - https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html
  - https://www.w3.org/WAI/WCAG22/Understanding/media-alternative-prerecorded.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transcripts

## 1. Requirements
- 1.2.1 (A): **audio-only** (podcasts, recordings) needs a text transcript; **video-only** (silent animations, screen recordings without narration) needs a transcript describing the visuals or an audio track.
- 1.2.3 (A) / 1.2.8 (AAA): a full "media alternative" (descriptive transcript) for video can substitute for audio description at A, and is required at AAA.
Transcripts are needed by deaf-blind users (via braille displays) among others, and also help search and skimming.

## 2. What goes in
- All speech, with speaker names.
- Meaningful sounds `[applause]`.
- For video (descriptive transcript): key visual information - on-screen text, actions, scene changes, slides content - in brackets or a "Visual:" paragraph at the right point.
- Optional timestamps per section for long media.

## 3. Structure and placement
```html
<section aria-labelledby="ep12-t">
  <h2 id="ep12-t">Episode 12 transcript</h2>
  <p><strong>Dana:</strong> Welcome back…</p>
  <p>[Slide shows: "Revenue up 12%"]</p>
</section>
```
- Usually put it on the same page as the media; a separate page is fine when the media is hosted elsewhere (W3C media guide).
- `<details>` to collapse long transcripts is fine.
- Use headings for long transcripts so users can navigate topics.
- Interactive transcripts (click to seek, highlight current line) are a bonus; keep the plain text accessible.

## 4. Production
Generate from captions/ASR, then edit: correct names, add speakers and visual descriptions. Publish at the same time as the media, not later.

## Verify
Someone who can't hear or see the media can get the same information from the transcript; check it's reachable by keyboard and screen reader near the player.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 success criteria text, W3C WAI media guide (transcripts).
- Confirmed: 1.2.1 is Level A (audio-only needs a transcript; video-only needs a descriptive transcript or an audio track); 1.2.8 Media Alternative is AAA; 1.2.3 allows a media alternative instead of audio description at A; transcripts identify speakers, may add bracketed clarifications, use timestamps only when useful, are usually best on the same page; descriptive transcripts help deaf-blind users.
- Removed (no documentation found): the "only option" wording and the non-native-speaker benefit.
Method: documentation only; no commands were run.