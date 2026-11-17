---
id: languages-linguistics.linguistics.corpus-linguistics.concordancing-collocation-and-frequency-analysis
name: concordancing-collocation-and-frequency-analysis
category: languages-linguistics
field: linguistics
product: corpus-linguistics
tags: [corpus-linguistics, corpus, concordance, kwic, collocation, collocates, mutual-information, log-dice, log-likelihood, t-score, keyness, keywords, frequency, normalised-frequency, dispersion, antconc, sketch-engine, cqpweb, cqp, coca, bnc, lancsbox, corpus-design, annotation, pos-tagging, lemmatisation]
level: practitioner
status: draft
description: "Use corpora as evidence: pick or build a corpus, read KWIC concordances, normalise frequencies, choose collocation and keyness statistics (MI, logDice, LL) and report reproducibly."
sources: ["McEnery & Hardie, Corpus Linguistics: Method, Theory and Practice", "Brezina, Statistics in Corpus Linguistics", "Anthony, AntConc documentation (laurenceanthony.net)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Concordancing, collocation and frequency analysis

**Goal:** answer a language question ("how is *utterly* used?", "what's distinctive
about this genre?") with corpus evidence that another researcher could reproduce.

## 1. Pick or build the corpus
- **Existing reference corpora:** BNC (British English), COCA (American), national
  corpora, Universal Dependencies treebanks, web corpora in Sketch Engine. Check
  licence, size, period, genres, and whether it's annotated (POS, lemma).
- **Building your own:** define the population (whose language, which genres, which
  dates), sampling frame and balance; keep metadata per text; clean (boilerplate,
  encoding — save as UTF-8); document all decisions.
- Copyright: you may analyse texts you can't redistribute; record what you can share.

## 2. Tools
- **AntConc** (free, desktop): KWIC, collocates, clusters/n-grams, keywords, plots.
- **Sketch Engine** (subscription): word sketches, CQL queries, large preloaded corpora.
- **CQPweb / CQP**: CQP query language over annotated corpora.
- **LancsBox**, **#LancsBox X**: collocation networks, statistics.
- **Python/R** (`nltk`, `spaCy`, `quanteda`) when you need full control.
*Tool features change; check current versions.*

## 3. Concordances (KWIC)
- Search the **lemma** (all forms) when you mean the lexeme; the **word form** when
  form matters. Use POS filters to separate *run* (verb) from *run* (noun).
- Sort by **1R, 2R / 1L, 2L** (words to the right/left) to make patterns pop out.
- Read a **random sample** of lines (e.g. 100–200), not the first page — the first page
  over-represents whichever text comes first.
- Code lines manually for meaning/pattern if needed; report the sample size.

## 4. Frequency
- Report **raw counts** *and* **normalised frequency** (per million words) when
  comparing corpora of different sizes.
- Check **dispersion** (e.g. range: how many texts it occurs in; Juilland's D or DP):
  a word frequent in one text only is not "frequent in the corpus".
- Gotcha: tokenisation differences (hyphens, apostrophes, *don't*) change counts —
  state the tokeniser/tool.

## 5. Collocation statistics — choose deliberately
| Measure | Tends to favour |
|---|---|
| Raw frequency | function words |
| **MI (mutual information)** | rare, exclusive pairs (sensitive to low counts — set a minimum frequency, e.g. ≥5) |
| **t-score** | frequent, less exclusive collocates |
| **Log-likelihood** | statistical significance of association |
| **logDice** | stable across corpus sizes; good for lexicography |
Specify the **window** (e.g. 5L–5R), minimum frequencies and the measure in every
report. Different measures give different "top collocates"; that's normal.

## 6. Keyness (comparing corpora)
- Compare a target corpus to a reference corpus; rank words by log-likelihood or by
  an effect size (log ratio, %DIFF). Report both significance and effect size.
- Large corpora make everything "significant"; effect size decides importance.

## 7. Annotation
- POS-tag and lemmatise with a documented tagger (e.g. CLAWS, TreeTagger, spaCy model
  version). Spot-check accuracy on your data (often lower on informal or historical text).
- For custom annotation, write a coding manual and measure inter-annotator agreement.

## Verify
- [ ] Corpus composition, size and source are stated.
- [ ] Frequencies normalised; dispersion checked.
- [ ] Concordance claims based on a random sample with N stated.
- [ ] Collocation measure, window and thresholds reported.
- [ ] Keyness reported with significance and effect size.
- [ ] Tool names and versions recorded so the analysis can be rerun.
