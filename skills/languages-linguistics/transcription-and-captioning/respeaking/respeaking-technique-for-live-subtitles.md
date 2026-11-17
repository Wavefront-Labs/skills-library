---
id: languages-linguistics.transcription-and-captioning.respeaking.respeaking-technique-for-live-subtitles
name: respeaking-technique-for-live-subtitles
category: languages-linguistics
field: transcription-and-captioning
product: respeaking
tags: [respeaking, voice-writing, live-subtitling, live-captioning, speech-recognition, asr, dragon, dragon-naturallyspeaking, voice-model, voice-training, punctuation-voicing, verbal-punctuation, macros, housestyle, colour-changes, speaker-changes, latency, decalage, ner-model, accuracy-rate, broadcast-subtitling, ofcom, shadowing, stenomask]
level: advanced
status: draft
description: "Live subtitling by respeaking: shadowing technique and décalage, voicing punctuation, speaker-change macros, voice-model training, latency trade-offs and measuring accuracy with the NER model."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Respeaking technique for live subtitles

**Goal:** produce live subtitles by repeating (and lightly editing) speech into speech-
recognition software trained on your voice — fast, accurate and correctly punctuated.

> Draft. Built from broadcast-respeaking practice as generally described (UK/European
> live subtitling, NER accuracy model by Romero-Fresco and Martínez). Software specifics
> (Dragon versions, broadcaster subtitling systems) vary; follow your employer's setup.

## 1. What respeaking is
The respeaker listens to the programme and **re-voices** it to ASR in a flat, clear,
consistent voice, adding punctuation and speaker changes by voice/command, and
condensing when the speech is too fast. The ASR output goes to the subtitling system,
sometimes with a quick correction step.

## 2. Voice and voice model
- Train the ASR profile carefully: initial enrolment, then **add vocabulary** for every
  domain (sports names, politicians, place names) and **train misrecognised words**
  individually.
- Speak in a **steady, even, slightly slower than natural** "respeaking voice" — no
  emotion, consistent volume, clear word boundaries. The model is trained on this voice;
  shifting into your natural chatty voice degrades accuracy.
- Same microphone, same position, every session. Headset or stenomask (a muffled mic
  over the mouth, used where you work in the same room as others).

## 3. Shadowing and décalage
- **Décalage** (lag) = how far behind the original you speak. Too short: you can't
  condense or anticipate sentence ends; too long: you forget content and latency grows.
  Many practitioners work a few words to a clause behind — find your stable lag in
  practice.
- **Chunk by meaning units:** wait for enough to know the clause's shape, then say it
  cleanly.
- **Edit as you go:** drop false starts, fillers and repetitions; compress
  ("what we're going to be doing is" → "we'll"). Keep names, numbers, negatives.
- If you lose the thread, skip to the next sentence — don't try to recover the lost one.

## 4. Punctuation and formatting by voice
- Voice punctuation commands ("comma", "full stop"/"period", "question mark") in the
  same flat tone, without a pause that the engine treats as a word break.
- **Macros** for frequent formatting: speaker change (new line + colour change or
  chevron, per housestyle), `[APPLAUSE]`, common long names.
- Learn the housestyle's colour or label conventions for speakers and stick to them.

## 5. Latency and correction
- Total delay = your décalage + ASR processing + subtitle system. Broadcast live
  subtitles often run several seconds behind; minimise your share.
- Some workflows have a **correction window** (a second person or you checking text
  before release) — trades latency for accuracy.
- For pre-scheduled segments (scripted news), use prepared subtitles instead of
  respeaking where the system allows.

## 6. Measuring accuracy: the NER model
The NER model scores live subtitles as: **(N − E − R) / N × 100**, where N = number of
words in the subtitles, E = edition errors (your editing lost or changed meaning),
R = recognition errors (ASR got it wrong). Errors are weighted by severity (minor,
standard, serious). Commonly cited quality threshold: **98%** NER. Edits that keep
meaning are not errors — condensing is allowed.

## 7. Practice regime
- Daily shadowing of news and talk radio, 20–30 min, recorded and scored.
- Build domain dictionaries before every new programme type.
- Review recognition errors and retrain the specific words.

## Gotchas
- Emotional or emphatic voice when the content is exciting (sports) → recognition drops.
- Homophones the engine can't resolve (their/there, names) — prepare macros.
- Fatigue: shifts are typically limited (e.g. ~15–30-minute stints with breaks; confirm
  local practice).
- Pauses inside phrases splitting words in the engine.

## Verify
- [ ] Score a recorded 10-minute session with NER: ≥98% (or your target).
- [ ] Every speaker change appears with the housestyle marker.
- [ ] Domain vocabulary list added and trained before the session.
- [ ] Average lag behind the original measured and stable.
