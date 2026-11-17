---
id: computing-software.search-and-information-retrieval.typesense.basic-stemming
name: basic-stemming
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [stemming, snowball-stemmer, field-locale, typesense]
level: practitioner
status: docs-checked
description: "Turn on Snowball-based stemming per Typesense field with stem true, understand locale-driven language rules, and the risk for brand names and locations."
sources: ["https://typesense.org/docs/30.2/api/stemming.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic stemming

With stemming, searching one grammatical form matches the others: `run` finds `running`, `runs`, `ran`; `walk` finds `walking`, `walked`, `walks`; `company` finds `companies`.

## Enable

Set `"stem": true` on a field when creating the collection: `POST /collections` with `{"name": "companies", "fields": [{"name": "description", "type": "string", "stem": true}]}`.

Basic stemming uses the Snowball stemmer, a rules-based algorithm. The language is taken from the field's `locale`, so `"locale": "fr"` applies French rules.

## Caveat

Rules were designed mostly for common nouns. On brand names, proper nouns, company names or locations they can have unintended effects and reduce relevance. In that case use a stemming dictionary instead, or leave stemming off for those fields.

## Guidance

Start with basic stemming and the right `locale`; use dictionaries only for exceptions and domain-specific variations. Behaviour changes with locale, so set it to match the content's language.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Stemming page (https://typesense.org/docs/30.2/api/stemming.html) and its source markdown. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
