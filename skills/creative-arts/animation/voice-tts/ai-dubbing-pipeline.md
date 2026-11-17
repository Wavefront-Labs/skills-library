---
id: creative-arts.animation.voice-tts.ai-dubbing-pipeline
name: ai-dubbing-pipeline
category: creative-arts
field: animation
product: voice-tts
tags: [ai-dubbing, dubbing, elevenlabs, localisation, speaker-detection, voice-cloning, translation]
level: advanced
status: draft
description: "Run an AI-assisted dubbing pipeline: source audio prep, transcription and translation review, per-speaker voices, timing checks, human QC and consent records."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AI dubbing pipeline

AI dubbing tools (for example ElevenLabs Dubbing) transcribe the source, translate, and generate speech in the target language in cloned or selected voices. Quality depends on prep and human review. Check the provider documentation for current features, languages and limits.

## Pipeline
1. **Prepare source**: use the cleanest dialogue available, ideally the dialogue stem without music and effects. Separate the M&E track (`m-and-e-mix.md`) so the dub is mixed over the original M&E.
2. **Transcribe**: let the tool transcribe, then proofread it against the script. Fix names and invented words before translating.
3. **Speakers**: set the number of speakers if the tool allows it and check that detection assigned each line to the right character.
4. **Translate**: review the translation with a native speaker (`dub-script-adaptation-and-lip-sync-fit.md`).
5. **Voices**: choose per-character voices; cloning the original actor's voice into another language needs the actor's consent (`consent-and-rights-for-voice-cloning.md`).
6. **Timing**: check duration fit per line (`isochrony-and-timing-fit-of-translated-lines.md`) and edit text or settings.
7. **Export**: export dialogue stems separately per language, not a flattened video.
8. **Mix and QC**: mix with M&E to the platform loudness spec (`dialogue-gated-loudness-for-streaming.md`), then a native-speaker QC pass against picture.

## Gotchas
- AI voices sound more uniform than actors; emotional scenes usually need speech-to-speech or human actors (`speech-to-speech-performance-transfer.md`).
- Errors in names, jokes and slang are common; keep a glossary.
- Disclose AI use where contracts or platform rules require it.

## Verify
- [ ] Source transcript matches the script.
- [ ] Native reviewer approved translation and audio.
- [ ] Per-language stems and consent records archived.
