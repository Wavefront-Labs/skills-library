---
id: computing-software.search-and-information-retrieval.qdrant.text-matching-phrase
name: text-matching-phrase
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [text-index, phrase, tokenizer, stemmer, stopwords, filt-text]
level: advanced
status: docs-checked
description: "Filter on words and phrases in Qdrant with a text index: tokenizer, lowercasing, stemmer, stopwords, text, text_any and phrase conditions."
sources:
  - https://qdrant.tech/documentation/search/text-search/text-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

To filter on words inside a string field, first create a full-text (`text`) payload index for it. Compared with keyword filtering (exact, case-sensitive, whole string), text filtering is case-insensitive and matches individual words.

```json
{ "field_name": "description",
  "field_schema": { "type": "text", "ascii_folding": true, "phrase_matching": true } }
```

At index time (and the same steps are applied to the filter string at query time):

- The string is split into tokens; the default `word` tokenizer splits on word boundaries and discards spaces, punctuation and special characters.
- Tokens are lowercased by default, which makes filters case-insensitive.
- A stemmer is optional and disabled by default; it is language-specific, so configure a language when enabling it (then "running" also matches "run").
- Stopword removal is optional, disabled by default and language-specific; you can pick languages and/or give a custom list.

Filter conditions on a field with a text index:

- `match` with `text`: all terms must appear (logical AND, any order).
- `match` with `text_any`: any of the terms may appear (logical OR).
- `match` with `phrase`: the words must appear in exactly that order with no other words between them. It needs the index created with `phrase_matching: true`.

```json
{ "must": [ { "key": "description", "match": { "phrase": "fast shipping" } } ] }
```

For the query "Space War", the docs compare four methods: `text_any` (space OR war) also matches "War of the Worlds"; `text` (space AND war) matches "War in Space" but not "War of the Worlds"; `phrase` matches "The Space War" but not "War in Space"; keyword matches only the exact string "Space War".

For ranked keyword retrieval rather than filtering, use a full-text index with scoring and BM25, covered separately. Filtering narrows candidates, while scoring orders them.

## Checked

2026-11-08. Confirmed against the Text Filtering page (text-processing section, text/text_any/phrase sections and comparison table; the index-creation example with `ascii_folding` and `phrase_matching`). Page read by section; client-language tabs and the cloud-inference examples skipped. Removed unconfirmed claims: that text filtering without an index falls back to a slow scan, and the `lowercase`/`tokenizer` values shown in the example schema (kept to documented defaults in prose).
Method: documentation only; no commands were run.
