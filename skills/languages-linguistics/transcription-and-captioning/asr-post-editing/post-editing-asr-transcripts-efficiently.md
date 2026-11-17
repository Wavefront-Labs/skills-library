---
id: languages-linguistics.transcription-and-captioning.asr-post-editing.post-editing-asr-transcripts-efficiently
name: post-editing-asr-transcripts-efficiently
category: languages-linguistics
field: transcription-and-captioning
product: asr-post-editing
tags: [asr-post-editing, asr, automatic-speech-recognition, speech-to-text, post-editing, whisper, otter, rev, descript, trint, auto-captions, youtube-auto-captions, word-error-rate, wer, hallucinations, diarization, speaker-diarization, custom-vocabulary, timestamps, confidence-scores, proper-nouns, homophones, transcript-qa, caption-editing]
level: practitioner
status: draft
description: "Correct ASR transcripts and auto-captions fast: the error patterns to hunt (names, numbers, negations, hallucinations, diarization), a two-pass workflow, and QA against the audio."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-editing ASR transcripts efficiently

**Goal:** turn machine speech-recognition output (Whisper, platform auto-captions,
commercial transcription services) into a transcript or caption file you can stand
behind — in far less time than transcribing from scratch, without inheriting the
machine's silent errors.

> Draft. Error patterns are typical of current ASR systems as widely observed; any given
> engine's strengths differ. Speed ratios are rough.

## 1. Decide whether post-editing beats re-transcribing
Skim 2 minutes of the output against the audio. If you're fixing more than roughly one
word in five (heavy accents, crosstalk, poor audio, unusual language), starting from
scratch or re-running ASR with better settings may be faster. Clean audio with
mainstream accents often needs light editing.

## 2. Improve the input before editing
- Give the engine **custom vocabulary / prompt** where supported (names, jargon) — e.g.
  Whisper's initial prompt, service "custom vocabulary" lists.
- Choose the right **language** explicitly (auto-detect can pick wrong on short or
  mixed audio).
- Separate channels per speaker if recorded that way; better diarization.
- Light denoise/normalise on a copy if the audio is poor.

## 3. Know the error patterns (where to look hardest)
1. **Proper nouns and jargon:** names, companies, drugs, places → phonetically similar
   common words ("Kubernetes" → "communities").
2. **Numbers, dates, money, units:** misheard digits; inconsistent formatting ("15" vs
   "fifty").
3. **Negations and small function words:** "can"/"can't", "isn't"/"is" — tiny audio
   difference, huge meaning change.
4. **Homophones:** their/there, to/two, wait/weight.
5. **Hallucinations:** text that isn't in the audio — repeated phrases, invented sentences
   during silence or music, "thanks for watching" at the end. Common in some generative
   ASR models on non-speech segments.
6. **Omissions:** dropped words in fast or overlapping speech; whole quiet passages
   missing.
7. **Diarization errors:** speaker labels swapped or merged, especially on short
   interjections and similar voices.
8. **Punctuation and segmentation:** run-on sentences, wrong sentence boundaries that
   change meaning.

## 4. A two-pass workflow
**Pass 1 — listen and fix (at 1.0–1.5× speed):** play audio with the text highlighted in
sync (most editors do this); pause and correct content errors as they go by. Use
**confidence highlighting** if the tool provides it — low-confidence words first.
**Pass 2 — read and format (no audio, except for doubts):** speaker labels, punctuation,
paragraphing, style (verbatim level, tags — see the verbatim-transcription skill),
consistent spellings.
Then **targeted checks** (section 5).

## 5. Targeted search-and-check
- Search the transcript for every name and term in your glossary; check variants
  (`Smyth|Smith`).
- Find all numbers (regex `\d`) and check each against audio.
- Search for negations (`n't`, `not`, `never`, `no`) in key passages and verify.
- Scan for repeated lines or sentences — hallucination signature.
- Check silences/music sections for invented text.
- For captions: re-run reading-rate and line-length checks after edits (see subtitling).

## 6. Timing
Editing text can break caption timestamps. Use an editor that keeps word-level timing
(Descript, Subtitle Edit with waveform, platform caption editors), or re-sync/forced-
align after editing.

## Gotchas
- Trusting fluent output: ASR errors read naturally, unlike typos.
- Editing without audio — you'll "fix" grammar the speaker actually used.
- Auto-captions published as accessibility captions without editing (no sound tags,
  wrong names).
- Uploading confidential audio to a cloud service without permission.

## Verify
- [ ] Every glossary term and name appears spelled correctly.
- [ ] Every number checked against audio.
- [ ] No repeated hallucinated lines; silence sections are empty or tagged.
- [ ] Random 2-minute spot-check against audio: zero meaning-changing errors.
- [ ] Data-handling rules for the audio were followed.
