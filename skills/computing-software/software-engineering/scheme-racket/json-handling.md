---
id: computing-software.software-engineering.scheme-racket.json-handling
name: json-handling
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, json-handling, racket-data-formats]
level: practitioner
status: docs-checked
description: "Parse and emit JSON with the json library: string->jsexpr, jsexpr->string, read-json, write-json and the null mapping."
sources:
  - https://docs.racket-lang.org/json/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON
**Goal:** exchange JSON safely.
```racket
(require json)
(string->jsexpr "{\"a\":[1,2,null]}")   ; '#hasheq((a . (1 2 null)))
(jsexpr->string (hasheq 'a 1))           ; "{\"a\":1}"
(write-json (hasheq 'a '(1 2)) #:indent 2)
```
- A jsexpr is: the null value, boolean, string, an exact integer or finite inexact real, a list of jsexprs, or a hash with symbol keys (`hash/c symbol? jsexpr?`). Vectors, string-keyed hashes and `+inf.0` are not jsexprs.
- JSON `null` maps to the value of the `json-null` parameter, the symbol `'null` by default, compared with `eq?`. Every function takes `#:null` to override it.
- Reading: `read-json` reads one value from a port and leaves the rest, returning eof if only whitespace remains; `string->jsexpr` and `bytes->jsexpr` parse a prefix of the input. Malformed input raises `exn:fail:read`; catch it when handling untrusted data.
- Writing: `write-json`, `jsexpr->string`, `jsexpr->bytes` take `#:encode` (`'control` default, or `'all` to escape non-ASCII as `\uHHHH`) and `#:indent` (`#f` default, `#\tab`, or a number of spaces).
- Object key order is not preserved: hashes are used as the analogue of unordered JSON objects, and duplicate keys keep one pair.

## Self-check
Round-trip a nested value through string and back with `equal?`.

## Checked
2026-11-08. Confirmed against the json library reference: jsexpr definition and examples, `json-null` default `'null` and `eq?` comparison, `#:null`, `#:encode`, `#:indent` arguments and defaults, `read-json` eof and remaining-input behaviour, `exn:fail:read` on malformed input, prefix parsing of `string->jsexpr`, the hash-table design note.
Removed: the xml page as a source (unrelated to JSON).
Method: documentation only; no commands were run.
