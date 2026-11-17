---
id: computing-software.systems-network-administration.pi-hole.regex-approximate-matching
name: regex-approximate-matching
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [agrep-regex, fuzzy-domain-match, regex-backreference]
level: sme
status: docs-checked
description: "Use agrep-style approximate matching ({+x-y#z~n}) and back-references in Pi-hole regexes to catch near-miss domains."
sources: ["https://docs.pi-hole.net/regex/approximate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Approximate regex matching

Approximate matching, like `agrep`, tolerates a set number of errors in a subpattern. Append settings in braces:

| Setting | Meaning | Example |
| --- | --- | --- |
| `{+x}` | accept x insertions | `^doubleclick\.(nt){+1}$` matches `doubleclick.net` |
| `{-x}` | accept x deletions | `^doubleclick\.(neet){-1}$` matches `doubleclick.net` |
| `{#x}` | accept x substitutions | `(foobar){#2}` matches `oobargoobaploowap` |
| `{~n}` | cap total errors | `(foobar){+2#2~3}` |

Combinations such as `{+2-5#6}` are allowed; `~7` limits total attempted operations to 7. A substitution needs a replaced character, so `doubleclick.nt` is not matched by `^doubleclick\.n(tt){#1}$` but is matched by `{+1-1}`.

**Cost equation** (advanced, only when needed): `{ 2i + 1d + 2s < 5 }` weights insertions, deletions and substitutions and caps the total cost at 5. A lone cost equation needs a space after the opening `{`.

**Back-references.** `\1` to `\9` match the same text as the nth parenthesised group; FTL adds them to ERE in BRE style:

```text
(1234|4321)\.(foo)\.(dog)--\1
```

matches `1234.foo.dog--1234` but not `1234.foo.dog--4321`.

**Checklist**

1. Test with `pihole-FTL regex-test`.
2. The page says approximate matching is "just an idea" and that it remains to be seen whether it is useful.

## Checked

2026-11-03. Read the Approximate matching page (`+`, `-`, `#`, `~`, combinations such as `{+2-5#6~7}`, the cost equation and the space after `{`) and the Pi-hole regex extensions page (back-references `\1`, the `1234|4321` example). Removed the advice to start exact and add tolerance sparingly.

Method: documentation only; no commands were run.
