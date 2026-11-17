---
id: computing-software.systems-network-administration.paperless-ngx.matching-algorithms
name: matching-algorithms
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, matching-algorithm, tags, correspondents, regular-expression, fuzzy-match]
level: practitioner
status: docs-checked
description: "Pick the right matching algorithm (any, all, exact, regex, fuzzy, auto) for tags, correspondents, document types and storage paths."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching algorithms

Tags, correspondents, document types and storage paths each have a `match` text and a `matching_algorithm`. At consumption Paperless tests every rule against the document text and assigns those that match.

## Algorithms
- None: no matching.
- Any: any word in the match text occurs. `Bank1 Bank2` matches either.
- All: every word occurs, in any order.
- Exact: the text occurs exactly as given, order preserved.
- Regular expression: the match is a regex searched in the content.
- Fuzzy: partial ratio matching of the text inside the document.
- Auto: learned from your existing assignments; needs no match text. The Automatic matching notes on the advanced usage page cover how it is trained.

## Multi-word terms
With Any or All, use double quotes: `"Bank of America" BofA` matches either phrase, but not "Bank of South America".

## Example
A tag `Home Utility` with match `bc hydro` and algorithm Exact is applied to any document containing that text.

## Applying to old documents
Matching is applied to newly consumed documents. After changing or adding rules, run the retagger to apply them to existing ones:
```bash
document_retagger -T -c -t -s
```
- `-i` limits it to inbox documents; `--id-range 1 100` tests a subset.
- If several correspondents or types match, nothing is assigned unless `--use-first` is given.
- `-f` overwrites existing values; for tags it also removes tags that no longer match.
- With none of `-c`, `-T`, `-t`, `-s`, it does nothing.

Regex matching has a timeout, `PAPERLESS_MATCH_REGEX_TIMEOUT_SECONDS`, default 0.1 seconds.

## Checked
2026-11-04. Compared with Matching tags, correspondents, document types, and storage paths in advanced usage, Document retagger in administration, and PAPERLESS_MATCH_REGEX_TIMEOUT_SECONDS in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: every algorithm, quoting rule and example, Home Utility example, retagger flags and behaviour, regex timeout default of 0.1 seconds. Replaced the cross-reference to an auto-classifier skill with the advanced usage notes and reworded the new-documents sentence.

Method: documentation only; no commands were run.
