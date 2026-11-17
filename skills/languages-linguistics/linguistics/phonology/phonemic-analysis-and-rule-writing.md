---
id: languages-linguistics.linguistics.phonology.phonemic-analysis-and-rule-writing
name: phonemic-analysis-and-rule-writing
category: languages-linguistics
field: linguistics
product: phonology
tags: [phonology, phonemic-analysis, phoneme, allophone, minimal-pairs, near-minimal-pairs, complementary-distribution, free-variation, natural-classes, distinctive-features, phonological-rules, spe, rule-ordering, feeding, bleeding, optimality-theory, constraints, syllable-structure, sonority, stress, tone, problem-sets]
level: practitioner
status: draft
description: "Analyse a sound system from data: find minimal pairs, test complementary distribution, pick the underlying form, write feature-based rules, order them, and sanity-check against OT-style constraints."
sources: ["Hayes, Introductory Phonology", "Odden, Introducing Phonology", "Kager, Optimality Theory"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Phonemic analysis and rule writing

**Goal:** from a set of transcribed words, determine which sounds are contrastive
(phonemes), which are predictable variants (allophones), and state the predictions as
explicit rules (or constraints) that generate the data and nothing else.

## 1. Set up the data
- Work from consistent **narrow transcriptions** with glosses.
- List every segment that occurs; group suspicious pairs: sounds that are phonetically
  similar (e.g. `[t]`/`[tʰ]`, `[s]`/`[ʃ]`, `[i]`/`[ɪ]`, `[l]`/`[ɫ]`).

## 2. Test each suspicious pair
1. **Minimal pair** (same environment, different meaning: `[pʰɪn]` 'pin' vs `[bɪn]`)
   → separate phonemes. Near-minimal pairs are acceptable evidence when exact pairs
   don't exist; say so.
2. **No pairs?** Tabulate environments: preceding and following segment, syllable
   position, stress, word edge.
3. **Complementary distribution** (never in the same environment) → allophones of one
   phoneme. **Gotcha:** complementary distribution is necessary but not sufficient —
   English `[h]` (onsets) and `[ŋ]` (codas) are complementary but no one treats them
   as one phoneme; phonetic similarity matters.
4. **Overlapping distribution with no meaning change** → free variation (check
   speakers, register, speech rate).

## 3. Choose the underlying form (the "basic" allophone)
Pick the allophone that occurs in the **widest / elsewhere** set of environments; the
others then have statable conditions. If two choices both work, prefer the one giving
**simpler, more natural** rules (e.g. voicing assimilation, not dissimilation for no
reason).

## 4. Write the rule
Standard SPE-style format: `A → B / C __ D` ("A becomes B between C and D").
- Use **features and natural classes**, not lists: `[−sonorant, −continuant, −voice]
  → [+spread glottis] / # __` ("voiceless stops aspirate word-initially"), not
  "p, t, k → pʰ, tʰ, kʰ".
- Notation: `#` word boundary, `$` or `.` syllable boundary, `C`/`V` cover symbols,
  `( )` optional, `{ }` either/or, `Ø` zero (deletion/insertion).
- A good rule is **as general as the data allows**; test it against every form,
  including ones where it shouldn't apply.

## 5. Morphophonology and rule ordering
When morphemes alternate (e.g. plural `-s/-z/-ɪz`):
1. Line up the alternants; choose an underlying form that makes the rules natural.
2. Write each rule; then test orders:
   - **Feeding:** rule A creates the input for B.
   - **Bleeding:** A removes B's input.
   - **Counter-feeding / counter-bleeding** = opacity; flag it, it's evidence for order.
3. Derivation tables (UR → rule 1 → rule 2 → SR) for every alternant show the order works.

## 6. Constraint-based check (OT)
If your course or paper is OT-based: express the same generalisation as ranked
markedness vs faithfulness constraints in a tableau; check every candidate loses for
the right reason. Same data, different formalism — convert carefully, don't mix.

## 7. Suprasegmentals
- **Syllables:** apply sonority sequencing; justify onset/coda choices with
  phonotactics (which clusters occur word-initially/finally).
- **Stress:** test fixed (initial/penultimate), weight-sensitive or lexical; collect
  words of 1–5 syllables with different syllable weights.
- **Tone:** separate lexical from grammatical tone; record words in isolation and in
  frames; watch for downdrift and tone sandhi.

## Verify
- [ ] Every claimed phoneme pair has a (near-)minimal pair cited.
- [ ] Every allophonic rule is stated with features and checked against *all* forms.
- [ ] Underlying forms justified (elsewhere case, naturalness).
- [ ] Derivations show the rule order produces each surface form.
- [ ] Counterexamples or gaps in the data are stated, not hidden.
