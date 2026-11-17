---
id: computing-software.software-engineering.d.d-regex-replace-split-and-performance
name: d-regex-replace-split-and-performance
category: computing-software
field: software-engineering
product: d
tags: [d-regex-replace-split-and-performance, std-regex, replaceall, replacefirst, regex-split, splitter, ctregex, regex-performance, backreference, substitution, d]
level: practitioner
status: docs-checked
description: "Substitute with replaceAll/replaceFirst (format strings $1 $&, or delegate), split on patterns, and speed up regex via ctRegex and precompiled regex objects."
sources:
  - https://dlang.org/phobos/std_regex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# replace, split, splitter with regex and regex performance

Goal: edit text with patterns.

- `replaceAll(s, regex(r"(\d+)"), "<$1>")`; format references: `$1`..`$99` submatch, `$&` whole match, `` $` `` input before the match, `$'` input after, `$$` literal `$`, `\c` the character c. With no match the input itself is returned.
- Callback: `replaceAll!(m => m.hit.toUpper)(s, re)`; the function receives the `Captures` and returns the replacement. `replaceFirst` replaces only the first match.
- `replaceFirstInto` / `replaceAllInto(sink, ...)` write piece-wise to an output range instead of allocating a new string per call.
- Split: `split(s, regex(r"\s*,\s*"))` is the eager array of slices; `splitter(s, re)` is lazy, and `splitter!(Yes.keepSeparators)` keeps the matches in the result. `std.regex.escaper` lazily escapes literal text for use inside a pattern.
- `replace` is the old API (acts as `replaceAll` with the `g` flag, otherwise `replaceFirst`); prefer the explicit functions.
- Performance: compile a `regex` once and reuse the `Regex` object for frequently used patterns; `ctRegex!"..."` generates native code at compile time for faster matching; plain-string patterns are compiled to bytecode on every call. Matches are slices of the input; only the replace family allocates a new string.

Gotchas:
- The page keeps regex for character-level matching; do higher-level checks (value ranges) in code after matching.
- Replacement format strings use `$1`, not `\1`.

Verify: benchmark the `regex` object and `ctRegex` variants on your own text.

## Checked

2026-11-08. Confirmed against the std.regex page: replace format string table (`$&`, `` $` ``, `$'`, `$$`, `$1`..`$99`, `\c`), `replaceFirst`/`replaceAll` with format and with a function, `replaceFirstInto`/`replaceAllInto`, `replace` as old API, `split`, `splitter` with `Yes.keepSeparators`, `escaper`, `ctRegex`, slicing and allocation notes.

Removed because the page did not confirm it: named `$<key>` references, `\1` backreferences inside patterns, the static `Regex!char` and `__gshared` advice, ctRegex compile-time cost claims, advice to use `find`/`canFind`, the multi-line buffer advice, and the backtracking/Thompson fallback gotcha. The description no longer mentions `$<name>`.

Method: documentation only; no commands were run.
