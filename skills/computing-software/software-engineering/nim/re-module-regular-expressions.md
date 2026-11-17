---
id: computing-software.software-engineering.nim.re-module-regular-expressions
name: re-module-regular-expressions
category: computing-software
field: software-engineering
product: nim
tags: [re-module-regular-expressions, regex-and-pegs, re, regex, pcre, match, find, findall, replace, captures, nim-regex, nim]
level: practitioner
status: docs-checked
description: "Match, search, capture and replace with std/re (PCRE) using =~, find, findAll, replace and split."
sources:
  - https://nim-lang.org/docs/re.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regular expressions with std/re and nim-regex

Goal: apply regexes safely.

- `import std/re`: `if "x42" =~ re"([a-z])(\d+)": echo matches[0], matches[1]`; `find(s, re"\d+")`, `findAll`, `match`, `replace(s, re"\s+", " ")`, `split`, `contains`, `startsWith`.
- Pattern syntax is PCRE; `re"..."` is shorthand for `re(r"...")` and compiles the regex, which is expensive, so avoid it in loops; `re(pattern, flags={reIgnoreCase})` for dynamic patterns.
- The module wraps the PCRE library (the page carries the PCRE licence and syntax reference); the `regex` and `tinyre` nimble packages are named there as alternatives.
- Reuse compiled `Regex` objects; compiling in a loop is slow.

Gotchas:
- `=~` declares an implicit `matches` array usable in the scope of the `=~` call.
- `start` offsets the scan, but returned positions are relative to the whole input string.

Verify: capturing groups returns "x" and "42" above.

## Checked

2026-11-03. Confirmed against the re page: `=~` with the implicit matches array, find, findAll, match, replace, split, contains, startsWith, re(s, flags), reIgnoreCase, `re"..."` as short form of `re(r"...")`, compile cost warning, PCRE basis, start-offset note, regex and tinyre named as alternatives. Removed: libpcre/pcre64.dll file names, static-build claim, nim-regex feature and linear-time claims, catastrophic backtracking claim (none on the page).

Method: documentation only; no commands were run.
