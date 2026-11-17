---
id: humanities.musicology.music-analysis.harmonic-formal-and-schenkerian-analysis-for-scholarship
name: harmonic-formal-and-schenkerian-analysis-for-scholarship
category: humanities
field: musicology
product: music-analysis
tags: [music-analysis, music-theory, analysis, harmonic-analysis, roman-numeral-analysis, functional-harmony, cadence, pac, hc, formal-analysis, sonata-form, sonata-theory, hepokoski-darcy, caplin, formenlehre, form-functions, sentence, period, schenkerian-analysis, schenker, urlinie, ursatz, voice-leading, prolongation, reduction, post-tonal, set-theory, forte-numbers, neo-riemannian, analytical-argument, music-theory-spectrum]
level: advanced
status: draft
description: "Analyse a tonal work for publication: Roman-numeral and functional labels, formal plan (sonata, Formenlehre), basic Schenkerian voice-leading graphs, and turning observations into an argument."
sources: ["William Caplin, Classical Form (1998)", "Hepokoski & Darcy, Elements of Sonata Theory (2006)", "Cadwallader & Gagné, Analysis of Tonal Music: A Schenkerian Approach (3rd ed.)", "Allen Forte, The Structure of Atonal Music (1973)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Harmonic, formal and Schenkerian analysis for scholarship

**Goal:** go from "I've labelled the chords" to an analytical claim a theory journal
would accept: something about how *this* piece works that a reader can check in the score.

## 1. Pass one: harmony with a key plan
- Use a reliable edition (urtext or critical edition; see
  humanities.musicology.music-source-studies.collation-and-critical-editions-of-music)
  and number the bars.
- Label Roman numerals with inversions (`V6/5`, `ii6`, `V7/V`); mark **cadences**
  (PAC, IAC, HC, deceptive) with bar numbers — they are the punctuation that form hangs on.
- Separate **chord** from **embellishment**: suspensions, passing and neighbour notes,
  cadential 6/4 (label as `V` with 6/4–5/3, or `Cad6/4`, but be consistent and say which).
- Draw the **key scheme**: tonic → modulations (where confirmed by a cadence, not just
  an accidental).

## 2. Pass two: form
- Phrase level (Caplin's form functions): **sentence** (presentation – continuation –
  cadential), **period** (antecedent – consequent), hybrids. Measure lengths.
- Movement level: for sonata form, find the medial caesura, secondary theme,
  essential expositional closure (EEC) and its recapitulation partner (ESC) in
  **Hepokoski–Darcy** terms, or use Caplin's interthematic functions. Pick one framework
  per paper and define its terms on first use.
- Note what's *unusual* against the norm: a missing cadence, an expanded transition, a
  recapitulation in the "wrong" key. Deviations are where arguments live.

## 3. Pass three: voice leading (Schenkerian basics)
- Reduce in levels: foreground (remove embellishments) → middleground (prolonged
  harmonies, linear progressions, arpeggiations) → background (**Ursatz**: fundamental
  line 3–2–1, 5–4–3–2–1 or 8–...–1 over I–V–I bass arpeggiation).
- Notation: open noteheads with stems for structural tones, filled heads for
  subordinate ones, slurs for prolongations, beams for linear progressions, scale-degree
  carets (`^3`). Draw with notation software (MuseScore/Dorico/Sibelius) or a
  dedicated tool — check journal formatting rules.
- The choice of **Kopfton** (head tone) must be justified by register and emphasis, not
  chosen to make the graph tidy.
- Schenkerian reading is interpretive: present it as a reading, and show the
  alternatives you rejected and why.

## 4. Beyond tonality
For post-tonal music: pitch-class set analysis (prime forms, Forte numbers, interval
vectors), twelve-tone row tables (P/I/R/RI), or neo-Riemannian transformations (P, L, R)
for chromatic triadic music. Use **music21** to check set-class claims mechanically.

## 5. Turn analysis into argument
- Lead with the claim: "The recapitulation withholds tonic closure until the coda,
  recasting the second theme as..." then the evidence by bar number.
- Examples: annotate scores and graphs with bar numbers; every claim in prose points
  to an example.
- Engage the literature: who else analysed this piece, and where do you differ?
- Connect to context (sketches, performance, reception) where it strengthens the case.

## Gotchas
- Labels are not analysis. A paper of Roman numerals with no claim gets rejected.
- Mixing frameworks' terms (Caplin's "continuation" vs Hepokoski–Darcy's rotations)
  without definition confuses readers and reviewers.
- Edition differences (a missing accidental) can change a harmonic reading — check.
- Status: draft; terminology summarised from the cited texts, not exhaustive.

## Verify
- [ ] Every cadence and modulation has a bar number and is cadentially confirmed.
- [ ] Form chart shows sections, bar ranges, keys and the framework used.
- [ ] Graph levels are consistent and the Kopfton choice is justified.
- [ ] The paper states one main claim in the first paragraph.
- [ ] Prior analyses of the piece are cited and engaged.
