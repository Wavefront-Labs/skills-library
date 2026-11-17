---
id: computing-software.systems-network-administration.paperless-ngx.search-syntax
name: search-syntax
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, search, full-text-search, tantivy, query-syntax, wildcards]
level: practitioner
status: docs-checked
description: "Write Paperless-ngx full-text queries: boolean operators, field prefixes, wildcards, date ranges, notes and custom fields."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/migration-v3/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search syntax

By default only documents containing all typed words are returned. Matching is word-order-independent, accent-insensitive, and separator-agnostic (`1312` finds `A-1312/B`).

## Operators
`AND`, `OR` and `NOT` must be capitals; parentheses group terms and quotes match an exact phrase. Terms with no operator are combined with `AND`. A leading `-` does not exclude: `invoice -secret` finds documents containing both words, so write `invoice NOT secret`.

## Fields
`title`, `content`, `correspondent`, `document_type` (or `type`), `storage_path` (or `path`), `tag`, `original_filename`, `asn`, `page_count`, `num_notes`, `checksum`, `created`, `added`, `modified`.
```
type:invoice tag:unpaid
correspondent:"acme corp"
tag:bills,unpaid
asn:[50 to 150]
checksum:9f86d081*
```
- A field applies only to the word right after it, so quote multi-word values.
- A comma-separated `tag` list requires every listed tag.
- `asn`, `page_count` and `num_notes` are numbers: ranges work, wildcards do not.
- `checksum` only matches the complete lowercase checksum unless you add a wildcard.
- An unknown field name is searched as ordinary text.

## Wildcards
`*` matches any number of characters, `?` exactly one. `[...]` and `[!...]` match one character in or not in a set or range (`20[12]?`). Brackets only act as a wildcard when the value also contains `*` or `?`; a single-character range like `title:200[1-9]` is rejected with an error, so use `title:200[1-9]*`.

When a stemmer is available for the search language, words are indexed by stem: `copy*` also finds "copies", but `universit*` misses "university" (stored as `univers`), so try a shorter prefix such as `univers*`.

## Dates
Whole-period keywords work with or without quotes: `today`, `yesterday`, `tomorrow`, `previous week`, `this month`, `previous month`, `previous quarter`, `this year`, `previous year`. Also `created:2005`, `created:2005-01`, `created:2005-03-04`, `added:january`, `added:"next monday"` (quotes required), `added:"12 december 2019"`.

Ranges: `created:[2005 to 2009]`, `added:[-1 week to now]`. Bounds need no quotes; if you quote one, use single quotes (`added:['-1 week' to now]`), because double quotes are rejected. `now`, `noon`, `midnight` and relative times like `-1 week` only work as range bounds: `added:"-1 week"` finds nothing. A bare weekday and spellings like `3 days ago` or `this week` are not supported. Custom date fields do not support relative date syntax.

## Notes and custom fields
A plain search does not look at them. Use `notes.user:alice`, `notes.note:reminder` (bare `notes:` is shorthand for `notes.note:`), `custom_fields.value:policy` and `custom_fields.name:"Contract Number"` (bare `custom_fields:` is shorthand for `custom_fields.value:`). Combine name and value to match a specific field.

## v3 changes
Old `note:query` becomes `notes.note:query` and `custom_field:query` becomes `custom_fields.value:query`. Saved views with explicit `note:` or `custom_field:` prefixes are migrated automatically; unqualified queries are not, so use for example `invoice OR notes.note:invoice OR custom_fields.value:invoice`.

`PAPERLESS_ADVANCED_FUZZY_SEARCH_THRESHOLD` (0.5 is a reasonable starting point; unset by default, which disables it) applies approximate matching alongside exact matching, with fuzzy results ranked below exact ones. Single-character words are not fuzzy-matched.

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the whole Searching section of usage (global search through barcodes), the Search Index section of migration-v3, and the PAPERLESS_ADVANCED_FUZZY_SEARCH_THRESHOLD and PAPERLESS_SEARCH_LANGUAGE entries of configuration.
Corrections: field list now uses the page's full names with aliases; the stemming wildcard note was reworded to the page's conditions (a stemmer must be available); the date section was rewritten to the page's supported forms and unsupported spellings; the claim that `tag:bills,unpaid` means "both tags" is kept as the page's "requires every listed tag"; added the wildcard-in-brackets error rule. Barcode search syntax exists on the page but is not covered here.
Method: documentation only; no commands were run.
