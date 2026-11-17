---
id: creative-arts.animation.voice-tts.speech-to-speech-performance-transfer
name: speech-to-speech-performance-transfer
category: creative-arts
field: animation
product: voice-tts
tags: [speech-to-speech, voice-conversion, performance-transfer, tts-control, elevenlabs, acting]
level: practitioner
status: draft
description: "Transfer a human performance to a character voice with speech-to-speech: recording the guide read, timing preservation, settings, cleaning input and limits."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Speech-to-speech performance transfer

Speech-to-speech (also called voice conversion or voice changing) takes an existing recording and re-renders it in a different voice while keeping timing, pitch movement and emotion. It is the way to get **directed acting** out of a synthetic voice, since text-to-speech alone guesses the delivery.

## Where it fits
- A writer, director or actor records the line with the intended performance. The tool converts it into the character's voice.
- ElevenLabs offers a speech-to-speech endpoint with dedicated models, and open-source voice-conversion tools exist for local use. Check the current docs for supported models and limits.

## Steps
1. Record the guide read: clean, dry, close-mic, at the speed and emotion wanted. The output follows it closely, including mistakes and mouth noise.
2. Remove noise and clicks beforehand if you can without audible artefacts (`dialogue-denoise.md`).
3. Submit with the target voice and the settings. Lower stability tends to preserve more of the guide's variation; check the provider's notes.
4. Generate several versions; choose by ear.
5. Check lip-sync timing against the guide: the transfer usually keeps timing, which makes it easy to use the guide as the lip-sync reference (`lip-sync-review-and-offset-correction.md`).

## Limits
- The guide read must be intelligible and well-paced; pronunciation errors are carried over.
- Pitch range of source and target should be compatible; large mismatches (for example a deep adult guide to a child voice) can sound strained.
- Consent still applies to both the guide performer and the target voice (`consent-and-rights-for-voice-cloning.md`).

## Verify
- [ ] Guide read is clean and performs the intended emotion.
- [ ] Output compared with guide for timing.
- [ ] Consent for both voices recorded.
