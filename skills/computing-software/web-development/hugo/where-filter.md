---
id: computing-software.web-development.hugo.where-filter
name: where-filter
category: computing-software
field: web-development
product: hugo
tags: [where, collections-where, page-filtering, operators, intersect]
level: practitioner
status: docs-checked
description: "Filter page collections with where: operators, Params versus Page fields, type-mismatch pitfalls, date comparison, nil checks and missing booleans."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/collections/Where.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`collections.Where` (alias `where`) returns a slice filtered to elements matching a condition. Arguments: a slice (page collection or slice of maps), a key, an optional operator and a value. Without an operator, Hugo tests equality.

Operators:

- Equality and comparison: `eq`, `=`, `==`; `ne`, `!=`, `<>`; `ge`, `gt`, `le`, `lt`.
- Membership: `in` and `not in`.
- Overlap: `intersect`, whether two slices share an element; useful for taxonomy terms.
- Pattern: `like`, a regular expression against strings; it returns `false` for non-string fields.

Usage notes:

- Custom fields use `Params`, such as `Params.color`. Reserved fields use `Page` method names, such as `Title`. `Params.title` is deprecated as of v0.169.0.
- Types must match: the string `"123"` does not equal the integer `123`.
- Date comparisons work with predefined dates and unquoted TOML dates. Quoted TOML dates and YAML or JSON dates are strings; range over the slice and convert with `time.AsTime`.
- Compare with `nil` (unquoted) to check whether a parameter is present in front matter: `ne nil` for present, `eq nil` for absent.
- Calls can be nested. Use `site.MainSections` to avoid hardcoding section names: `where site.RegularPages "Section" "in" site.MainSections`. If `mainSections` is not configured, it returns the top-level section with the most pages.
- Pages with an undefined boolean field are excluded from an equality test and included in an inequality test. To exclude them from an inequality test, subtract an `eq nil` slice with `collections.Complement`.

## Checked
Confirmed 2026-11-08 against the Hugo collections.Where page (read in full): operators, Params versus Page fields, type matching, dates, nil, nesting and undefined booleans. Added the `like` non-string behaviour, nil direction, MainSections default and the Complement recipe. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
