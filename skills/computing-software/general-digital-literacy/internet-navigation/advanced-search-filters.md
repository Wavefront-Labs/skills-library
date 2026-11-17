---
id: computing-software.general-digital-literacy.internet-navigation.advanced-search-filters
name: advanced-search-filters
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, searching, advanced-search, search-operators, date-filter, filetype-search, site-search]
level: intro
status: docs-checked
description: "Narrow Google searches with filters, operators (quotes, minus, site, filetype, before, after) and the Advanced Search page, and avoid common operator mistakes."
sources:
  - https://support.google.com/websearch/answer/2466433
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Date and type filters and advanced search

**Goal:** go from a million vague results to the ten that matter.

## Operators (Google)
No space between the operator and the search term: `site:nytimes.com` works, `site: nytimes.com` does not.

| Operator | Example | Effect |
|---|---|---|
| `"..."` | `"tallest building"` | exact word or phrase |
| `-` | `jaguar speed -car` | leave a word out |
| `site:` | `site:youtube.com cat videos` | results from one site or domain |
| `filetype:` | `photoelectric effect paper filetype:pdf` | one file type |
| `before:` | `astronomy discovery before:2025/11/01` | documents last updated before a year or date |
| `after:` | `avengers endgame after:2020` | documents last updated after a year or date |

Combine `before:` and `after:` for a range: `avengers endgame after:2019-03-01 before:2019-03-05`.

## Built-in filters and Advanced Search
- After a search, filters appear below the search bar (for example Books, Forums, Images, Maps, News, Shopping, Short Videos, Videos, Web). They change with the query; use **All** to see others.
- Advanced Search: enter your query, click **Tools** under the search box (Search Tools on mobile), then **Advanced Search**.

## Strategies
- Start broad, then add one operator at a time.
- For official information, add `site:` with your government's domain.
- For error messages, paste the exact message in quotes.

## Gotchas
- `before:` and `after:` use the date the page was last updated, which may differ from its publication date.
- A mistyped operator is treated as ordinary words.

## Verify
- [ ] The first page of results matches the type, date range and source you wanted.

## Checked
Date: 2026-10-27. Documentation: Google Search Help, "Refine Google searches" (current page). Confirmed: operator list and examples, no-space rule, before/after meaning "last updated", Advanced Search path via Tools, filter names. Removed unconfirmed claims (intitle, OR, wildcard, Bing and DuckDuckGo behaviour, Verbatim and custom date range, usage-rights filters).
Method: documentation only; no commands were run.
