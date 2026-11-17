---
id: computing-software.software-engineering.d.d-string-parsing-and-formatting-helpers
name: d-string-parsing-and-formatting-helpers
category: computing-software
field: software-engineering
product: d
tags: [d-string-parsing-and-formatting-helpers, std-string, parse, munch, tokenizer, csvreader, std-csv, uri, base64, split, parsing, std-conv-parse, d]
level: practitioner
status: docs-checked
description: "Parse text with std.conv.parse, munch, splitter, strip, std.csv csvReader, std.uri encode/decode and std.base64, building simple tokenizers."
sources:
  - https://dlang.org/phobos/std_conv.html
  - https://dlang.org/phobos/std_algorithm_searching.html
  - https://dlang.org/phobos/std_csv.html
  - https://dlang.org/phobos/std_uri.html
  - https://dlang.org/phobos/std_base64.html
  - https://dlang.org/phobos/std_digest_sha.html
  - https://dlang.org/phobos/std_digest_md.html
  - https://dlang.org/phobos/std_uuid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String parsing helpers: parse, split by delimiter, csvReader

Goal: parse delimited and numeric text safely.

- `import std.conv : parse, to;` `auto n = s.parse!int;` consumes a prefix of the `ref` string `s`; `parse!(int)(s, radix)` takes a radix; failures throw `ConvException`; `to!int(s)` converts a whole string.
- Tokenize: `s.splitter(' ')` (lazy), `s.split`, `skipOver("key=")`, `findSplit(s, "=")` (std.algorithm.searching).
- CSV: `import std.csv; csvReader!(Tuple!(int, string))(text)`; `CSVException` signals malformed input (see std.csv for header-keyed use).
- Encoding and digests: `std.base64.Base64`, `std.uri.encodeComponent` / `decodeComponent`, `std.digest.sha` and `std.digest.md` (`toHexString`), `std.uuid.randomUUID`.

Gotchas:
- After `parse`, check that the remainder is what you expect (for example `s.empty`).

Verify: unittest parsing "42rest" leaves "rest" and returns 42.

## Checked

2026-11-03. Confirmed against: std.conv, std.algorithm.searching, std.csv, std.uri, std.base64, std.digest.sha, std.digest.md and std.uuid reference pages.

Removed because the pages read did not confirm it: `munch` (not on the pages), `pegged`, `parse!int` sign/stop-at-non-digit claim, CSV memory-reuse claim, `findSplit` triple remark kept only if on page.

Method: documentation only; no commands were run.
