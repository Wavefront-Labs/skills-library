---
id: languages-linguistics.lexicography.dictionary-compilation.planning-headwords-entry-structure-and-corpus-based-sense-division
name: planning-headwords-entry-structure-and-corpus-based-sense-division
category: languages-linguistics
field: lexicography
product: dictionary-compilation
tags: [dictionary-compilation, lexicography, dictionary-making, headword-list, lemma, lemmatisation, macrostructure, microstructure, entry-structure, homographs, polysemy, sense-division, lumping-and-splitting, corpus-lexicography, concordance, kwic, frequency-list, style-guide, dictionary-writing-system, tlex, lexonomy, tei-lex-0, dmlex, learner-dictionary, bilingual-dictionary]
level: advanced
status: draft
description: "Plan and build a dictionary: user-driven scope, a frequency-based headword list, a consistent entry microstructure and style guide, and splitting senses from concordance evidence."
sources: ["Atkins & Rundell, The Oxford Guide to Practical Lexicography (paraphrased)", "TEI Lex-0 and OASIS DMLex documentation (overview)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Planning headwords, entry structure and corpus-based sense division

**Goal:** a dictionary whose word list, entries and senses follow from evidence and a
written plan — so many compilers working over years produce one consistent book or database.

## 1. Start from the user
Write down: **who** uses it (learners, translators, native speakers, specialists), **for
what** (decoding text, encoding/writing, translation), **in what medium** (print page limits,
app, API) and **which language variety**. These answers drive every later choice: a learner's
dictionary needs a controlled defining vocabulary and many examples; a historical dictionary
needs dated citations.

## 2. Build the headword list (macrostructure)
- Generate a **lemmatised frequency list** from a representative corpus of the target variety
  (see the sketch-engine skill). Set a frequency cut-off from the dictionary's size budget.
- Add **user-need items** the corpus underrepresents: everyday household words, new coinages,
  regional items, words learners will look up.
- Decide treatment rules once:
  - **Lemma form** (infinitive vs stem; singular nouns; how to handle irregular forms —
    cross-reference entries).
  - **Homographs vs polysemy:** separate headwords for unrelated words (*bank* river /
    *bank* finance, often by etymology or part of speech) vs one entry with many senses.
  - **Multi-word expressions:** headwords, run-ons under a key word, or phrase sections.
  - Abbreviations, proper names, affixes: in or out.

## 3. Design the microstructure and style guide
Fix the **order and form** of every entry component: headword, pronunciation, part of speech,
inflections, grammar codes, **sense** blocks (definition, examples, labels for register,
region, domain), phrases, derived forms, etymology, cross-references.
- Encode it as a **data model** (an XML schema such as TEI Lex-0, or the OASIS DMLex model)
  rather than as formatting, so the same data can publish to print, web and API.
- Write a **style guide** with examples for every component and edge case; it's the single
  most important consistency tool. Use a dictionary writing system (e.g. TLex, Lexonomy, or an
  in-house editor) that enforces the schema.

## 4. Divide senses from evidence
1. Pull a **concordance** (KWIC) of the lemma — a random sample of a few hundred lines for
   common words.
2. **Sort and group** lines by pattern: collocates, grammar (transitive/intransitive, + *to*),
   subject types, register. Each stable cluster is a candidate sense.
3. **Lump or split** according to the users: split when patterns differ in grammar, meaning or
   translation (essential for bilingual work); lump fine shades a learner can't use.
4. **Order senses** by frequency (synchronic dictionaries) or chronology (historical ones) —
   be explicit which.
5. Pick **examples** from the corpus that show the typical pattern, lightly edited if needed
   for length (policy on editing is a style-guide decision).
Record a frequency count per sense from the sample so later editors can review decisions.

## Gotchas
- Corpus bias: web corpora overrepresent some genres; spoken and regional usage may be thin.
- Copying the word list or sense structure of an existing dictionary carries its biases and
  may raise copyright issues.
- Style-guide drift over long projects — schedule consistency checks by headword range.
- New senses appear first in small numbers: monitor recent-data subcorpora.

## Verify
- [ ] User profile and size budget written before the word list is built.
- [ ] Headword list traceable to corpus frequency plus a documented user-needs list.
- [ ] Schema and style guide cover every entry component with examples.
- [ ] A sample entry's senses can be traced to concordance clusters with counts.
- [ ] Two compilers given the same lemma produce structurally consistent entries.
