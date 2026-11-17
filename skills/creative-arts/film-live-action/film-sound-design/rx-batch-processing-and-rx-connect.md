---
id: creative-arts.film-live-action.film-sound-design.rx-batch-processing-and-rx-connect
name: rx-batch-processing-and-rx-connect
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, dialogue-editing, rx-batch, rx-connect-use, batch-restoration, izotope-rx, rx-connect, batch-processor, module-chain, audiosuite, rx-monitor, dialogue-restoration, pro-tools]
level: practitioner
status: draft
description: "Use iZotope RX efficiently on a show: RX Connect round trips from Pro Tools, Module Chains, and the Batch Processor for consistent restoration across many files without overprocessing."
sources:
  - "https://www.izotope.com/en/products/rx.html (iZotope RX)"
  - "https://docs.izotope.com/rx11/en/ (iZotope RX documentation - RX Connect, Module Chain, Batch Processor)"
  - "https://www.avid.com/pro-tools (Avid Pro Tools - AudioSuite)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RX batch processing and RX Connect

**Goal:** clip-specific restoration done fast in the RX editor without leaving the
dialogue session, and repetitive cleanup done once and applied consistently to many
files.

## 1. RX Connect (clip round trip)
- In Pro Tools, select the clip(s) and open the **RX Connect** AudioSuite plug-in; send
  to the RX standalone editor (handles included by setting AudioSuite handle length).
- Repair in RX with the spectral editor (spectral repair, de-click, de-plosive,
  dialogue isolate) - fix only what needs fixing.
- **Send back**; the processed clip returns as a new file on the same track, in place.
  Keep the original on a muted track below (or as a playlist) for comparison/undo.
- Other hosts: RX Connect works as a plug-in for offline processing in hosts that
  support it; otherwise export, process, reimport by TC.

## 2. Module Chain
- Build a chain in RX (*Module Chain*): e.g. De-hum > Mouth De-click > Voice De-noise
  (adaptive, light). Save it as a preset.
- Use for a known problem shared by many clips (same location hum, same lav).
- Audition on several clips before trusting it.

## 3. Batch Processor
- Add files (e.g. all lavs from one location day), choose a Module Chain or preset,
  set output folder, format (keep sample rate/bit depth), and **file naming suffix**
  (`_rx`).
- Keep metadata: confirm the processed files retain BWF time reference so they
  re-conform/sync.
- Typical uses: hum removal on all files from a location, de-clipping a whole day, ADR
  room-tone noise floor, preparing PFX/ambience recordings.
- Never batch-process originals; output to a new folder.

## 4. Judgement
- Batch only the mechanical fixes (hum, clicks, consistent broadband noise). Dialogue
  noise reduction that changes timbre is done per clip with ears on.
- Keep the processing chain documented in the dialogue notes for the mixer.

## Gotchas
- Batch outputs losing timecode metadata: files no longer conform.
- Short AudioSuite handles: processed clip can't be extended or crossfaded.
- Heavy batch de-noise creating artefacts that only show on a big stage.
- Processed files with the same name as originals, overwriting them.

## Verify
- [ ] Originals preserved; processed files suffixed in a new folder.
- [ ] Timecode and metadata intact (test conform/sync).
- [ ] A/B of processed vs original on several clips before committing.
- [ ] Processing documented for the mix.
