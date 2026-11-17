---
id: languages-linguistics.writing-systems-and-scripts.script-decipherment.structural-analysis-of-an-undeciphered-script
name: structural-analysis-of-an-undeciphered-script
category: languages-linguistics
field: writing-systems-and-scripts
product: script-decipherment
tags: [script-decipherment, decipherment, undeciphered-scripts, sign-inventory, sign-list, allography, paleography, frequency-analysis, positional-analysis, distributional-analysis, kober-triplets, ventris-grid, linear-b, linear-a, indus-script, rongorongo, proto-elamite, bilingual-inscriptions, rosetta-stone, onomastics, corpus, epigraphy, type-token]
level: sme
status: draft
description: "Analysing an undeciphered script: clean sign inventory, script type from sign counts, positional and distributional analysis, grids, and tests against bilinguals and names."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structural analysis of an undeciphered script

**Goal:** extract as much structure as possible from a corpus in an unknown script —
script type, word divisions, grammar-like patterns — before (and as a check on) any
proposed reading.

> Draft. Method summarised from well-documented decipherments (notably Linear B by Kober
> and Ventris) and standard epigraphic practice. The sign-count ranges below are
> commonly cited rules of thumb, not laws. Most published "decipherments" of famous
> unread scripts fail exactly the tests in the Verify list.

## 1. Build the corpus properly
- Collect every inscription with **provenance, date, object type and orientation**.
  Work from photographs/drawings of originals, not from someone's normalised copy.
- Assign stable inscription IDs; record damage and uncertain readings explicitly
  (e.g. `[?]`, `[...]`).
- Note **direction of writing** (sign orientation, line layout, crowding at line ends).

## 2. The sign inventory (the hardest step)
- Separate **signs** from **allographs** (variant forms of one sign, by scribe, period or
  medium) and from ligatures/composites. Over-splitting inflates the inventory; over-
  lumping hides contrasts.
- Use distribution to decide: two forms that appear in identical contexts in parallel
  texts are probably allographs.
- Publish the sign list with numbered signs, examples and your merge/split decisions.

## 3. Estimate the script type from inventory size
Rough heuristics:
- ~20–40 signs → alphabet or abjad.
- ~40–100 → syllabary (Linear B has ~87 syllabic signs).
- Hundreds or more → logo-syllabic/logographic system (Mayan, cuneiform, Chinese).
Check with a **sign-saturation curve**: plot new signs found vs corpus size; if it hasn't
flattened, your inventory is incomplete and the estimate is unreliable.
Also separate numerals, metrology and ideograms (often in accounting texts) from the
phonetic set.

## 4. Positional and distributional analysis
1. **Word segmentation:** use dividers if present; otherwise look for recurring
   sequences.
2. **Frequencies** of each sign overall and by position (initial, medial, final). Signs
   frequent word-initially but rare elsewhere may be pure vowels (in a syllabary).
3. **Alternating endings** on a shared stem — Kober's "triplets" in Linear B — suggest
   inflection, and that the alternating signs share a consonant or vowel.
4. **Grid:** arrange signs into a table where rows share a (hypothesised) consonant and
   columns a vowel, from alternation evidence alone, before assigning any sound values
   (Ventris's grid).
5. **Context:** text type (lists, dedications, seals), associated pictograms, numerals and
   commodity signs give semantic anchors.

## 5. Anchors for reading
- **Bilinguals** (the Rosetta Stone model): any parallel text in a known script.
- **Proper names** — places, rulers, gods — likely preserved in later languages or
  neighbouring records.
- **Later descendant scripts** and loan words.
- **Candidate language** hypotheses: test, don't assume.

## 6. Testing a proposed decipherment
A real decipherment:
- applies **one consistent set of values** across the whole corpus;
- yields **language-like** output that fits a known or reconstructable language;
- **predicts** readings of texts not used to derive the values (including new finds —
  Linear B's Pylos tablet test is the classic case);
- doesn't need ad-hoc exceptions for each inscription.

## Gotchas
- Small corpora (Indus seals are short; rongorongo is tiny) may not contain enough
  information to decipher at all.
- Confirmation bias: matching a favourite language by selecting convenient values.
- Ignoring allography and scribal hands.
- Treating iconicity of signs as their meaning.

## Verify
- [ ] Sign list published with allography decisions and a saturation curve.
- [ ] Frequency and positional tables computed per sign.
- [ ] Any grid was built from internal evidence before sound values were assigned.
- [ ] Proposed values were tested on held-out inscriptions with consistent results.
