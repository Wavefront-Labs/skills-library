---
id: computing-software.software-engineering.elixir.string-split-replace-trim
name: string-split-replace-trim
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, string-split, string-replace, trim, normalize, downcase, slice, pad, string-module, elixir-strings-text]
level: practitioner
status: docs-checked
description: "Use the String module for Unicode-aware split, replace, trim, case change, slice and padding; most functions work on graphemes."
sources: ["https://hexdocs.pm/elixir/String.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String module: split, replace, trim, normalize

**Goal:** manipulate text without breaking Unicode.

```elixir
String.split("a,b,,c", ",")                 #=> ["a", "b", "", "c"]
String.split("a  b", " ", trim: true) ; String.split(" a b ")   # default splits on whitespace
String.replace("a-b", "-", "_") ; String.replace(s, ~r/\s+/, " ")
String.trim(s) ; String.trim_leading(s, "0") ; String.trim_trailing(s)
String.upcase(s) ; String.capitalize(s) ; String.downcase(s, :ascii)
String.slice("héllo", 1..3) ; String.at(s, 0) ; String.starts_with?(s, ["a", "b"])
String.pad_leading("7", 3, "0") ; String.duplicate("ab", 2) ; String.reverse(s)
String.contains?(s, "x")
String.normalize(s, :nfc)       # Unicode normalisation
```

## Rules
- Functions work on graphemes (`length`, `slice`, `reverse`, `at`); `Kernel.byte_size/1` counts bytes and runs in constant time, while `String.length/1` takes longer as the input grows.
- Interpolation converts non-string values with the `String.Chars` protocol.
- `downcase`/`upcase`/`capitalize` take a mode: `:default`, `:ascii`, `:greek` or `:turkic`; `:ascii` only changes A to Z.
- For large builds use iolists, not repeated `<>` (see the binaries performance skill).

## Self-check
`String.length/1` counts graphemes, not bytes: compare it with `byte_size/1` on a string with accents.

## Checked
2026-11-03: confirmed against the Elixir String docs (`split/3` `trim:` option, whitespace splitting, grapheme-based functions, `byte_size` versus `length`, case modes, `normalize/2`, `pad_leading`, `slice`, `String.Chars` interpolation). Removed: `String.to_integer`, `Integer.parse`, the nil/atom interpolation examples, `inspect/1` advice and the flag emoji example (not on the pages read).
Method: documentation only; no commands were run.
