---
id: creative-arts.animation.voice-tts.pronunciation-dictionaries-and-lexicons
name: pronunciation-dictionaries-and-lexicons
category: creative-arts
field: animation
product: voice-tts
tags: [pronunciation-dictionary, lexicon, pls, phoneme, tts-control, g2p, invented-names]
level: practitioner
status: draft
description: "Fix TTS pronunciation of invented names, acronyms and jargon with pronunciation dictionaries: alias versus phoneme rules, PLS files, testing and per-character scope."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pronunciation dictionaries and lexicons

TTS engines guess how to say unfamiliar words. In animation, invented names and sound effects spelled as words break this guess constantly. A pronunciation dictionary lets you set the pronunciation once, and apply it to every generation.

## Two kinds of rule
- **Alias / respelling**: replace the written word with a phonetic respelling the engine handles ("Xorblax" becomes "Zor-blacks"). Works in every engine and is the first thing to try.
- **Phoneme rule**: give an exact phonetic transcription in IPA (or the engine's own alphabet, such as CMU/ARPAbet for some). Precise but needs a phonetic transcription and engine support.

## Formats
- **PLS** (Pronunciation Lexicon Specification, a W3C standard) is an XML file of lexemes with a grapheme and a phoneme or alias. ElevenLabs lets you upload a PLS file or build rules in its dictionary tool, then attach the dictionary to text-to-speech requests; check the docs for current limits on rules and case sensitivity.
- Cloud TTS services and some local engines accept lexicons or per-request `<phoneme>` and `<sub>` SSML (`ssml-breaks-and-pauses.md`).
- For engines without lexicon support, preprocess the script: a find-and-replace pass that rewrites names to respellings before sending the text.

## Practice
1. Collect problem words from a first test generation; add them to a shared list with the agreed pronunciation approved by the director or writer.
2. Prefer respelling first; move to phonemes only when respelling fails.
3. Keep one dictionary per series, and per-character overrides only where voices differ.
4. Version the dictionary file with the project and re-generate affected lines after changes.
5. Keep the respelled text out of subtitles: the dictionary acts at synthesis time, not in the script.

## Verify
- [ ] Each rule tested by generating the word in a sentence.
- [ ] Dictionary under version control with the script.
- [ ] Subtitles use the original spelling.
