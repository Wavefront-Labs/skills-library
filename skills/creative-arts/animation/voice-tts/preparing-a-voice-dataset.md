---
id: creative-arts.animation.voice-tts.preparing-a-voice-dataset
name: preparing-a-voice-dataset
category: creative-arts
field: animation
product: voice-tts
tags: [voice-dataset, dataset-preparation, voice-cloning, tts-training, transcription, audio-cleanup]
level: practitioner
status: draft
description: "Prepare a clean speech dataset for voice cloning or TTS training: recording spec, segmenting, transcripts, normalisation, filtering and a manifest."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Preparing a voice dataset

The quality ceiling of any cloned or trained voice is the dataset. The same preparation serves cloning services and local trainers such as Piper (`training-a-custom-piper-voice.md`).

## Recording spec
- One speaker, one mic, one room, one distance; 24-bit WAV at 44.1 or 48 kHz as the master, converted later to what the trainer needs (often 22.05 kHz mono for Piper).
- Treated room or booth (`booth-and-room-treatment.md`); peaks around -12 to -6 dBFS.
- Scripts that cover the language's sounds, include numbers, names, questions and the styles the voice will use.

## Segmenting
- Cut into utterances of roughly 2-12 seconds at sentence or phrase boundaries, with short silence (about 0.1-0.3 s) at each end; avoid cutting inside a word or leaving a breath cut in half.
- Name files with a stable ID: `spk01_0001.wav`.

## Transcripts
- Each file gets an exact text transcript, written as spoken (expand numbers, abbreviations as the speaker said them).
- Automatic transcription (a speech-to-text tool) speeds this up but must be proofread; wrong text is a common cause of garbled output.

## Clean-up and checks
- Loudness-normalise consistently (for example to the same integrated level per file) rather than peak-normalising wildly different clips.
- Remove clips with clipping, background noise, other voices, mouth noises that do not belong, or reading mistakes.
- Do not apply noise reduction or heavy compression unless the same chain will be used at delivery. Artefacts will be learned.
- Check duration totals per style and keep a balanced mix.

## Manifest
A CSV or pipe-separated file: `file|text|speaker|duration|style`. Keep a README with recording date, mic chain, consent reference and licence terms.

## Verify
- [ ] Every clip has a verified transcript.
- [ ] Clips audited for noise and clipping; outliers removed.
- [ ] Manifest and consent reference stored with the dataset.
