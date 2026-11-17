---
id: computing-software.search-and-information-retrieval.meilisearch.search-snippets-highlight-and-crop
name: search-snippets-highlight-and-crop
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [search-snippets, attributes-to-crop, crop-length, meilisearch]
level: practitioner
status: docs-checked
description: "Build result snippets in Meilisearch with attributesToHighlight, highlight tags, attributesToCrop, cropLength and cropMarker, read from the _formatted object."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/getting_started/search_with_snippets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snippets: highlighting and cropping

Two search parameters shape what users see of a hit. Results arrive in a `_formatted` object inside each hit.

## Highlighting

`attributesToHighlight` lists fields whose matched terms get wrapped in tags; `["*"]` means all displayed attributes. The default tag is `<em>`. Replace it with `highlightPreTag` and `highlightPostTag`, for example `<mark>` and `</mark>`.

## Cropping

`attributesToCrop` trims long fields to the area around the match.

| Parameter | Default | Meaning |
|---|---|---|
| `attributesToCrop` | `null` | fields to crop, `["*"]` for all displayed |
| `cropLength` | `10` | maximum words in cropped text |
| `cropMarker` | `"..."` | text placed at a truncated start or end |

Per-field length: append `:length`, as in `"attributesToCrop": ["overview:30", "tagline:10"]`.

## Combining

Request both for short, emphasised snippets, for instance `attributesToHighlight: ["title","overview"]`, `attributesToCrop: ["overview"]`, `cropLength: 30`. A cropped field is automatically highlighted if it is in `attributesToHighlight` or that list is `["*"]`.

## Checked

2026-11-03. Confirmed claim by claim against the Search with snippets page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
