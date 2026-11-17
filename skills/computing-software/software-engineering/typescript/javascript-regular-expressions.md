---
id: computing-software.software-engineering.typescript.javascript-regular-expressions
name: javascript-regular-expressions
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, js-regex, named-groups, regex-flags, matchall, redos, unicode-regex]
level: practitioner
status: docs-checked
description: "Use JavaScript regex effectively: flags (g, y, u, v, s, d), named groups, lookbehind, matchAll and replace callbacks, the lastIndex trap, escaping input and avoiding ReDoS."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/unicodeSets
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/escape
  - https://github.com/mdn/browser-compat-data/blob/main/javascript/builtins/RegExp.json
  - https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JavaScript regular expressions

**Goal:** readable, correct regexes that don't hang the event loop.

## Flags
| Flag | Effect |
|---|---|
| `g` | global: all matches (`matchAll`, `replaceAll`, stateful `exec`) |
| `i` / `m` | case-insensitive / `^ $` match at line breaks |
| `s` | dotAll: `.` matches newlines |
| `u` | Unicode code points, `\p{...}` property escapes, stricter syntax |
| `v` | superset of `u`: set operations (intersection, union, subtraction) in character classes |
| `y` | sticky: match only at `lastIndex` (tokenizers) |
| `d` | indices of groups (`match.indices`) |

## Named groups and lookarounds
```js
const re = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/u;
const { year, month } = "2026-10-18".match(re).groups;
"2026-10-18".replace(re, "$<day>/$<month>/$<year>");
/(?<=\$)\d+(\.\d\d)?/.exec("cost: $42.50")[0];      // lookbehind: "42.50"
/^(?!.*password).+$/i.test(input);                   // negative lookahead
```

## Iterating matches
```js
for (const m of text.matchAll(/#(\w+)/g)) console.log(m[1], m.index);   // requires g
text.replace(/\b(\w)(\w*)/g, (_, a, rest) => a.toUpperCase() + rest);
```

## The lastIndex trap
A `g` or `y` regex is stateful: `re.test(s)` advances `re.lastIndex`, so calling it repeatedly
on different strings alternates true/false.
```js
const re = /a/g; re.test("a"); re.test("a");   // true, false
```
Don't use `g` with `test()`; or create the regex per call.

## Escaping user input
```js
const safe = RegExp.escape(userText);        // ES2025 (Node 24+); otherwise:
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
new RegExp(`\\b${esc(term)}\\b`, "i");
```

## Unicode
`/^.$/.test("😀")` is false without `u` (two UTF-16 units). Letters in any script:
`/\p{L}+/u`. Use `u` (or `v`) by default.

## ReDoS
Backtracking engines go exponential on nested quantifiers with overlapping alternatives:
`/^(a+)+$/`, `/([a-zA-Z]+)*$/`, `/(a|aa)+$/` against a long non-matching input can block a Node
process. Defences: avoid nested quantifiers, anchor patterns, cap input length
before matching, and keep untrusted patterns away from the backtracking engine.

## Verify
- [ ] Regexes applied to user input are linted for catastrophic backtracking and inputs length-capped.
- [ ] No `g`-flag regex reused with `.test()`.

## Checked
Checked 2026-10-25 against the MDN content repository, MDN browser-compat-data (RegExp.json) and the OWASP ReDoS page. Confirmed: flags d, g, i, m, s, u, v, y and the stateful `lastIndex`; named groups and `matchAll`; `RegExp.escape` shipping in Node 24; `v` flag adding set operations; the OWASP evil patterns `(a+)+$`, `([a-zA-Z]+)*$` and `(a|aa)+$`. Removed the unconfirmed set-subtraction example, emoji property escape, named ReDoS linters and RE2 recommendation.
Method: documentation only; no commands were run.
