---
id: creative-arts.film-live-action.premiere-pro.text-based-editing-and-transcripts
name: text-based-editing-and-transcripts
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, film-live-action, text-based-editing, transcript, transcribe, transcription, speech-to-text, auto-captions, captions, caption-track, caption-styles, srt, scc, subtitles, burn-in-captions, sidecar-captions, filler-words, pauses, delete-pauses, speaker-labels, text-panel, rough-cut-from-transcript, interview-editing, documentary-editing, paper-edit, search-transcript, multicam-transcript, language-models, offline-transcription, caption-export, 708, 608, teletext, transcribe-settings, speaker-labelling, text-rough-cut, transcript-to-timeline, filler-word-removal, pause-detection, transcript-search-use, sequence-transcript, captions-from-transcript, caption-editing-premiere, caption-track-use, caption-export-use, embedded-captions, burn-in-export, caption-styling, caption-style-presets]
level: practitioner
status: draft
description: "Cut from words in Premiere Pro: transcribe clips and sequences, build a rough cut from transcript text, strip pauses and filler words, label speakers, then generate, style and export captions."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/text-based-editing.html (Adobe - Text-Based Editing)"
  - "https://helpx.adobe.com/premiere-pro/using/speech-to-text.html (Adobe - Speech to Text and captions)"
  - "https://certifiedprofessional.adobe.com/ (Adobe Certified Professional - Premiere Pro exam objectives)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text-based editing and transcripts in Premiere Pro

**Goal:** an interview-driven assembly built in hours instead of days, and captions
that pass delivery QC - all from one transcript.

## 1. Transcribe
`Window > Text` > **Transcript** tab.
- **Clips**: in the Project panel select clips > right-click > *Transcribe*; or enable
  `Preferences > Transcription > Auto-transcribe on import` for interview-heavy shows
  (language auto-detect or set; *Speaker labelling* on; choose the audio track/channel
  with the clean mic - the mix track, not the boom and lav both).
- **Sequences**: Text panel > *Transcribe sequence* (uses the sequence's audio; choose
  *Mix* or a specific track; *Transcribe clips in all sequence tracks*).
- Transcription runs locally (language packs download once); speed ~real time or faster.
- Edit the text: double-click a word to fix spelling (improves captions; doesn't move
  edits); right-click a speaker > *Edit Speakers* to name them; `Ctrl/Cmd+F` search
  the whole transcript, including across all project clips in the *Project* transcript view.

## 2. Build a rough cut from text
Text panel (Transcript tab) with a **source clip** open:
1. Select words/sentences in the transcript (click-drag, or `Shift`-click to extend).
2. **Insert** (`,`) or **Overwrite** (`.`) buttons in the panel (or `Ctrl/Cmd+Enter`)
   places that range on the active sequence at the playhead with the sequence's
   source patching rules.
3. Repeat across clips; the sequence transcript (**Sequence** tab) now reads as a paper
   edit - rearrange by cutting/pasting text? No: reorder by dragging the text selection
   in the sequence transcript (`Ctrl/Cmd+X`/`V` on selected sequence text moves the
   corresponding clips).
4. Delete a sentence in the sequence transcript (`Delete`) to ripple-delete it from the
   timeline; `Ctrl/Cmd+Z` undoes both.
- **Pause detection**: the panel's "..." / pause markers; *Delete all pauses* (set
  minimum pause length in the panel settings, e.g. 1.0 s) ripples them out - review
  afterwards; breaths and reactions can matter.
- **Filler words**: Text panel > *Filler Words* (highlights "um", "uh", "like" - 2024+)
  > select all > delete. Keep a few for naturalness in docs.
- Markers from text: select text > *Add Marker* to flag for b-roll.
Works with **multicam source sequences** too (transcribe the multicam sequence; edits
respect angles).

## 3. Captions from the transcript
Text panel > **Captions** tab > *Create captions from transcript*:
- Format: **Subtitle** (open captions / SRT style), **CEA-608**, **CEA-708**, **Teletext**,
  **EBU Subtitle**, *Australian OP-47* - choose what the deliverable demands (broadcast
  often 708/608; streaming SRT/WebVTT/IMSC; social burn-in).
- *Maximum characters per line* (32 for 608; ~42 for subtitles), *Minimum duration*
  (~1 s), *Gap between captions*, *Lines: single/double*, *Split on sentence end*.
- A **caption track** appears in the timeline; edit text, split (`Ctrl/Cmd+Shift+K`...
  use the panel's *Split* and *Merge*), retime by trimming caption clips, align to cuts.
- **Style**: Essential Graphics panel with a caption selected (font, size, fill,
  background, position); save as a *Caption Style* (Track Style) and apply to the track;
  for 608/708 the style is limited by the standard.
- Multiple caption tracks for languages: *Add caption track* and *Translate*
  (Premiere 2025+ can machine-translate; always have a human review).

## 4. Export captions
Export panel > **Captions** > *Export Options*: **Create Sidecar File** (`.srt`, `.scc`,
`.mcc`, `.xml` IMSC/TTML, `.stl`, `.vtt`), **Embed in output file** (608/708 in MXF/
QuickTime), or **Burn captions into video** (open captions). Burn-in uses the Essential
Graphics styling; check safe margins. Export audio-less captions-only via *File >
Export > Captions* when the picture isn't changing.

## 5. Accuracy and privacy
Auto transcription is ~90-97% on clean English; names, jargon and accents need a pass.
For legal/broadcast captions a human QC is mandatory. Transcripts live in the project
file (`.prproj`), so sensitive interviews stay offline with the project; disable
Sensei cloud features if policy requires (transcription is on-device by default).

## Gotchas
- Transcribing the boom + lav mixed stereo pair; words doubled or garbled - pick one channel.
- Deleting all pauses on a scene with reaction shots; the rhythm dies.
- Captions created before picture lock; every trim requires re-timing them - generate after lock, or regenerate.
- 608 captions with 42-character lines; rejected at QC.
- Translation exported without review; names and idioms wrong on air.

## Verify
- [ ] Transcript from the clean dialogue channel; speakers named; obvious misrecognitions fixed.
- [ ] Rough cut built from transcript selections; pauses/fillers removed selectively.
- [ ] Captions generated after lock in the required format and line length; styled with a saved track style.
- [ ] Sidecar/embedded/burn-in chosen per deliverable; human QC of caption text.
