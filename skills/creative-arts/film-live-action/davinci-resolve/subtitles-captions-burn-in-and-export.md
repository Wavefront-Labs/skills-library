---
id: creative-arts.film-live-action.davinci-resolve.subtitles-captions-burn-in-and-export
name: subtitles-captions-burn-in-and-export
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, subtitle-track, caption-editing, resolve-subtitles, subtitle-burn-in, subtitle-export, srt-export, auto-captions, imsc, closed-captions]
level: practitioner
status: draft
description: "Create and deliver subtitles in Resolve: subtitle tracks, importing SRT, auto transcription captions, styling, then burn-in or sidecar export (SRT/WebVTT/IMSC) from the Deliver page."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Subtitles and Captions; Deliver page subtitle settings)"
  - "https://partnerhelp.netflixstudios.com (Netflix - Timed Text Style Guide)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subtitles and captions: tracks, burn-in and export

**Goal:** accurate, readable subtitles authored in the timeline and delivered in the
form each platform wants.

## 1. Subtitle tracks (Edit page)
- **Add Subtitle Track** (right-click the track header area). Add subtitles with the
  Effects > Titles > Subtitle item, or **import an SRT** (Media Pool import, then drag to
  the subtitle track - it lands as editable captions).
- One track per **language**; name tracks ("EN", "ES - forced").
- **Auto transcription**: *Timeline > Create Subtitles from Audio* (Studio version) to
  generate captions from dialogue, then edit for accuracy.

## 2. Editing and style
- Inspector shows each caption's text and timing; **track-level style** (font, size,
  outline, background, position) applies to all captions on the track.
- Follow the platform guide (e.g. Netflix Timed Text Style Guide): max 42 characters per
  line, 2 lines, reading speed limits (e.g. 17-20 characters/second for adults), minimum
  duration ~5/6 s, gaps between events, shot-change rules.
- Captions for accessibility (SDH) include speaker IDs and sound descriptions [door
  slams].

## 3. Delivery from the Deliver page
In the render settings > **Subtitle Settings**:
- **Export Subtitle**: check it; choose **As a separate file** (SRT, WebVTT, or other
  available formats per version), **Burn into video**, or **As embedded captions** (in
  supported containers like MXF/MOV for broadcast).
- Choose which subtitle tracks to export.
- Burn-in for social or festival screeners; sidecar for streaming/broadcast; IMSC/TTML via
  IMF deliveries where needed.
- **Forced narratives** (translations of on-screen foreign dialogue only) are often a
  separate deliverable track.

## 4. QC
Play the export with the sidecar in a player (VLC, platform preview), spot-check sync at
start/middle/end; check frame-rate conversions didn't shift timing.

## Gotchas
- SRT timing from a 25 fps project used on a 23.976 deliverable - drift.
- Burned-in subtitles on a master that should be clean (textless master needed separately).
- Auto captions delivered unedited.
- Exceeding line length/reading speed specs; QC rejection.

## Verify
- [ ] Subtitle track per language, named; style set at track level.
- [ ] Captions edited for accuracy and to platform spec.
- [ ] Deliver settings: correct method (burn/sidecar/embedded) and tracks.
- [ ] Exported subtitles checked for sync in a player.
