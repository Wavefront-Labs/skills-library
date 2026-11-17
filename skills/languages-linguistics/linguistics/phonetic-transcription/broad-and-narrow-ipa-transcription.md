---
id: languages-linguistics.linguistics.phonetic-transcription.broad-and-narrow-ipa-transcription
name: broad-and-narrow-ipa-transcription
category: languages-linguistics
field: linguistics
product: phonetic-transcription
tags: [phonetic-transcription, phonetics, ipa, international-phonetic-alphabet, broad-transcription, narrow-transcription, phonemic-transcription, diacritics, place-of-articulation, manner-of-articulation, voicing, vowel-chart, cardinal-vowels, ear-training, slashes-vs-brackets, unicode-ipa, x-sampa, aspiration, allophones, speech-sounds]
level: practitioner
status: draft
description: "Transcribe speech in the IPA: slashes vs brackets, describing consonants and vowels articulatorily, choosing diacritics for narrow transcription, ear-training drills, and typing IPA reliably."
sources: ["International Phonetic Association, Handbook of the IPA (1999) and the IPA chart (2020 revision)", "Ladefoged & Johnson, A Course in Phonetics", "Catford, A Practical Introduction to Phonetics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Broad and narrow IPA transcription

**Goal:** write down what a speaker actually said in the International Phonetic
Alphabet, at the level of detail the task needs, in a form another linguist can read
back the same way.

## 1. Decide the level first
- **Phonemic / broad** — between **slashes** `/ˈkæt/`: only contrasts that distinguish
  words in that language. You need to know (or hypothesise) the phoneme inventory.
- **Phonetic / narrow** — in **square brackets** `[ˈkʰæʔt]`: what was physically
  produced, including allophones, aspiration, glottalisation, nasalisation, length.
- Mixing the two (brackets around a phonemic transcription) is the most common error
  in student work and papers. Use `⟨ ⟩` for spelling.

## 2. Describe before you symbolise
For every consonant, decide three things (the "VPM" label):
- **Voicing:** feel the larynx (fingers on throat) or cover your ears and listen for buzz.
- **Place:** bilabial, labiodental, dental, alveolar, postalveolar, retroflex, palatal,
  velar, uvular, pharyngeal, glottal.
- **Manner:** plosive, nasal, trill, tap/flap, fricative, lateral fricative,
  approximant, lateral approximant; plus affricates, ejectives, implosives, clicks.
Then find the cell on the chart. For vowels: **height**, **backness**, **rounding**,
plus length/nasality; locate relative to the cardinal vowels.

## 3. Useful narrow diacritics (most-used first)
- `ʰ` aspirated `[pʰ]`; `̚` unreleased `[t̚]`; `ʔ` glottal stop.
- `̥` voiceless `[n̥]`, `̬` voiced; `̃` nasalised `[ã]`; `ː` long, `ˑ` half-long.
- `̪` dental `[t̪]`; `ʷ` labialised; `ʲ` palatalised; `ˠ` velarised (dark l `[ɫ]`).
- `̩` syllabic `[n̩]`; `̯` non-syllabic `[aɪ̯]`.
- Stress `ˈ` primary, `ˌ` secondary — placed **before** the stressed syllable.
- Tone: diacritics (`á à â`) or Chao tone letters (`˥˩`), with a key stating which.
Only add what you heard and what the analysis needs; over-narrow transcriptions are
unreadable and often unreliable.

## 4. Process for a recording
1. Listen whole; note speaker, context, recording quality.
2. Segment into words/phrases; transcribe broadly first.
3. Replay **short stretches** (a syllable or word) many times; slow playback helps, but
   pitch-preserving slow-down can create artefacts — confirm against normal speed.
4. Add narrow detail where it matters; mark uncertain segments with `(?)` or a
   bracketed alternative, and say in a note what you couldn't decide.
5. Check acoustically when in doubt (formants for vowels, VOT for aspiration, the
   presence of a burst for stops) — see languages-linguistics.linguistics.praat.formant-pitch-measurement-and-textgrid-scripting.
6. Have a second transcriber do a portion; compare and compute agreement.

## 5. Ear-training drills
- Produce every chart sound yourself; you hear best what you can make.
- Minimal pairs in unfamiliar languages (e.g. dental vs alveolar, aspirated vs not).
- Nonsense-word dictation with a partner (Catford-style exercises).
- Daily 10 minutes of vowel placement against recordings of cardinal vowels.

## 6. Typing IPA
- Use Unicode IPA fonts (Charis SIL, Doulos SIL, Gentium) — they render diacritics
  correctly stacked.
- Input: the SIL IPA keyboard, an online IPA keyboard, or X-SAMPA-to-IPA conversion
  for ASCII-only workflows.
- **Gotcha:** visually similar characters: `ɡ` (IPA, U+0261) vs `g`; `ː` (U+02D0) vs
  colon; `ʼ` ejective vs apostrophe. Searchable corpora break on look-alikes.

## Verify
- [ ] Slashes for phonemic, brackets for phonetic, consistently.
- [ ] Every symbol corresponds to a VPM or vowel description you can state.
- [ ] Uncertain segments are marked, not silently guessed.
- [ ] A second transcriber's agreement on a sample is acceptable for the purpose.
- [ ] Text uses true IPA code points in an IPA-capable font.
