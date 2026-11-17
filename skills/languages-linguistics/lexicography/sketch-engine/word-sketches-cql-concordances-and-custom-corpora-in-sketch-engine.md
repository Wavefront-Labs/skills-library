---
id: languages-linguistics.lexicography.sketch-engine.word-sketches-cql-concordances-and-custom-corpora-in-sketch-engine
name: word-sketches-cql-concordances-and-custom-corpora-in-sketch-engine
category: languages-linguistics
field: lexicography
product: sketch-engine
tags: [sketch-engine, corpus-query, corpus-linguistics, word-sketch, word-sketch-difference, logdice, collocations, concordance, kwic, cql, corpus-query-language, regex, pos-tags, gdex, good-dictionary-examples, thesaurus, distributional-thesaurus, keywords, term-extraction, reference-corpus, wordlist, frequency-list, tenten-corpora, webbootcat, custom-corpus, lexicography]
level: practitioner
status: draft
description: "Use Sketch Engine for lexicography: read word sketches and logDice, write CQL queries, sort and sample concordances, pick GDEX examples, extract keywords and build your own corpus."
sources: ["Sketch Engine user guide and CQL documentation (paraphrased)", "Kilgarriff et al., The Sketch Engine: ten years on (2014)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Word sketches, CQL concordances and custom corpora in Sketch Engine

**Goal:** get from "how is this word used?" to defensible evidence — collocations, patterns,
senses, examples and term lists — quickly, without being misled by the tool's defaults.

> Uncertainty: feature names follow the current web interface as generally documented;
> menus and default settings change between releases. Tag names depend on the corpus's tagset.

## 1. Pick the right corpus first
- Large **web corpora** (the "TenTen" family, e.g. English enTenTen) give coverage of common
  and new usage; specialised or historical corpora answer different questions.
- Check the corpus **info page**: size, sources, date range, tagset. Every later number is
  only as representative as this corpus.
- For contrast work, choose a **reference corpus** in the same language (needed for keywords).

## 2. Word Sketch: the one-page summary
- Enter a lemma and part of speech. The sketch lists **grammatical relations** (objects of a
  verb, modifiers of a noun, "and/or" partners, prepositional phrases) with collocates.
- Collocates are ranked by **logDice**, a salience score (max 14) that's stable across corpus
  sizes; frequency is shown separately. High logDice + reasonable frequency = typical pattern.
- Click any collocate to jump to its concordance lines — always inspect real lines before
  trusting a relation (parsing errors create odd collocates).
- **Word Sketch Difference** compares two lemmas (*big* vs *large*) or one lemma in two
  subcorpora — ideal for near-synonym usage notes and regional labels.

## 3. Concordances and CQL
Simple queries cover most needs; **CQL** (Corpus Query Language) gives control:
```
[lemma="make"] [tag="DT.*"]? [lemma="decision"]       make (a/the) decision
[lemma="go"] []{0,2} [word="home"]                    go … home with up to 2 words between
[lemma="interest"] [word="in"] [tag="N.*"]            interest in + noun
[word="(?i)e-?mail"]                                  email / e-mail, case-insensitive regex
```
(Tag patterns like `N.*` and `DT.*` assume a Penn-style English tagset; check the corpus's tagset.)
Working the concordance:
- **Sort** by the word to the right or left of the node to make patterns jump out.
- **Sample** (e.g. 250 random lines) before analysing frequent words — don't read the first page only.
- **Frequency** on node forms or on a context position to count variants and complements.
- Use **filters** and **text types** (genre, domain, date where available) to compare usage.
- Tag lines manually into sense groups when dividing senses (see dictionary-compilation skill).

## 4. Examples and thesaurus
- **GDEX** ranks concordance lines by suitability as dictionary examples (length, common
  words, complete sentence). Treat it as a shortlist; still read for typicality and
  offensiveness.
- The **Thesaurus** lists distributionally similar words — useful for finding synonyms,
  antonyms and co-hyponyms to check definitions against, not a list of true synonyms.

## 5. Keywords and terms
- **Keywords** compare your focus corpus with the reference corpus; a smoothing parameter
  shifts results toward rarer (low value) or more common (higher value) words.
- **Terms** extraction finds multi-word candidates — a fast start for a termbase, but review
  every candidate with a subject expert.

## 6. Build your own corpus
- Upload documents (common formats are accepted) or build from the web from seed words
  (WebBootCaT-style). The system tags and lemmatises automatically for supported languages.
- Add metadata (source, date, author type) as **text types** so you can filter later.
- Check copyright and confidentiality before uploading client or licensed texts.

## Gotchas
- Web corpora contain duplicates, spam and machine translation; check suspicious spikes.
- Lemmatiser errors cluster on rare and new words — search by word form too.
- Frequency per million, not raw counts, when comparing corpora of different sizes.

## Verify
- [ ] Corpus info (size, sources, tagset) noted alongside every finding.
- [ ] Each collocation claim backed by inspected concordance lines.
- [ ] CQL query tested on a known case before use on the real question.
- [ ] Analyses on frequent words used a random sample.
- [ ] Custom corpus uploads cleared for rights and given text-type metadata.
