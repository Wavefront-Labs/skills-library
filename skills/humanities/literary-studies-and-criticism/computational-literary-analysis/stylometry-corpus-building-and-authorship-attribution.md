---
id: humanities.literary-studies-and-criticism.computational-literary-analysis.stylometry-corpus-building-and-authorship-attribution
name: stylometry-corpus-building-and-authorship-attribution
category: humanities
field: literary-studies-and-criticism
product: computational-literary-analysis
tags: [computational-literary-analysis, digital-humanities, dh, stylometry, authorship-attribution, burrows-delta, delta, most-frequent-words, mfw, function-words, stylo, r, python, faststylometry, cluster-analysis, bootstrap-consensus-tree, pca, distant-reading, moretti, corpus-building, project-gutenberg, hathitrust, ocr-errors, text-cleaning, topic-modelling, mallet, word-embeddings, cross-validation, imposters-method, cultural-analytics, reproducibility]
level: advanced
status: draft
description: "Study literature computationally: build a documented corpus, run Burrows' Delta and stylometric tests (stylo, Python), validate attribution claims, report distant reading honestly."
sources: ["John Burrows, 'Delta: a Measure of Stylistic Difference', Literary and Linguistic Computing 17 (2002)", "Eder, Rybicki & Kestemont, 'Stylometry with R: a package for computational text analysis', R Journal 8 (2016)", "Franco Moretti, Distant Reading (2013)", "Ted Underwood, Distant Horizons (2019)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stylometry, corpus building and authorship attribution

**Goal:** computational results about literature that survive a sceptical reviewer:
a documented corpus, a method suited to the question, validation, and claims no
bigger than the evidence. For general corpus tools (concordances, collocations) see
languages-linguistics.linguistics.corpus-linguistics.concordancing-collocation-and-frequency-analysis.

## 1. Build the corpus deliberately
- **Sampling frame**: what population do the texts stand for? "Novels on Project
  Gutenberg" over-represents canonical and out-of-copyright works; say so, or build from
  bibliographies (HathiTrust, national bibliographies) to reduce the bias.
- **Metadata table** (CSV): id, author, title, first-publication year, edition used,
  source URL, genre, gender/nationality only if relevant and sourced, licence.
- **Clean**: strip Gutenberg headers/footers and licence text, editorial prefaces,
  footnotes, page numbers and running heads; normalise quotes and hyphenation across
  line breaks; record what you removed. OCR text: sample-check error rates (e.g. 5
  random pages per volume) and report them.
- Keep the raw and cleaned versions; version the corpus (a dated release, a checksum).

## 2. Stylometry (who wrote it?)
Authorship signals live in high-frequency **function words** (the, of, and, but), which
writers use unconsciously.
- **Burrows' Delta**: take the n most frequent words (MFW) across the corpus, convert
  each text's relative frequencies to z-scores, and average the absolute differences
  between texts. Smaller = more similar. Minimal Python (tested on synthetic data only):
```python
import re, collections, numpy as np
def tokens(t): return re.findall(r"[a-z']+", t.lower())
def delta(texts, n_mfw=150):                 # texts: {label: full_text}
    counts = {k: collections.Counter(tokens(v)) for k, v in texts.items()}
    mfw = [w for w, _ in sum(counts.values(), collections.Counter()).most_common(n_mfw)]
    rel = np.array([[c[w] / sum(c.values()) for w in mfw] for c in counts.values()])
    z = (rel - rel.mean(0)) / rel.std(0, ddof=1)
    labels = list(texts)
    return {(a, b): np.abs(z[i] - z[j]).mean()
            for i, a in enumerate(labels) for j, b in enumerate(labels) if i < j}
```
- In practice use **stylo** (R): put plain-text files named `author_title.txt` in a
  folder called `corpus`, run `library(stylo); stylo()` and choose MFW ranges, culling,
  distance and cluster/PCA/bootstrap consensus tree. Python alternatives include
  `faststylometry`.
- **Sample size**: attribution gets unreliable on short texts; Eder's work suggests
  several thousand words per sample as a working minimum — test for your corpus.

## 3. Validate before you claim
- **Known-author test**: hold out texts of known authorship and check your setup
  attributes them correctly (cross-validation). Report accuracy.
- Vary MFW (100, 200, ... 1000) and culling; a real signal is stable across settings.
- Use the **imposters method** or similar to test against plausible alternative authors,
  not just the two you suspect.
- Watch confounds: genre, period, translation, editorial normalisation, co-authorship
  and topic all move function-word frequencies.

## 4. Distant reading beyond attribution
Topic models (MALLET, gensim), word embeddings, or classifier-based genre studies:
choose parameters with a stated rationale, read the texts behind the top results, and
publish code and corpus metadata. A topic is a word distribution you have interpreted,
not a theme the machine found.

## Gotchas
- Ranking ≠ proof. Stylometry gives probabilistic evidence to combine with
  documentary evidence.
- Unequal text lengths skew frequencies; sample equal-length chunks.
- Status: draft; the code is a teaching implementation, not a replacement for stylo.

## Verify
- [ ] Corpus has a sampling rationale, metadata table, cleaning log and version.
- [ ] Results hold across several MFW settings and pass a known-author test.
- [ ] Alternative candidate authors and confounds were tested.
- [ ] Top computational results were checked by reading the texts.
- [ ] Code, parameters and corpus metadata are published or archived.
