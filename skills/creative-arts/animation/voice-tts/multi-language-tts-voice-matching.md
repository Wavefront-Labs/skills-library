---
id: creative-arts.animation.voice-tts.multi-language-tts-voice-matching
name: multi-language-tts-voice-matching
category: creative-arts
field: animation
product: voice-tts
tags: [multi-language-tts, multilingual, voice-matching, tts, accent, localisation, voice-casting]
level: practitioner
status: draft
description: "Keep one character sounding like themselves in several languages with multilingual TTS: model choice, per-language testing, accent drift and native review."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Multi-language TTS voice matching

Some TTS models (for example ElevenLabs' multilingual models and the open XTTS-v2) can speak many languages in one voice. The aim is to make a character recognisable across languages, not identical.

## Steps
1. Pick a **multilingual-capable model**; some models are English-only or support fewer languages. Check the documentation's language list.
2. Use the same voice ID or reference clip across languages, with settings from the voice bible (`voice-casting-consistency.md`).
3. Generate the same test script in each language; compare pitch, pace and warmth with the English version.
4. Expect **accent carry-over**: a voice cloned from English speech may speak other languages with a slight English accent. Decide whether that suits the character, or pick a native-language voice with similar timbre for important languages.
5. Have a **native speaker review** pronunciation, stress and naturalness; they will catch errors a non-speaker will not.
6. Add per-language entries to the pronunciation dictionary for names and terms (`pronunciation-dictionaries-and-lexicons.md`).
7. Record language-specific settings; stability and speed often need different values per language.

## Gotchas
- Script text must be in the right language and script (Unicode); mixed-language text can confuse language detection. Set the language code explicitly where the engine allows it.
- Punctuation conventions differ by language and affect pauses.
- A voice sample that sounds young in English may sound different in another language.

## Verify
- [ ] Same test script rendered in every target language.
- [ ] Native reviewer signed off each language.
- [ ] Per-language settings stored.
