---
id: computing-software.software-engineering.ocaml.string-module-and-utf-8
name: string-module-and-utf-8
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, string-module-utf8, string-split-on-char, utf-8, uchar, string-index]
level: practitioner
status: docs-checked
description: "Split, trim, search and decode strings with String, String.Ascii-style helpers and Uchar/UTF-8 decoders; know strings are bytes."
sources: ["https://ocaml.org/manual/api/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings and UTF-8

```ocaml
String.split_on_char ',' "a,b,c"           String.trim "  x "
String.concat ", " ["a"; "b"]              String.sub "hello" 1 3
String.index_opt "hello" 'l'               String.starts_with ~prefix:"he" "hello"   (* 4.13+ *)
String.fold_left (fun n c -> if c = 'a' then n+1 else n) 0 "banana"   (* 4.13+ *)
let d = String.get_utf_8_uchar "é" 0       (* 4.14+ : Uchar.utf_decode *)
let () = if Uchar.utf_decode_is_valid d then print_int (Uchar.to_int (Uchar.utf_decode_uchar d))
```

## Notes
- OCaml strings are byte sequences; `String.length "é"` is 2 for UTF-8 source. Indexing is by byte.
- `String.sub` raises `Invalid_argument` on bad ranges.
- Case conversion `String.uppercase_ascii` handles ASCII only.
- `Buffer.add_utf_8_uchar`, `Bytes.set_utf_8_uchar` encode.
- `String.cat` (4.13+) concatenates two strings.

## Self-check
- [ ] `String.length` is never used as a character count for non-ASCII input.

## Checked
2026-11-02. Confirmed: String functions and since-versions (string.mli), UTF-8 decoding API, ASCII-only case mapping. Removed: Unicode packages and the substring-search claim.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
