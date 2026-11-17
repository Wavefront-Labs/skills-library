---
id: creative-arts.animation.voice-tts.forced-alignment-of-transcript-to-audio
name: forced-alignment-of-transcript-to-audio
category: creative-arts
field: animation
product: voice-tts
tags: [forced-alignment, montreal-forced-aligner, textgrid, phoneme-timing, lip-sync, rhubarb]
level: advanced
status: draft
description: "Align a transcript to dialogue audio to get word and phoneme timings: Montreal Forced Aligner workflow, corpus layout, TextGrid output and conversion to lip-sync cues."
sources:
  - https://montreal-forced-aligner.readthedocs.io/
  - https://github.com/DanielSWolf/rhubarb-lip-sync
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Forced alignment of transcript to audio

Forced alignment takes audio and its known transcript and finds when each word and phoneme occurs. It gives much more accurate timing than guessing from the waveform and is the basis for automatic lip-sync.

## Tools
- **Montreal Forced Aligner (MFA)**: a Kaldi-based command-line aligner with pretrained acoustic models and pronunciation dictionaries for many languages. Output is a Praat **TextGrid** with word and phone tiers.
- **Rhubarb Lip Sync**: aligns (optionally with `--dialogFile` text) and outputs mouth-shape cues directly (`setup-windows.md`).
- Others exist (for example the aeneas Python library for text-to-audio sync at sentence level); choose by precision needed.

## MFA workflow (check the current docs for exact commands)
1. Install MFA in its own environment (the documentation recommends conda).
2. Download an acoustic model and dictionary: `mfa model download acoustic english_us_arpa` and `mfa model download dictionary english_us_arpa`.
3. Make a corpus folder: for each `line.wav`, a `line.lab` (or `.txt`) file with the transcript of the same name. Group per-speaker in subfolders if you have several speakers.
4. Run: `mfa align <corpus_dir> english_us_arpa english_us_arpa <output_dir>`.
5. Read the TextGrids in `<output_dir>`; each interval has start/end seconds and a label.
6. Out-of-vocabulary words (invented names) are reported; add them to a custom dictionary with an ARPAbet-style pronunciation, then re-run.

## Convert to animation timing
- Map the phones (ARPAbet in the English models) to your viseme set (`mouth-chart-and-viseme-set-design.md`), merge neighbouring identical visemes and drop shapes shorter than about 2 frames at 24 fps.
- Convert seconds to frames with the project frame rate: `frame = round(seconds * fps)`.
- Output an exposure sheet or keyframe list (`reading-dialogue-onto-an-exposure-sheet.md`).

## Gotchas
- Transcripts must match what was said, including false starts; wrong text gives bad alignment.
- Noisy audio or music under dialogue degrades alignment; use the dialogue stem.
- TTS audio aligns well; shouted or whispered audio less so.
- The model's dictionary decides phone labels; mixed accents may mis-align without a custom dictionary.

## Verify
- [ ] Spot-check word boundaries on a few lines in an audio editor.
- [ ] Unknown words reviewed and added.
- [ ] Frame conversion uses the project frame rate.
