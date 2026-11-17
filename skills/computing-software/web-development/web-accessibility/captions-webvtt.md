---
id: computing-software.web-development.web-accessibility.captions-webvtt
name: captions-webvtt
category: computing-software
field: web-development
product: web-accessibility
tags: [time-based-media, webvtt, closed-captions, wcag-1-2-2, wcag-1-2-4, video]
level: practitioner
status: verified
description: "Captioning prerecorded and live video to WCAG 1.2.2 and 1.2.4: WebVTT format, caption quality rules, sound descriptions, sync, styling, and live caption options."
sources:
  - https://www.w3.org/WAI/media/av/captions/
  - https://www.w3.org/TR/webvtt1/
  - https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
  - https://www.w3.org/WAI/WCAG22/Understanding/captions-live.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Captions (WebVTT)

## 1. Requirements
- 1.2.2 (A): captions for all prerecorded audio in synchronised media.
- 1.2.4 (AA): captions for live audio in synchronised media (webinars, live streams).
Captions = dialogue + speaker identification + meaningful sounds, synchronised. Subtitles (translation only) don't satisfy this for same-language audio.

## 2. WebVTT
```
WEBVTT

00:00:01.000 --> 00:00:04.200
<v Dana>Welcome to the quarterly update.

00:00:04.400 --> 00:00:06.000 line:85%
[upbeat music]

00:00:06.100 --> 00:00:09.500
<v Sam>Thanks, Dana. Let's start with revenue.
```
```html
<video controls crossorigin="anonymous">
  <source src="update.mp4" type="video/mp4">
  <track kind="captions" src="update.en.vtt" srclang="en" label="English (CC)" default>
</video>
```
Serve as `text/vtt`, CORS headers if cross-origin. Style with `::cue { font-size: 1.2em; background: rgb(0 0 0 / .8); }` but let user caption preferences override.

## 3. Quality rules (DCMP Captioning Key)
- Verbatim versus edited is a debated choice (DCMP describes both camps); keep the original meaning and essential vocabulary, with correct spelling, punctuation and names.
- DCMP Captioning Key: preferably no more than two lines per caption, minimum duration 40 frames (1 s 10 frames), maximum 6 s (music notation excepted), presentation rate at most 130 wpm (lower-level), 140 (middle) or 160 (upper-level educational media). DCMP sets no characters-per-line figure; broadcast style guides differ, so follow your client's spec.
- Identify speakers when not obvious; describe relevant sounds `[door slams]`, `[laughter]`, music with mood `[tense music]`.
- Don't cover important on-screen text (use `line:` positioning).
- Auto-generated captions (YouTube, Whisper) are a starting draft - edit them; uncorrected ASR typically fails accuracy needs for names, numbers and terms.

## 4. Live
CART (human real-time captioners) for high-stakes events; platform live captions (Zoom, Teams, YouTube Live) are ASR - acceptable fallback with disclosure; publish corrected captions on the recording afterwards.

## 5. Players
Third-party players must expose a CC button reachable by keyboard and respect user styling (YouTube, Vimeo, Able Player, Video.js do).

## Verify
Watch with sound off: can you follow everything? Check sync at start/middle/end; validate the VTT. The example above loaded in Chromium as three cues (`<v Dana>` became a span titled Dana; `line:85%` set `snapToLines` to false).
