---
id: computing-software.software-engineering.v-lang.v-regex-matching-basics
name: v-regex-matching-basics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-regex-matching-basics, regex-module, regex, regex_opt, matches_string, find, find_all, pattern, regular expression, re, v-lang]
level: practitioner
status: draft
description: "Compile patterns with regex.regex_opt, test with matches_string, find, find_all and understand the supported syntax subset."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiling and matching regular expressions

Goal: match text with V's built-in regex.

- `import regex; re := regex.regex_opt(r'(\d+)-(\d+)')!`.
- Test: `re.matches_string('10-20')`; search: `start, end := re.find('abc 10-20')`; all: `re.find_all(text)` (positions) or `find_all_str(text)` (strings).
- Raw strings `r'...'` avoid double escaping backslashes.
- Flags: case-insensitive `(?i)` is not universal; use `re.flag = regex.f_ic` style flags (confirm names).
- Supports `. * + ? [] [^] ^ $ | () {n,m} \d \w \s`; not a full PCRE (no lookbehind, limited lazy quantifiers; confirm).

Gotchas:
- A bad pattern returns an error from `regex_opt`; handle with `!`.
- For performance critical hot paths, precompile once and reuse (not thread safe if mutated; confirm).

Verify: `assert regex.regex_opt(r'^\d+$')!.matches_string('123')`.
