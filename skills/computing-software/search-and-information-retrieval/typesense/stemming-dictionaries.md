---
id: computing-software.search-and-information-retrieval.typesense.stemming-dictionaries
name: stemming-dictionaries
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [stemming-dictionary, jsonl-import, irregular-plurals, typesense]
level: practitioner
status: docs-checked
description: "Import a JSONL word-to-root stemming dictionary into Typesense, attach it with stem_dictionary on a field, and manage dictionaries; precedence over basic stemming."
sources: ["https://typesense.org/docs/30.2/api/stemming.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stemming dictionaries

Dictionaries give exact word to root mappings for irregular forms that algorithmic stemming handles badly.

## Pre-made

An English plurals dictionary is available as `plurals_en_v1.jsonl` from `dl.typesense.org/data/stemming/`; it covers singular and plural variation without algorithmic side effects.

## Create

Write a JSONL file, one object per line: `{"word": "people", "root": "person"}`, `{"word": "children", "root": "child"}`, `{"word": "geese", "root": "goose"}`. Upload with `POST /stemming/dictionaries/import?id=irregular-plurals` using `--data-binary @dictionary.jsonl`. The response echoes `id` and a `words` array of root/word pairs.

## Use

Reference it in the collection schema field: `{"name": "title", "type": "string", "stem_dictionary": "irregular-plurals"}`.

Precedence: `stem: true` alone uses the default stemmer; `stem_dictionary` implies stemming (the schema shows `stem: true` automatically); with both set, the dictionary wins.

## Manage

`GET /stemming/dictionaries/<id>` retrieves one; `GET /stemming/dictionaries` returns `{"dictionaries": ["irregular-plurals", "company-terms"]}`.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Stemming page (https://typesense.org/docs/30.2/api/stemming.html) and its source markdown. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
