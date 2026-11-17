---
id: computing-software.ai-ml-engineering.feature-engineering.text-normalization-and-cleaning
name: text-normalization-and-cleaning
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, text-features, text-normalization, unicode-normalization, text-cleaning, preprocessing, tokenization]
level: practitioner
status: draft
description: "Normalize text for features consistently in training and serving: Unicode NFKC, casing, HTML/URL/number handling, whitespace, and when to leave raw text for transformer tokenizers."
sources:
  - https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
  - https://unicode.org/reports/tr15/
  - https://scikit-learn.org/stable/modules/feature_extraction.html#customizing-the-vectorizer-classes
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text normalization and cleaning

**Goal:** one deterministic normalisation function, applied identically in training and serving, that removes noise without destroying signal.

## A sensible normaliser for sparse/classic features
```python
import re, unicodedata, html
URL = re.compile(r"https?://\S+|www\.\S+"); EMAIL = re.compile(r"\S+@\S+\.\S+")
NUM = re.compile(r"\d+([.,]\d+)?")
def normalize(t: str) -> str:
    t = html.unescape(t)
    t = re.sub(r"<[^>]+>", " ", t)                  # strip HTML tags
    t = unicodedata.normalize("NFKC", t)            # full-width chars, ligatures, compatibility forms
    t = URL.sub(" <url> ", t); t = EMAIL.sub(" <email> ", t)
    t = NUM.sub(" <num> ", t)
    t = t.lower()
    return re.sub(r"\s+", " ", t).strip()
```
- NFKC unifies visually identical characters (e.g. full-width letters, "ﬁ" ligature), which otherwise become different tokens.
- Placeholders for URLs/emails/numbers keep the fact that one was present while removing unique values that would bloat vocabularies and leak IDs.
- Lowercasing helps sparse models; skip it if case carries meaning (code, product codes, "US" vs "us").

## For transformer models: clean less
Pretrained tokenizers expect natural text; lowercasing an uncased-trained model's input is harmless, but stripping punctuation, numbers or casing for cased models loses information. Limit cleaning to: HTML/markup removal, encoding fixes (mojibake via `ftfy`), whitespace normalisation, and PII redaction where required.

## Things to decide deliberately
- **Emoji:** often signal (sentiment); keep or map to names (`emoji.demojize`).
- **Accents:** `strip_accents="unicode"` merges "resume"/"résumé"; harmful for languages where accents distinguish words.
- **Stop words / stemming / lemmatisation:** sometimes help small-data sparse models; rarely help modern models; test.
- **Language:** detect language (fastText lid, `langdetect`) and route or add as a feature for multilingual data.
- **Boilerplate:** remove signatures, quoted reply chains, templates - they leak source/agent identity and dominate features.

## Consistency
Package the normaliser as a function in the model's codebase (or as the vectorizer's `preprocessor=`) so it ships with the pipeline; reimplementing it in another service is a classic train/serve skew source.

## Verify
- [ ] Same normaliser object used by training and serving (unit test on sample strings).
- [ ] Ablation shows each cleaning step helps or is neutral.
- [ ] Boilerplate/template text removed and checked for label leakage.
