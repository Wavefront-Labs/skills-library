---
id: creative-arts.animation.editorial.aaf-audio-turnover
name: aaf-audio-turnover
category: creative-arts
field: animation
product: editorial
tags: [aaf-audio-turnover, editorial-sound, audio-turnover, aaf, omf, handles, embedded-media, pro-tools, reference-video, sound-post]
level: advanced
status: draft
description: "Turn audio over from picture editorial to sound post: AAF with handles and embedded or linked media, reference video with timecode, EDLs and the checks that prevent re-turnovers."
sources:
  - https://www.avid.com/learn-and-support
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://helpx.adobe.com/premiere-pro/using/exporting-aaf-files.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AAF audio turnover

**Goal:** sound post opens the edit's audio in Pro Tools (or Nuendo/Fairlight) with every clip in place, with
handles to extend edits, in sync with a reference picture.

## The package

| Item | Spec |
|---|---|
| AAF | audio tracks only, handles 3-10 s (sound teams commonly ask for 5-10 s), media embedded or copied/consolidated, 48 kHz 24-bit |
| Reference video | ProRes Proxy/DNxHR LB or H.264, burned-in timecode, 2-pop and head leader, same start TC as the timeline |
| Guide track | the editor's mix as stereo WAV, for comparison |
| EDL | per track (optional), for conform checks |
| Notes | track layout, temp material flags, known issues |

## Export settings

- **Avid**: File - Export - AAF, "Export method: Consolidate media" with handles, audio format WAV.
- **Premiere**: File - Export - AAF: "Mixdown video" off, "Breakout to mono" on for mono dialogue, "Embed audio"
  or "Separate audio" with handles.
- **Resolve**: File - Export AAF/XML - "Export AAF for Pro Tools" style options, or via Fairlight: deliver
  media and AAF with handles.
OMF is legacy (2 GB limit, no volume automation in older versions); use AAF.

## Sync checks

- Head leader with a 2-pop at exactly 2 s before first frame of action, on the picture and every audio export.
- Sound post lines up the pop on import; any offset reveals a problem immediately.

## Gotchas

- Clips with speed changes, nested sequences or effects may export as rendered or missing; flatten/render
  them or note them.
- Multichannel clips linked as one may export as polyphonic in odd ways; test early with sound post.
- Re-turnover after recuts: send a change list (`creative-arts.animation.editorial.editorial-change-lists`) and a
  new AAF; sound uses conform tools to update their session.

## Verify

Sound post confirms: pops line up, all tracks and clips present with handles (extend a clip and hear more
audio), and the guide mix matches their import when played together (phase-cancel test).
