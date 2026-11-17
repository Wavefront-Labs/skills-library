---
id: computing-software.systems-network-administration.pi-hole.regex-syntax-tutorial
name: regex-syntax-tutorial
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [regex-anchors, regex-groups, regex-character-classes]
level: intro
status: docs-checked
description: "Learn the regex syntax Pi-hole supports: anchors, wildcards, bounds, groups, alternation and character classes, with domain examples."
sources: ["https://docs.pi-hole.net/regex/tutorial/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole regex syntax

All characters match themselves except `.[]{}()\*+?|^$`, which you escape, like `\.` for a literal period.

**Anchors.** Without anchors a match can be partial.

| Pattern | Matches |
| --- | --- |
| `domain` | anywhere in the name |
| `^localhost$` | exactly `localhost` only |
| `^abc` | names starting with `abc` |
| `com$` | names ending in `com` |

**Wildcard and multipliers.** An unescaped `.` is any single character. `?` is zero or one, `*` zero or more, `+` one or more; `{4}`, `{4,}` and `{3,5}` set bounds. `^r-*movie` allows any number of dashes; `^r-+movie` needs at least one.

**Groups and alternation.** `(abc){1,3}` matches one to three copies; `domain(a|b)\.com` matches `domaina.com` and `domainb.com`.

**Character groups.** `[a-z0-9]` and `[^a-z]` (negation). Inside brackets special characters lose their meaning; put `]` first and `-` first or last to include them.

**Classes** must sit inside brackets: `[[:digit:]]`, not `[:digit:]`. FTL matches case-insensitively by default.

**Examples**

```text
^[0-9][^a-z]+\.((com)|(edu))$
^[a-z0-9]+([-]{1}[a-z0-9]+)*\.[a-z]{2,7}$
```

The first blocks all-numeric `.com` or `.edu` names such as `555661.com`; the second matches simple domains without subdomains.

**Checklist**

1. Anchor patterns unless a partial match is wanted.
2. Escape periods.
3. Test before saving.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Regex tutorial (regex/tutorial). Removed the claim that `\d` and `\D` are shortcuts; the tutorial lists only POSIX bracket classes such as `[[:digit:]]`.
Method: documentation only; no commands were run.
