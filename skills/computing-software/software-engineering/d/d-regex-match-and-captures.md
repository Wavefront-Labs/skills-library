---
id: computing-software.software-engineering.d.d-regex-match-and-captures
name: d-regex-match-and-captures
category: computing-software
field: software-engineering
product: d
tags: [d-regex-match-and-captures, std-regex, regex, matchfirst, matchall, captures, named-groups, regex-flags, pattern-matching, ctregex, d]
level: practitioner
status: docs-checked
description: "Match with std.regex: regex(pattern, flags), matchFirst, matchAll, Captures indexing and named groups, flags g i m s x, and bool tests with !m.empty."
sources:
  - https://dlang.org/phobos/std_regex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# regex, matchFirst, matchAll, captures and flags

Goal: pattern matching with captures.

```d
import std.regex;
auto re = regex(r"(?P<key>\w+)=(?P<val>\d+)", "g");
foreach (m; matchAll("a=1 b=22", re)) writeln(m["key"], " -> ", m["val"]);
auto m = matchFirst("x=9", re);
if (m) writeln(m.pre, m.hit, m.post, m[1]);
```
- Create: `regex(pattern, flags)` (runtime, throws `RegexException` on a bad pattern), `ctRegex!(pattern, flags)` (compile-time, generates native code for faster matching). Flags: `g` global, `i` case insensitive, `m` multi-line (`^` `$` at line separators), `s` single-line (`.` also matches `\n` and `\r`), `x` free-form (whitespace in the pattern ignored).
- Use raw strings (`r"..."` or backticks) to avoid doubling backslashes.
- `matchFirst(s, re)` returns `Captures` (empty if no match; test with `if (m)` or `!m.empty`); `matchAll` returns a lazy range of non-overlapping matches. `match` and `bmatch` exist but the page discourages them: use `matchAll` or `matchFirst`. A string pattern (or several) can be passed instead of a `Regex`.
- `Captures`: `m.hit`, `m.pre`, `m.post`, `m[n]` (0 is the whole match), `m["name"]`, `m.length`, `m.whichPattern` (1-based when a multi-pattern regex is used, 0 for no match). A group that did not take part in the match is null.
- Syntax is an ECMAScript flavour with extensions: classes `\d \w \s`, anchors `^ $ \b`, groups `(...)`, `(?:...)`, named `(?P<name>...)`, lookahead `(?=...)` `(?!...)`, lookbehind `(?<=...)` `(?<!...)`, lazy `*?`, Unicode properties `\p{L}`, `\p{Cyrillic}`.

Gotchas:
- Matches are slices of the original input, so they stay valid only as long as that string does.
- Without anchors `matchFirst` finds the pattern anywhere; add `^...$` for a full match.
- Regex works on characters, not higher-level rules (such as a number bounded to a range): check those in code afterwards.

Verify: unittest asserting captures of a sample line.

## Checked

2026-11-08. Confirmed against the std.regex page: `regex`, `ctRegex`, flags `g i m s x`, `matchFirst`, `matchAll`, `match`/`bmatch` discouraged, `Captures` members (`pre`, `post`, `hit`, indexing, named lookup, `length`, `whichPattern`, bool test, null for unmatched group), syntax table, slicing note, `RegexException`.

Removed because the page did not confirm it: the claim that lambdas hold references to the input, `m.captures.length` (replaced by `m.length`), `\p{Letter}`. Replaced landing-page sources with the std.regex page.

Method: documentation only; no commands were run.
