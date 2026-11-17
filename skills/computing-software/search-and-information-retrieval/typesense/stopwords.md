---
id: computing-software.search-and-information-retrieval.typesense.stopwords
name: stopwords
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [stopwords, stopword-sets, query-time, typesense]
level: practitioner
status: docs-checked
description: "Create, list, fetch and overwrite Typesense stopword sets with optional locale and apply them per search with the stopwords parameter; they are not removed at index time."
sources: ["https://typesense.org/docs/30.2/api/stopwords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stopwords

Stopwords are removed from the search query while searching. They are not dropped during indexing, so documents keep every word.

## Create a set

`PUT /stopwords/<set id>` with a body like `{"stopwords": ["Germany", "France", "Italy", "United States"], "locale": "en"}`; `locale` is optional. The response lists the stored words in lowercase and tokenized: the phrase `United States` becomes the two separate words `states` and `united`.

## Use in a search

Pass the set name in the `stopwords` search parameter, e.g. a multi_search entry with `"collection": "books"`, `"q": "the"`, `"query_by": "title"`, `"stopwords": "stopword_set1"`. Keywords present in the set are removed from `q` before matching.

## Read and update

- `GET /stopwords` lists all sets.
- `GET /stopwords/<set id>` returns one set.
- Updating is an overwrite: repeat the `PUT` with the new array, e.g. `{"stopwords": ["Germany", "France", "Italy"], "locale": "en"}` replaces the earlier content of the set called `countries`.

All calls need the `X-TYPESENSE-API-KEY` header.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Stopwords page (https://typesense.org/docs/30.2/api/stopwords.html). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
