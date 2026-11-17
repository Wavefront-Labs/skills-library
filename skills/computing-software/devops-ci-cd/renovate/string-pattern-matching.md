---
id: computing-software.devops-ci-cd.renovate.string-pattern-matching
name: string-pattern-matching
category: computing-software
field: devops-ci-cd
product: renovate
tags: [pattern-matching, glob, regex, renovate]
level: practitioner
status: docs-checked
description: "The glob, regex and negation syntax Renovate accepts in matchers, with the special cases for star and case sensitivity."
sources:
  - https://docs.renovatebot.com/string-pattern-matching/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Many Renovate options accept a list of strings that are treated as patterns. Three forms exist: exact or glob strings, regex strings, and negations.

- A string that is not a regex is a glob, parsed with the `minimatch` library, and always case insensitive (use a regex if you need case sensitivity). `abc123` matches `abc123` or `AbC123`; `abc*` matches `abc` and `abc123` but not `abc/def`; `abc**/*` matches `abc/def` but not `abc`; `abc{/,}**` matches `abc`, `abcd`, `abc/def` and `abc/def/ghi`.
- A regex pattern starts with `/` (or `!/` for negation) and ends with `/` or `/i`. Regex is case sensitive unless you add the `i` flag, so `/^abc/i` matches `ABC` too. Renovate uses the `re2` library, whose syntax differs from full regex (see the `re2` syntax wiki).
- Prefix a pattern with `!` to negate it, for example `!/^a/` (not starting with lower-case `a`) or `!b*`.
- The single value `*` means match everything. It cannot be combined with any other positive or negative pattern, so `["*", "ABC"]` and `["*", "!ABC"]` are invalid; omit the `*` in the negation case.

An array matches when at least one positive pattern matches (if any positive patterns exist) and no negative pattern matches. For `["/^abc/", "!/^abcd/", "!/abce/"]`, `abc` and `abcf` match; `foo`, `abcd`, `abce` and `abcdef` do not. To positively match a string starting with `!`, use a regex such as `["/^!abc$/"]`.

If a matcher has several possible inputs, such as a manager with several categories, it returns true when any one input matches. This limits negation: `"matchCategories": ["!docker"]` is true for a manager in both `java` and `docker`, because `java` satisfies it.

When pasting a regex from regex101 into JSON config, escape backslashes (`\n\s` becomes `\\n\\s`).

## Checked

2026-11-08: read the whole String Pattern Matching page (raw source of docs.renovatebot.com/string-pattern-matching). Confirmed minimatch glob and always case-insensitive globs, regex delimiters and the `i` flag, `re2`, the `*` special case and its invalid combinations, the positive and negative array rules and the multiple-input negation limit, and the regex101 backslash escaping note. Removed the `eslint**` and `@aws-sdk/*` glob examples, the `!/^@types//` example, the "no lookaheads or backreferences" claim and the packageRules example, none of which the page states.
Method: documentation only; no commands were run.
