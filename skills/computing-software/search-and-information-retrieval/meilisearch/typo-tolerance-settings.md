---
id: computing-software.search-and-information-retrieval.meilisearch.typo-tolerance-settings
name: typo-tolerance-settings
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [typo-tolerance, min-word-size-for-typos, disable-on-words, meilisearch]
level: advanced
status: docs-checked
description: "Tune Meilisearch typo tolerance: enabled, minWordSizeForTypos, disableOnWords, disableOnAttributes, disableOnNumbers, and how the Levenshtein limits work."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/relevancy/typo_tolerance_settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typo tolerance settings

Configured per index with the typo-tolerance settings endpoint (PATCH `/indexes/<index>/settings/typo-tolerance`).

## Keys

- `enabled`: on by default. Turn off for massive or multilingual data where false positives hurt; otherwise keep it on. Turning it off also effectively disables the `typo` ranking rule, since every hit has 0 typos.
- `minWordSizeForTypos`: defaults to one typo for terms of 5+ characters and two typos for 9+. Override with `oneTypo` and `twoTypos`; constraint `0 <= oneTypo <= twoTypos <= 255`. Recommended ranges: `oneTypo` 2 to 8, `twoTypos` 4 to 14.
- `disableOnWords`: case-insensitive list of query terms exempt from typo tolerance, e.g. `shrek`.
- `disableOnAttributes`: attributes whose matches tolerate no typos, e.g. `title`.
- `disableOnNumbers`: `true` makes numbers match exactly (stops `2024` matching `2025` or `2004`) and may improve indexing performance.

## How matching works

A prefix Levenshtein algorithm applies per word: 1 to 4 characters allow no typo, 5 to 8 allow one, over 8 allow two. A maximum of two typos is ever allowed. A typo on the first character counts as two typos, so `caturday` does not match `saturday`. Space-separated terms may be concatenated and counted as one typo (`any way` matches `anyway`).

The `typo` ranking rule orders results by increasing typo count; tolerance decides what matches, the rule decides how matches are ordered.

## Checked

2026-11-03. Confirmed claim by claim against the Typo tolerance settings page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
