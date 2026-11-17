---
id: computing-software.software-engineering.python.regular-expressions-with-re
name: regular-expressions-with-re
category: computing-software
field: software-engineering
product: python
tags: [python, python-stdlib, python-regex, re-module, named-groups, catastrophic-backtracking, verbose-regex]
level: practitioner
status: verified
description: "Use Python's re module well: raw strings, match vs search vs fullmatch, named groups, verbose patterns, flags, substitution callbacks and avoiding catastrophic backtracking."
sources:
  - https://docs.python.org/3/library/re.html
  - https://docs.python.org/3/howto/regex.html
  - https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regular expressions with re

**Goal:** correct, readable patterns that do not hang on hostile input.

## 1. Basics that prevent bugs
```python
import re
PAT = re.compile(r"(?P<key>[A-Za-z_]\w*)\s*=\s*(?P<value>.*)")   # raw string: \w, \s, \d stay intact
m = PAT.fullmatch(line)          # whole string must match; match() anchors only the start; search() anywhere
if m:
    key, value = m["key"], m["value"]
```
- `re.fullmatch` for validation; `re.match(r"\d+", "12abc")` succeeds, which is rarely what a validator wants (write patterns as raw strings: a non-raw `"\d"` is a `SyntaxWarning` on 3.12+).
- `$` matches before a trailing newline; use `\Z` or `fullmatch` when exactness matters.
- Precompile at module level for reuse (re caches ~512 patterns, but compiled objects document intent).

## 2. Verbose patterns
```python
DATE = re.compile(r"""
    (?P<year>\d{4}) -
    (?P<month>0[1-9]|1[0-2]) -
    (?P<day>0[1-9]|[12]\d|3[01])
""", re.VERBOSE)
```
Whitespace and `#` comments are ignored in VERBOSE; escape literal spaces as `\ ` or `[ ]`.

## 3. Finding and replacing
```python
re.findall(r"\d+", s)                 # list of strings (or tuples if groups)
for m in re.finditer(r"\b\w+@\w+\.\w+\b", text): print(m.start(), m.group())
re.sub(r"\s+", " ", s).strip()
re.sub(r"(?P<n>\d+)", lambda m: str(int(m["n"]) * 2), s)    # callback replacement
re.split(r"[;,]\s*", s)
re.escape(user_input)                 # literal search for user-provided text
```
In replacement strings, backslashes are processed: use `\g<name>` and raw strings.

## 4. Flags
`re.IGNORECASE`, `re.MULTILINE` (`^`/`$` per line), `re.DOTALL` (`.` matches newline), `re.ASCII` (`\w`, `\d` ASCII only; by default `\d` matches any Unicode digit like Arabic-Indic). Inline: `(?i)` at the start.

## 5. Catastrophic backtracking (ReDoS)
Nested quantifiers over overlapping alternatives explode on non-matching input: `(a+)+$`, `(\w+\s?)*$`, `(.*,)*`.
- Make alternatives mutually exclusive, avoid nested `+`/`*`.
- 3.11+: possessive quantifiers `a++` and atomic groups `(?>...)` stop backtracking.
- Cap input length before matching untrusted data; for guaranteed linear time use the `google-re2` binding.

## Gotchas
- `.` does not match `\n` without DOTALL.
- `findall` with one group returns the group, not the whole match; use `(?:...)` for grouping without capture.
- Do not parse HTML, JSON or CSV with regex; use the proper parser.
- `str.startswith`, `in`, `str.split` are clearer and faster for literal checks.

## Verify
- Unit tests include matching, non-matching and adversarial long inputs (e.g. 50k chars) with a timeout; the pattern stays sub-millisecond.

## Checked
- Python 3.14.0: `fullmatch`/`match`/`search` behaviour, `$` matching before a trailing newline while `\Z` and `fullmatch` do not, Unicode versus `re.ASCII` digits, cache limit 512, possessive `a++` and atomic groups, `(a+)+$` taking 2.2 s on 26 `a`s plus `b` versus microseconds with a possessive form, VERBOSE comments and escaped spaces, `findall` group behaviour, callback and `\g<name>` substitution, backslash processing in replacement strings, `re.escape`, DOTALL and MULTILINE, `split`; a non-raw `"\d"` string compiles with `SyntaxWarning`. `google-re2` exists on PyPI; it was not run.
