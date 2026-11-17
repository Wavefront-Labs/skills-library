---
id: languages-linguistics.linguistics.morphology-syntax.interlinear-glossing-and-constituency-tests
name: interlinear-glossing-and-constituency-tests
category: languages-linguistics
field: linguistics
product: morphology-syntax
tags: [morphology-syntax, morphology, syntax, interlinear-glossing, igt, leipzig-glossing-rules, morpheme-segmentation, gloss-abbreviations, constituency-tests, substitution, movement, coordination, ellipsis, clefting, tree-diagrams, x-bar, agreement, argument-structure, grammatical-relations, case, alignment, ergativity]
level: practitioner
status: draft
description: "Gloss example sentences to the Leipzig Glossing Rules and test syntactic structure with constituency tests (substitution, movement, coordination, ellipsis), with the classic pitfalls of each."
sources: ["Leipzig Glossing Rules (Max Planck Institute for Evolutionary Anthropology, 2008/2015)", "Carnie, Syntax: A Generative Introduction", "Payne, Describing Morphosyntax"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interlinear glossing and constituency tests

**Goal:** present language data so any linguist can see each morpheme's form and
function, and justify the structure you claim for a sentence with tests rather than
intuition.

## 1. Interlinear glossed text (IGT) — the three lines
```
(1) Ni-li-m-pa                  kitabu.
    1SG.SBJ-PST-3SG.OBJ-give     book
    'I gave him/her a book.'
```
(Swahili-style example for illustration; check against a source before citing.)
1. **Object line:** the language data, segmented with hyphens.
2. **Gloss line:** one gloss per morpheme, aligned word by word.
3. **Free translation:** in quotes.
Add a source line (speaker, corpus, page) when it's not your own elicitation.

## 2. The Leipzig rules you'll use daily
- **Hyphen `-`** separates segmentable morphemes, with the **same number of hyphens**
  in object and gloss lines.
- **`=`** marks clitics.
- **`.`** joins several glosses for one object-language element (`come.PST` for `came`).
- **`:`** for non-segmentable but distinguishable features (some authors);
  **`\`** for morphophonological change (e.g. `mouse\PL`); **`<>`** infixes;
  **`~`** reduplication.
- **Grammatical categories in small caps** (or capitals): `PST`, `PL`, `ERG`, `DEF`.
  Use the standard abbreviations (1, 2, 3, SG, PL, NOM, ACC, ERG, ABS, PFV, IPFV…);
  list any non-standard ones in an abbreviations table.
- Lexical glosses in lowercase; multi-word glosses joined with dots (`come.out`).
**Gotcha:** word processors break alignment — use tabs, a table, or tools (LaTeX
`gb4e`/`expex`, the `langsci` templates, FLEx/ELAN export) rather than spaces.

## 3. Morphological parsing
- Compare forms in paradigms; a recurring form–meaning pairing is a morpheme.
- Identify zero morphemes only when the paradigm demands them (`-Ø`), and say why.
- Distinguish **inflection** (obligatory, grammatical, paradigm-forming) from
  **derivation** (new word, may change class) and clitics from affixes (clitics attach
  to phrases, show low selectivity of host).

## 4. Constituency tests
Run several; one test alone proves little.
- **Substitution (pro-form):** a string replaceable by a pronoun/*do so*/*there* is a
  constituent. "[The old dog] slept" → "It slept."
- **Movement / topicalisation / clefting:** "It was [the old dog] that slept."
- **Coordination:** "[the old dog] and [the cat]". **Gotcha:** coordination over-generates
  (non-constituent coordination: "John gave [Mary a book] and [Sue a pen]").
- **Ellipsis / VP deletion:** "Kim will [read the book], and Lee will too."
- **Answer fragment:** "What slept? — The old dog."
Report which tests passed and failed; conflicting results are data about the
structure, not noise.

## 5. Grammatical relations and argument structure
- Identify subject/object by **behaviour** (agreement, case, word order, control,
  reflexive binding), not by meaning.
- Check alignment: nominative–accusative vs ergative–absolutive (S patterning with A
  or with P). Split systems (by tense/aspect or person) are common.
- Note valency changes: passive, antipassive, applicative, causative.

## 6. Drawing trees
- Pick one framework and state it (X-bar/Minimalist, LFG, dependency).
- Every node should be justified by a test or a theoretical commitment you name.
- For dependency or corpus work, Universal Dependencies conventions are widely used.

## Verify
- [ ] Hyphen counts match between object and gloss lines on every example.
- [ ] All grammatical abbreviations are standard or listed.
- [ ] Free translation is idiomatic and in quotes.
- [ ] Each constituency claim cites at least two passing tests.
- [ ] Subject/object claims are based on syntactic behaviour, not semantic role.
