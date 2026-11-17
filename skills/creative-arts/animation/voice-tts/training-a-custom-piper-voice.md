---
id: creative-arts.animation.voice-tts.training-a-custom-piper-voice
name: training-a-custom-piper-voice
category: creative-arts
field: animation
product: voice-tts
tags: [piper-training, piper, tts-engines, vits, fine-tuning, voice-dataset, onnx]
level: advanced
status: draft
description: "Plan a custom Piper voice: dataset requirements, fine-tuning from a checkpoint versus scratch, preprocessing, training checks, ONNX export and testing before use."
sources:
  - https://github.com/OHF-Voice/piper1-gpl
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Training a custom Piper voice

Piper is a fast local neural TTS (VITS-based, exported to ONNX). Training your own voice is feasible on a single consumer GPU, but the exact commands depend on the repository version, so follow the training document in the version you install. The older rhasspy/piper repository and the newer OHF-Voice/piper1-gpl repository have different training entry points; do not mix instructions between them.

## Plan
1. **Rights and consent first**: only train on a voice you have written permission to use (see `consent-and-rights-for-voice-cloning.md`).
2. **Dataset**: clean recordings of one speaker in one consistent mic and room, with exact transcripts. Prepare it as described in `preparing-a-voice-dataset.md`. A common layout is a folder of WAV files plus a pipe-separated metadata file (`id|text`), as in the LJSpeech format.
3. **Fine-tune versus scratch**: fine-tuning an existing high-quality checkpoint of a similar language needs much less data and time than training from scratch, and is the realistic route for a small cast. The community rule of thumb is that fine-tuning can work with well under an hour of clean speech while scratch training wants many hours; treat these as rough guidance, not guarantees.
4. **Sample rate**: match the checkpoint (Piper "medium" voices commonly use 22.05 kHz; check the voice's `.onnx.json`).

## Training outline
- Run the repo's preprocessing step to produce phoneme IDs and a config JSON for your dataset (it uses espeak-ng phonemisation for most languages, so install espeak-ng).
- Start training from the base checkpoint, watching loss curves and saved samples. Stop when sample quality plateaus; more steps can over-fit a small dataset.
- Export the chosen checkpoint to ONNX and ship it with its `.onnx.json` config; Piper needs both files.

## Test
- Synthesise a fixed test sentence list, including numbers, names, questions, and long sentences.
- Listen for robotic buzz, dropped words, skipped endings, and wrong stress.
- Compare against the real speaker's recordings for timbre match.

## Gotchas
- Any noise or mouth click in the dataset tends to be reproduced.
- Mismatch between transcript and audio causes babble. Verify transcripts.
- A trained voice is deterministic but only as good as its dataset; fix the data before training more.

## Verify
- [ ] Written consent and licence recorded.
- [ ] Dataset passes listening and transcript spot checks.
- [ ] Exported `.onnx` and `.onnx.json` load in the Piper CLI and render the test list.
