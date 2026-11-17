---
id: humanities.history.palaeography-and-diplomatics.transcribing-historical-handwriting
name: transcribing-historical-handwriting
category: humanities
field: history
product: palaeography-and-diplomatics
tags: [palaeography-and-diplomatics, paleography, palaeography, diplomatics, old-handwriting, historical-handwriting, secretary-hand, italic-hand, court-hand, copperplate, kurrent, sutterlin, latin-abbreviations, suspension, contraction, tironian-et, transcription, transcription-conventions, semi-diplomatic, expanded-transcription, charters, deeds, wills, regnal-years, dating-clause, transkribus, htr]
level: practitioner
status: draft
description: "Read and transcribe old handwriting reliably: building a letter key, decoding abbreviations, choosing a transcription convention, dating clauses and regnal years, and using HTR tools carefully."
sources:
  - "Marshall, H. Palaeography for Family and Local Historians (2nd ed., 2010)"
  - "The National Archives (UK), Palaeography: reading old handwriting 1500-1800 (online tutorial)"
  - "Cappelli, A. Lexicon Abbreviaturarum (Dizionario di abbreviature latine ed italiane)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transcribing historical handwriting

**Goal:** produce a faithful, checkable transcription of a handwritten document, and
understand its form well enough to date and interpret it. Examples lean on English
secretary hand and Latin abbreviations; the method transfers to other scripts (e.g.
German Kurrent).

## 1. Method: build a key from the document itself
1. **Read what you can first.** Names, dates and formulaic phrases ("In the name of God
   Amen", "Know all men by these presents") give you known letters.
2. **Make an alphabet key** for *this* scribe: cut out or draw each letter form from words you
   are sure of. Scribes are consistent with themselves, not with textbooks.
3. **Letter-by-letter** on hard words: count minims (the short strokes in i, m, n, u) — "minim
   confusion" makes *mmn* and *nim* look alike.
4. Leave genuine unknowns marked; come back with fresh eyes. Don't let context "autocorrect" a word.

## 2. Notorious secretary-hand letter forms
- **e** often looks like a backwards *o* or a reversed *6*; **h** has a long tail below the line.
- **c** resembles a modern *r*; **r** may look like a *w* or a *v*.
- Long **s** (ſ) looks like *f* without the full crossbar; it is used initially/medially.
- **u/v** and **i/j** are positional, not phonetic: *vnto*, *haue*, *Iohn*. Transcribe as written.
- Thorn: **ye** = *the*, **yt** = *that* (y stands for þ). Never read it as "ye".

## 3. Abbreviations
- **Suspension:** end of word omitted, often marked by a stroke (e.g. *Willm* for William).
- **Contraction:** middle omitted with a bar over (e.g. *pish* with mark = parish).
- **Special signs:** the *p* with a barred descender = *per/par*; crossed *p* with a loop = *pro*;
  superscript letters (*wch* = which); the tironian *et* ⁊ = *and*.
- For Latin, use Cappelli or an online abbreviation database; Latin documents follow strong
  formulae, so a diplomatics template of the document type helps fill gaps.

## 4. Transcription conventions — pick one and declare it
- **Diplomatic:** exactly as written, abbreviations retained, original lines and spelling.
- **Semi-diplomatic (common):** original spelling and capitalisation; abbreviations expanded
  in *italics* or [square brackets]; line breaks marked `|`; illegible text `[...]` or
  `[illeg.]`; uncertain readings `[?word]`; insertions `\word/`; deletions ~~word~~ or `<del>`.
- **Modernised:** for readers, not for evidence. Never the only version.
State the convention at the top of every transcription.

## 5. Diplomatics: reading the form
Documents follow a structure: protocol (invocation, address), text (exposition,
disposition, sanctions), eschatocol (dating clause, witnesses, seal). Knowing the part tells
you what words to expect. Dating clauses may use **regnal years** ("the fifth year of the
reign of…") and saints' days; convert with a handbook such as Cheney's *Handbook of Dates*.
In England before 1752 the year began on 25 March — write "10 February 1650/1".

## 6. Handwritten text recognition (HTR)
Tools like Transkribus can produce rough transcriptions for consistent hands and large
volumes. Treat output as a draft: proofread every line against the image, especially
names, numbers and dates. *Accuracy varies widely by model and hand; not verified here.*

## Gotchas
- Names: spelling wasn't standardised; transcribe as written and normalise only in an index.
- Numbers: Roman numerals with a final *j* (*viij* = 8); £ s d with superscript marks.
- Damaged areas: note the reason (`[torn]`, `[stain]`) not just `[...]`.

## Verify
- [ ] Transcription convention stated at the top.
- [ ] Every uncertain reading is marked, not silently guessed.
- [ ] Abbreviation expansions are distinguishable from original text.
- [ ] Dates converted with the calendar issue noted.
- [ ] HTR output proofread line by line against the image.
