---
id: creative-arts.film-live-action.premiere-pro.export-xml-aaf-media-encoder-and-publishing
name: export-xml-aaf-media-encoder-and-publishing
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, xml-export-premiere, aaf-export-premiere, omf-export, encoder-queue, watch-folders, encoder-presets, direct-publish, publish-to-youtube, publish-settings, media-encoder]
level: practitioner
status: draft
description: "Get work out of Premiere Pro: AAF/OMF to Pro Tools, XML to Resolve, Media Encoder queues, presets and watch folders, and direct publishing to platforms from the Export workspace."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/exporting-aaf-files.html (Adobe - Exporting AAF)"
  - "https://helpx.adobe.com/media-encoder/using/overview-media-encoder-user-interface.html (Adobe Media Encoder - queue, presets, watch folders)"
  - "https://helpx.adobe.com/premiere-pro/using/export-workflow.html (Adobe - Export mode and publishing destinations)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Export: XML, AAF, Media Encoder and publishing

**Goal:** every handoff and deliverable leaves Premiere in the format the receiver
expects - and long renders run in the background.

## 1. AAF / OMF to sound (Pro Tools)
*File > Export > AAF*:
- **Mixdown video** off (send a separate reference movie); **Embed audio** or separate
  (embedded is simpler for small projects; large ones use separate WAVs), **handles**
  (e.g. 120-240 frames), sample rate 48 kHz 24-bit, **Breakout to mono**.
- Prepare first: duplicate the sequence, remove disabled/muted clips you don't want,
  flatten nests and multicam, put dialogue, FX and music on consistent tracks.
- **OMF** (*File > Export > OMF*) for older workflows - 2 GB file limit; prefer AAF.
- Send a reference QuickTime with timecode burn-in and 2-pop/ head leader.

## 2. XML to Resolve / other NLEs
*File > Export > Final Cut Pro XML*: carries cuts, basic transitions, speed changes,
transforms (partially). Flatten nests/multicam, remove effects Resolve won't read, and
supply a reference movie for the conform check.

## 3. Media Encoder
- *Export* window > **Send to Media Encoder** (or `Ctrl/Cmd+Alt+M` in some versions) to
  queue instead of rendering in Premiere - keeps editing while it encodes.
- **Presets**: create and save custom presets (codec, bitrate, audio, LUTs, captions)
  in the Preset Browser; group them (e.g. "Client deliverables") and apply several to one
  source at once.
- **Watch folders**: point a folder at presets - anything dropped in is encoded
  automatically (dailies, social versions).
- Queue control: start/pause, parallel encoding option; check the encoding log for errors.

## 4. Direct publish
In **Export mode** (Premiere 22+), add destinations: **Media File** plus publishing to
YouTube, Vimeo, Facebook, X, TikTok, Behance etc. after signing in; set title/
description/ privacy per destination; the file renders once and uploads. For
client-critical uploads verify the uploaded file plays and looks right on the platform.

## Gotchas
- AAF without handles - dialogue editors can't extend.
- Nested/multicam sequences exported to XML/AAF - clips missing.
- Media Encoder presets with mismatched frame rate - stutter.
- Public publishing setting left on a client draft.

## Verify
- [ ] AAF exported from a prepared, flattened duplicate with handles and a reference movie.
- [ ] XML tested in the receiving app against the reference.
- [ ] Encoder presets saved and named; queue logs checked.
- [ ] Publish destinations' privacy and metadata set; uploads verified.
