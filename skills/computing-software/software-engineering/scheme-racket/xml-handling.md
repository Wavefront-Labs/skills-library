---
id: computing-software.software-engineering.scheme-racket.xml-handling
name: xml-handling
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, xml-handling]
level: practitioner
status: docs-checked
description: "Read XML with read-xml and convert via xml->xexpr; produce markup with xexpr->string."
sources:
  - https://docs.racket-lang.org/xml/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XML and X-expressions
**Goal:** work with XML as x-expressions.
```racket
(require xml)
(xml->xexpr (document-element (read-xml (open-input-string "<a x='1'><b/></a>"))))
(xexpr->string '(p ((class "c")) "hi"))
(string->xexpr "<doc><bold>hi</bold> there!</doc>")
```
- X-expression: `(tag ((attr "v") ...) child ...)`; attribute names are symbols and values strings; the attribute list may be omitted when writing. A string child is escaped as needed when written.
- `read-xml` reads one document (exactly one root element, otherwise `exn:xml`); `read-xml/element` reads a single element and leaves later data in the port.
- Output: `write-xml` and `display-xml` (the latter takes `#:indentation` of `'none`, `'classic` (default), `'peek` or `'scan`); only `'none` is guaranteed accurate when whitespace matters. `write-xexpr` writes an x-expression directly.
- Limits stated by the docs: no DTD processing or validation, no expansion of user-defined entities, no namespace interpretation.
- `validate-xexpr` raises `exn:invalid-xexpr` for a bad x-expression; `xexpr?` tests.
- Parameters: `read-comments` (default `#f`, comments dropped), `collapse-whitespace` (default `#f`), `empty-tag-shorthand`, `current-unescaped-tags`.

## Self-check
`(xml->xexpr (document-element (read-xml (open-input-string "<doc><bold>hi</bold> there!</doc>"))))` gives `'(doc () (bold () "hi") " there!")`.

## Checked
2026-11-08. Confirmed against the xml library reference: `read-xml` and its example result, `read-xml/element`, `exn:xml`, `display-xml` indentation modes and default, x-expression grammar, `write-xexpr`, `validate-xexpr`, parameter names and defaults, and the statement on DTDs, entities and namespaces.
Removed: the json page as a source, the claim that external entities are not processed (the docs say DTD processing and user-defined entity expansion are absent, not an entity-security statement), and the unverified `"<b>x</b>"` output claim.
Method: documentation only; no commands were run.
