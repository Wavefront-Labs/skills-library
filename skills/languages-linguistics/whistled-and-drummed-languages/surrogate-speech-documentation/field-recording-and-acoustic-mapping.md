---
id: languages-linguistics.whistled-and-drummed-languages.surrogate-speech-documentation.field-recording-and-acoustic-mapping
name: field-recording-and-acoustic-mapping
category: languages-linguistics
field: whistled-and-drummed-languages
product: surrogate-speech-documentation
tags: [surrogate-speech-documentation, surrogate-speech, speech-surrogate, whistled-language, drummed-language, talking-drums, language-documentation, field-recording, fieldwork, linguistic-fieldwork, acoustic-analysis, praat, spectrogram, pitch-tracking, f0, formants, elan, annotation, metadata, archiving, elar, paradisec, informed-consent, documentary-linguistics, ethnomusicology]
level: advanced
status: draft
description: "Document whistled and drummed speech: consented field recording with matched spoken versions, careful metadata, Praat analysis of pitch, and a mapping from surrogate signal to the source phonology."
sources: ["Meyer, Whistled Languages (Springer 2015) — field methods and acoustics", "Seifart et al. 2018, 'Reducing language to rhythm: Amazonian Bora drummed language…' (Royal Society Open Science)", "Boersma & Weenink, Praat manual (praat.org)", "Bowern, Linguistic Fieldwork: A Practical Guide (2nd ed.)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Field recording and acoustic mapping of surrogate speech

**Goal:** produce recordings and analyses of a whistled or drummed language that (a) are
usable by researchers and the community decades from now, and (b) show precisely which
features of the spoken language the surrogate carries.

*Method synthesis from documentary linguistics; adapt to local ethics rules and community
protocols.*

## 1. Ethics and permissions first
- Obtain **informed consent** from each performer in a form and language they understand:
  what will be recorded, who will access it, whether it will be published or archived openly.
  Record oral consent if writing isn't appropriate.
- Respect restrictions: some drum texts or whistles are sacred, lineage-owned or not for
  outsiders. Record access conditions in metadata.
- Agree on credit and benefit return (copies to the community, school use).
- University projects typically need ethics/IRB approval.

## 2. Recording setup
- **Recorder**: uncompressed WAV, at least 44.1 kHz/16-bit (48 kHz/24-bit preferred). Whistles
  commonly fall roughly in the 1–4 kHz range, well within this.
- **Microphones**: one close mic near the performer and, for distance traditions, a second
  mic at the **listener's** position (hundreds of metres away) to capture what's actually heard.
  Note the distance and terrain.
- Avoid automatic gain control and heavy noise reduction; set levels so loud strokes or
  whistles peak around −12 to −6 dBFS — finger whistles and drums are louder than you expect.
- Log wind, temperature/humidity if relevant to propagation, and background noise.
- Video helps: drum technique (cord squeezing, stick placement) and whistling hand positions.

## 3. Elicitation design
For every surrogate utterance, record the **spoken version** by the same person (and ideally
a second speaker). Useful sets:
- word lists with minimal tone or vowel contrasts;
- standard phrases and formulas (greetings, calls, drum praise names);
- natural exchanges: a real message relayed between two whistlers/drummers;
- comprehension tests: play recorded surrogate items to listeners and log their responses.
Number items and announce the number aloud at the start of each take.

## 4. Annotation
- Segment and transcribe in **ELAN** or Praat TextGrids: tiers for spoken transcription
  (with tones), surrogate segments (notes/strokes/whistled syllables), translation, comments.
- Keep spoken and surrogate items aligned by item number.

## 5. Acoustic analysis (Praat)
- Whistles: extract the whistle's frequency over time (it's near-sinusoidal, so the spectrogram's
  strongest band or a pitch track with a raised ceiling, e.g. 500–5,000 Hz). Default pitch
  settings are tuned for voice and will fail on whistles.
- Drums: measure stroke onset times, inter-onset intervals and perceived/measured pitch per
  stroke; tension drums glide, so measure contour, not just a point value.
- Compare against the spoken version: F0 contour for tonal languages; vowel F2 (and F1) for
  non-tonal whistled languages; syllable durations for rhythm.
- Plot mappings (e.g. whistle frequency by vowel category; drum pitch by tone category) and test
  whether categories are separable.

## 6. Archiving
Deposit with a language archive (e.g. ELAR, PARADISEC, AILLA, or a national archive): WAV
masters, annotation files, consent records, metadata (who, where, when, equipment, conditions,
access level). Keep copies in the community.

## Gotchas
- Compressed audio (MP3, phone apps with processing) distorts the very cues you study.
- Recording only close-mic surrogates misses the distance degradation that shapes the system.
- Elicited citation forms differ from real messages; include natural use.
- Analysts "hear" the spoken language into the surrogate — use blind comprehension tests.

## Verify
- [ ] Consent and access conditions documented for every performer.
- [ ] Each surrogate item has a matching spoken recording and item number.
- [ ] WAV masters, annotations and metadata are archived and backed up in two places.
- [ ] A mapping plot shows how surrogate pitch/rhythm relates to source tone/formants.
- [ ] Community has received copies in a usable format.

Related: `languages-linguistics.whistled-and-drummed-languages.surrogate-language-revitalisation.teaching-programmes-and-safeguarding-plans`,
`languages-linguistics.whistled-and-drummed-languages.whistled-speech-technique.encoding-tone-and-formants-in-whistle`.
