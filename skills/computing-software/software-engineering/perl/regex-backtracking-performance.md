---
id: computing-software.software-engineering.perl.regex-backtracking-performance
name: regex-backtracking-performance
category: computing-software
field: software-engineering
product: perl
tags: [perl, backtracking, possessive-quantifier, atomic-group, catastrophic-backtracking, re-debug, regex-backtracking-performance]
level: advanced
status: docs-checked
description: "Avoid catastrophic backtracking with anchors, lazy/possessive quantifiers and atomic groups, and inspect with use re 'debug'."
sources: ["https://perldoc.perl.org/perlre", "https://perldoc.perl.org/re"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backtracking, possessive quantifiers and performance

**Goal:** keep regex time bounded on hostile input.

```perl
/((a{0,5}){0,5})*[c]/   # perlre's own example of exponential-time backtracking
/a++b/                  # possessive: gives nothing back
/(?>a+)b/               # independent (atomic) group: possessive is sugar for this
/<.+?>/                 # non-greedy: fewest repetitions
/<[^>]*>/               # negated class, no overlap between the repeated part and what follows
```

## What perlre says
- Backtracking is used by all regular non-possessive quantifiers (`*`, `*?`, `+`, `+?`, `{n,m}`, `{n,m}?`). If the
  start of a pattern succeeds in a way that makes later parts fail, the engine backs up and retries.
- Particularly complicated patterns can take exponential time. Internal optimisations do not always apply, and the
  suggested tool is an independent group, which does not backtrack.
- Possessive forms: `*+`, `++`, `?+`, `{n}+`, `{n,}+`, `{,n}+`, `{n,m}+` "give nothing back". `'aaaa' =~ /a++a/` never
  matches. They are syntactic sugar for `(?>pattern)`. They cannot be combined with the non-greedy `?`.
- Typical use: double-quoted strings, `/"(?:[^"\\]++|\\.)*+"/`; the "unrolled" form
  `/ " [^"\\]*+ (?: \\(?s: .) [^"\\]*+ )*+ " /x` has better performance than looping with alternation inside.
- `(?>pattern)` does not disable backtracking altogether: you can still backtrack past the construct, but not into it.
  `^(?>a*)ab` never matches, whereas `a*ab` does.
- Alternatives are tried left to right and the first that lets the whole expression match wins, so `foo|foot` against
  "barefoot" matches only "foo". Order alternatives with that in mind.
- Quantifiers are greedy by default; `.*` can swallow more than intended, and `?` after a quantifier makes it match
  the minimum.
- `\A` matches only at the beginning of the string.
- Backtracking control verbs such as `(*PRUNE)`, `(*COMMIT)` and `(*FAIL)` exist for finer control.
- Zero-length lookaround assertions do not backtrack to make the tail match.

## Techniques
- Anchor where the problem allows (`\A`) so a match is attempted only at the start.
- Replace `.*` with a negated class such as `[^"]*`.
- Use possessive quantifiers or atomic groups when backtracking can never help.
- Avoid nested quantifiers over overlapping alternatives, as in the perlre exponential example.
- Untrusted, user-supplied patterns are a risk because of the exponential-time warning: do not accept them unbounded.

## Inspecting
```bash
perl -Mre=debug -e '"aaab" =~ /(a+)+b/'
perl -Mre=Debug,EXECUTE -e '...'
```
`use re 'debug'` outputs debugging information during compile and match; `use re qw(Debug ...)` fine-tunes it by group
(compilation, execution, special purposes), with EXECUTE covering the main matching loop. The `re` documentation says
the output format is not a supported API and may change without notice, and that the directives are lexically scoped
but have both compile-time and run-time effects. Benchmark with `Benchmark::cmpthese` on realistic strings.

## Self-check
- [ ] No unbounded nested quantifier over overlapping alternatives remains; a non-matching input of realistic length
      returns promptly.

## Checked
Confirmed 2026-11-08 against perlre (quantifiers, possessive forms, `(?>...)`, backtracking section and its
exponential-time warning, `\A`, alternation order, backtracking verbs) and the `re` pragma page (debug and Debug modes,
EXECUTE, stability note). Removed: the claim that Perl's optimiser looks for a required floating or anchored literal,
the `re::engine::RE2` and alarm-timeout suggestions, the "Complex regular subexpression recursion limit (32766)"
message, and the 30-character millisecond timing target, none of which the cited pages state. perlretut was dropped
from sources because no claim relies on it.
Method: docs-only read of cited pages, 2026-11-08
