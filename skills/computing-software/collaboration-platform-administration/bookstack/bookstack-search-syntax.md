---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-search-syntax
name: bookstack-search-syntax
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, search, search-operators, tag-search, filters, exact-phrase, content-search]
level: intro
status: docs-checked
description: "Search BookStack with exact phrases, tag expressions, negation and filters such as type, created_by, updated_after, in_name and viewed_by_me, plus the term limits."
sources: ["https://www.bookstackapp.com/docs/user/searching/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack search syntax

- Terms: `london meeting`; exact phrase: `"london meeting"`.
- Tags: `[location]`, `[=london]`, `[attendees>5]`. Value operators: `=`, `!=`, `<`, `>`, `<=`, `>=`, `like` (`%` wildcard).
- Filters: `{name}` or `{name:value}`. Negate exact, tag or filter terms with a leading `-`, e.g. `-[location]`.

Filters:
- Dates (YYYY-MM-DD): `updated_after`, `updated_before`, `created_after`, `created_before`.
- Users: `updated_by`, `created_by`, `owned_by` with a user slug or `me`.
- Content: `in_name`, `in_body`.
- Options: `is_restricted`, `is_template`, `viewed_by_me`, `not_viewed_by_me`.
- Type: `{type:page|chapter|book}`.
- Sort: `{sort_by:last_commented}` is the only supported sort.

Examples:
```
"my cat" {viewed_by_me} {updated_after:2017-01-24}
textbook discussion -"draft" [meeting] {type:page} {created_by:me}
{type:book|chapter} {created_by:me} {created_after:2016-08-12} {created_before:2017-02-18}
```
Per-search limits: normal 5, exact 2, tag 4, filter 5, doubled for logged-in users.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) user/searching/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
