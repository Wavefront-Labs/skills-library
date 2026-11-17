---
id: creative-arts.film-live-action.premiere-pro.transcript-export-and-paper-edits
name: transcript-export-and-paper-edits
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, transcript-export, transcript-docx, paper-edit-from-transcript, text-based-editing, speech-to-text, paper-edit, srt-export, documentary-editing, selects, interview-transcripts, prtranscript]
level: practitioner
status: draft
description: "Export Premiere Pro transcripts for documentary paper edits: text and caption exports, timecoded Word documents for producers, and turning marked-up selects back into a sequence."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/text-based-editing.html (Adobe - Text-Based Editing)"
  - "https://helpx.adobe.com/premiere-pro/using/speech-to-text.html (Adobe - Speech to Text, export transcript)"
  - "https://helpx.adobe.com/premiere-pro/using/working-with-captions.html (Adobe - Captions export)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transcript export and paper edits from Premiere Pro

**Goal:** interview transcripts the director and producer can mark up away from the
edit bay, and a fast route from their marked selects back to clips on a timeline.

## 1. Transcribe properly first
- Transcribe source clips (*Text panel > Transcript > Transcribe*), not sequences, so
  every transcript stays with its master clip.
- Set the language and **speaker labelling**, then rename "Speaker 1" to real names
  before export; renaming after export means fixing every document.
- Fix proper nouns in the transcript (edit text directly) on key interviews.

## 2. Export options
- *Transcript panel > ... menu > Export to text file* gives plain `.txt` with speakers
  (and timecode if enabled in the export options of your version).
- *Export transcript* writes a `.prtranscript` for another Premiere project, not for people.
- For guaranteed source timecodes, create captions from the clip transcript and
  *Export to SRT*: every line carries in/out times.
- Convert to a **Word document**: open the txt/SRT in Word, set a monospaced or table
  layout (timecode | speaker | text), add a header with clip name, tape/card name and
  date. Name it after the master clip so it maps back.

## 3. The paper edit
- Producers highlight selects, number them in story order, and write bridging notes;
  colour code by theme or character.
- Return a single document (or spreadsheet: order, clip name, TC in, TC out, line).
- Combine with the documentary structure work (paper edit, radio cut) in the
  documentary editing skill.

## 4. Back to the timeline
- Open the clip's transcript, find the line (search in the Text panel), select the text
  and **Insert** or **Overwrite** into the sequence - Premiere cuts the matching media.
- Or set In/Out from the TC on the paper edit and three-point edit.
- Build the radio cut in paper-edit order first, then refine.

## Gotchas
- Transcripts made on a sequence point to sequence time, not source TC.
- Clips with timecode reset per card (all starting 00:00:00:00) need clip names in the
  document, or selects are ambiguous.
- Auto transcripts mishear names and numbers; never quote them in titles or publicity
  without checking audio.
- Interview subjects' transcripts are sensitive; share via access-controlled links.

## Verify
- [ ] Every exported transcript names its master clip and speakers.
- [ ] Timecodes in the document match the source monitor.
- [ ] Ten random selects found and cut from the paper edit without guessing.
