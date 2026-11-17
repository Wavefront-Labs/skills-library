---
id: creative-arts.animation.voice-tts.instant-voice-cloning-from-short-samples
name: instant-voice-cloning-from-short-samples
category: creative-arts
field: animation
product: voice-tts
tags: [instant-voice-clone, voice-cloning, elevenlabs, zero-shot, tts, voice-samples]
level: practitioner
status: draft
description: "Create an instant voice clone from a short sample: pick clean audio, upload, test with a fixed script, know the limits and keep a consent record."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Instant voice cloning from short samples

Instant voice cloning (IVC) builds a usable voice model from a short recording, in seconds rather than hours. It conditions a general model on the sample; it does not train a new model. ElevenLabs offers it in their product; open models such as XTTS-v2 do the same with a reference clip (`coqui-xtts-v2-local-generation.md`).

## Steps
1. **Consent**: confirm and record permission from the speaker (`consent-and-rights-for-voice-cloning.md`).
2. **Choose the sample**: roughly one to a few minutes of clean, single-speaker speech in the delivery style you want. Check the provider's current guidance; recommended lengths and upload limits change.
3. **Clean the audio**: remove other voices, music, long silences, clicks and breaths that are not part of the style. Do not over-process: heavy denoise artefacts are cloned too.
4. **Upload** in the provider's voice creation page or API, name the voice with the character, and save the returned `voice_id`.
5. **Test** with a fixed test script (a short and a long sentence, a question, a number, a name, an emotional line). Compare to the source speaker.
6. **Record** the sample file, voice ID, model ID and settings in the voice bible.

## Limits
- The clone follows the style of the sample: a flat sample gives flat reads, a shouted sample is hard to turn gentle.
- Accents and unusual voices may drift. Quality is below a professional clone on long form (`professional-voice-cloning-from-long-datasets.md`).
- Quality can change when the provider updates models.

## Verify
- [ ] Consent on file before upload.
- [ ] Fixed test script output reviewed by ear.
- [ ] Voice ID, model and settings saved.
