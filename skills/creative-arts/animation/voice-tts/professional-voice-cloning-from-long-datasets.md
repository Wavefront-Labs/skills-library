---
id: creative-arts.animation.voice-tts.professional-voice-cloning-from-long-datasets
name: professional-voice-cloning-from-long-datasets
category: creative-arts
field: animation
product: voice-tts
tags: [professional-voice-clone, voice-cloning, elevenlabs, fine-tuned-voice, voice-dataset, verification]
level: advanced
status: draft
description: "Plan a professional voice clone trained on a long dataset: sourcing the recordings, verification, training time, quality testing, when it beats instant cloning."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Professional voice cloning from long datasets

Professional voice cloning (PVC) fine-tunes a model on a substantial recording set of one speaker. Providers (ElevenLabs is the best-known case) typically require a higher subscription tier and a **verification step** proving the voice's owner is the person submitting it. Consult the current docs for tier, duration guidance and supported languages; recommended amounts have been on the order of tens of minutes to a few hours of clean speech.

## When to choose it over instant cloning
- A hero or narrator voice used for hours of output where subtle timbre and pacing consistency matters.
- The actor is available to record a studio-quality dataset.
- You need stable results across many generations and episodes.

## Dataset
Follow `preparing-a-voice-dataset.md`. Particular points:
- One consistent mic, room, preamp and distance; one session style per desired delivery (neutral, excited).
- Vary sentence length and content, with numbers and names.
- No processing beyond gentle clean-up. Provide uncompressed audio where the provider accepts it.

## Process
1. Written consent and licence terms agreed with the actor, including AI-use scope and compensation (see `consent-and-rights-for-voice-cloning.md`).
2. Record, clean, and upload the dataset; complete the provider's verification.
3. Wait for training (can take from minutes to hours or more depending on the provider and queue).
4. Test with the fixed script, hard cases and long passages; compare against held-out real recordings.
5. Lock the voice (`voice-casting-consistency.md`) and store IDs and settings.

## Gotchas
- A clone cannot fix a noisy dataset.
- Language support for the professional tier may differ from the instant tier.
- Provider policy changes can affect access to a clone; keep the source dataset archived.

## Verify
- [ ] Dataset reviewed for noise, consistency and transcripts before upload.
- [ ] Verification and consent complete.
- [ ] Blind A/B by ear against real recordings has passed with the director.
