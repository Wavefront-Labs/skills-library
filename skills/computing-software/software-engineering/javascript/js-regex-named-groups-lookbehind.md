---
id: computing-software.software-engineering.javascript.js-regex-named-groups-lookbehind
name: js-regex-named-groups-lookbehind
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, regex-named-groups, js-regex]
level: advanced
status: docs-checked
description: "Use named capture groups, lookbehind and the g/y flags correctly, including matchAll and replaceAll global-flag checks and lastIndex behaviour."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp
  - https://tc39.es/ecma262/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named groups lookbehind and match APIs

- Named groups: `/(?<year>\d{4})-(?<mo>\d{2})/u.exec(s).groups.year`; the match result has a `groups` property. In replacement strings `$<year>` refers to a named group.
- Lookbehind uses `(?<=...)` and negative lookbehind `(?<!...)`; both are in the ECMAScript pattern grammar.
- `String.prototype.matchAll()` and `replaceAll()` check whether the global flag is set when the first argument is a regex (MDN, "Special handling for regexes"), so pass a `g` regex.
- `lastIndex` is the index at which the next match starts. With `g` or `y`, a successful match sets `lastIndex` to the end of the match, and a failed match resets it to 0 (ECMA-262 RegExpBuiltinExec), so a reused `/a/g` alternates true and false in `.test`. Reset `lastIndex = 0` or create the regex per call.
- Sticky `y`: the next match has to start at `lastIndex`; with `g` it can start there or later (MDN).
- Flags: `s` makes `.` match newlines (dotAll), `d` exposes start and end indices of captures (hasIndices), `u` enables Unicode features such as `\p{L}`, and `v` is the unicodeSets upgrade to `u` (MDN).
- `\w` matches only ASCII letters, digits and `_`; use Unicode property escapes with `u` for other scripts.

Self-check: calling the same `/a/g` `.test("a")` twice returns true then false.

## Checked

Checked 2026-11-08 against the MDN RegExp page (special handling for regexes, flag properties, sticky versus global, Unicode notes) and the ECMAScript specification (RegExpBuiltinExec lastIndex handling, lookbehind grammar, `$<` in replacement templates, the `groups` result property). Removed: the claim that `matchAll` returns an iterator (not stated on the cited pages) and the "newer" qualifier on the `v` flag.
Method: docs-only read of cited pages, 2026-11-08
