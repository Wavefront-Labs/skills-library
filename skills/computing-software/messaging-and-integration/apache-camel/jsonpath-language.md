---
id: computing-software.messaging-and-integration.apache-camel.jsonpath-language
name: jsonpath-language
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, language, jsonpath, json, predicates]
level: practitioner
status: docs-checked
description: "Camel JSONPath language: suppressExceptions, allowSimple, easy predicates, option flags, source from variable or header, resultType and Jackson needs for POJO bodies."
sources:
  - https://camel.apache.org/components/next/languages/jsonpath-language.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSONPath

Works as an Expression or Predicate on JSON. Options (defaults):
- `suppressExceptions` false (true quietly ignores `PathNotFoundException`)
- `allowSimple` true (inline Simple in the path)
- `allowEasyPredicate` true
- `writeAsString` false
- `unpackArray` false
- `option`: comma-separated `DEFAULT_PATH_LEAF_TO_NULL`, `ALWAYS_RETURN_LIST`, `AS_PATH_LIST`, `SUPPRESS_EXCEPTIONS`, `REQUIRE_PROPERTIES`
- `source`: read from `variable:`, `header:` or `property:` instead of the body
- `resultType`, `trim` true, `resolveResource` false

Properties prefix: `camel.language.jsonpath.` (plural `options`).

Syntax:
- Standard: `$.store.book[?(@.price < 20)]`
- Easy: `store.book.price < 20` or `price < 20`; must not start with `$` and allows one operator; the right side may be Simple (`${header.limit}`)
- Inline Simple: `$.store.book[?(@.price < ${header.cheap})]`

Examples: `jsonpath(variable:cars, $.length())` counts array elements; `source="header:books"` reads from a header; with `resultType` `java.util.List` a split of a single match stays a list; a single lookup with `java.util.Map` returns one element, while a filter with zero or several matches returns `null`.

Bodies: File, String, Map, List, POJO (needs Jackson, e.g. `camel-jackson`) and InputStream. Non-Unicode input: pass a String or set header `CamelJsonPathJsonEncoding`.

Verify: a missing `person.middlename` returns null instead of throwing when `suppressExceptions` is true.

## Checked

Method: docs-checked 2026-11-09 against the full camel.apache.org jsonpath-language page (options, syntax, examples, body types, encoding detection).
