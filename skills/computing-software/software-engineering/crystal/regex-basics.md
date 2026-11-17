---
id: computing-software.software-engineering.crystal.regex-basics
name: regex-basics
category: computing-software
field: software-engineering
product: crystal
tags: [regex-basics, regex, pcre2, regex-literal, match, scan, gsub, match-question, flags, regexp, crystal]
level: practitioner
status: docs-checked
description: "Use PCRE2 regex literals with flags i m x, match, =~, match?, scan, gsub with blocks and named captures."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex literals and matching

Goal: match text.

- Literal `/ab+c/i`; flags `i` ignore case, `m` multiline (`^`/`$` match at line breaks and `.` matches newline), `x` extended (ignore whitespace and `#` comments); build dynamically with `Regex.new("a#{Regex.escape(s)}")`.
- Test: `str.matches?(/re/)` or `/re/.matches?(str)` (no capture), `str =~ /re/` returns index or nil and sets `$~`, `$1`.
- Extract: `str.match(/(\d+)-(\d+)/)` gives `Regex::MatchData?`; `m[1]`, `m.pre_match`, `m.post_match`, `m.begin(0)`.
- All: `str.scan(/\d+/)` returns an Array(MatchData) (use `.map(&.[0])`); `str.gsub(/\d/) { |d| ... }`, `sub`, `split(/,\s*/)`.
- Engine: PCRE2 with JIT (PCRE before Crystal 1.8); the PCRE2 pattern syntax applies, and strings and regexes are UTF-8 only.

Gotchas:
- `$~` is per-method frame; capture to a local immediately.
- Catastrophic backtracking is possible; avoid nested quantifiers on untrusted input.
- Interpolation `/#{x}/` compiles at runtime (cost, and injection risk).

Verify: `"a1b22".scan(/\d+/).map(&.[0])` gives ["1", "22"].

## Checked

Date 2026-11-03. Confirmed in the Regex source: PCRE2 with JIT, PCRE before Crystal 1.8, flags i, m and x with MULTILINE equal to PCRE multiline plus dotall, Regex.escape, Regex#match, matches?, String#match, match!, scan returning Array(Regex::MatchData), sub, gsub with blocks, split with a Regex, =~ returning the index and setting $~, and $1/$1? access. Removed the unverified lookaround and unicode-class list.

Method: documentation only; no commands were run.
