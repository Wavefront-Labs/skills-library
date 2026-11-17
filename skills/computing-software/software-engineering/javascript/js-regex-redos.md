---
id: computing-software.software-engineering.javascript.js-regex-redos
name: js-regex-redos
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, redos, js-regex]
level: advanced
status: docs-checked
description: "Recognise regexes with nested repetition or overlapping alternation that backtrack exponentially on crafted input (OWASP ReDoS), and how to avoid them."
sources:
  - https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Catastrophic backtracking (ReDoS)

- Cause (OWASP): many regex engines use a backtracking algorithm; when a match fails the engine returns to earlier positions and tries other paths. For `^(a+)+$` OWASP counts 16 paths for `aaaaX` and 65536 for `aaaaaaaaaaaaaaaaX`, doubling for each extra `a`.
- OWASP's "evil regex" shape: grouping with repetition, and inside the repeated group either repetition or alternation with overlapping branches. Its examples are `(a+)+$`, `([a-zA-Z]+)*$`, `(a|aa)+$` and `(a|a?)+$`, all slow on `aaaaaaaaaaaaaaaaaaaaaaaa!`.
- Symptom: a program using such a regex can hang for a very long time on crafted input. JavaScript runs your code on one thread, so a hung regex blocks everything else in that thread.
- Regex injection: if user input is used as the pattern, an attacker can supply an evil regex. OWASP's example uses a username as the pattern against a password.
- Avoid building a pattern from user input. If you must, escape it first: MDN describes `RegExp.escape()` as escaping any potential regex syntax characters so the result can be used as a literal pattern for the `RegExp()` constructor.
- Review each repeated group: make alternatives mutually exclusive, avoid a quantifier on a group that already contains a quantifier, and test against long near-miss inputs.

Self-check: time the pattern against inputs such as `"a".repeat(n) + "!"` for growing n; time that roughly doubles per extra character means the pattern is vulnerable.

## Checked

Checked 2026-11-08 against the OWASP ReDoS page (backtracking explanation, path counts, evil regex description and examples, regex injection example) and the MDN RegExp page (`RegExp.escape()` description). Removed: the claims about RE2 bindings, `safe-regex` and `recheck` tools, input-length caps and `{1,64}` bounds (not on the cited pages), and the extra danger shapes `(.*)*` and `^(\w+\s?)*$`.
Method: docs-only read of cited pages, 2026-11-08
