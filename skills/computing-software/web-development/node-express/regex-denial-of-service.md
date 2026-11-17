---
id: computing-software.web-development.node-express.regex-denial-of-service
name: regex-denial-of-service
category: computing-software
field: web-development
product: node-express
tags: [redos, catastrophic-backtracking, regex-security, re2, safe-regex, node-security]
level: practitioner
status: verified
description: "Finding and fixing ReDoS: catastrophic backtracking patterns, linting and checking regexes, RE2 for untrusted patterns, escaping user input into RegExp, and input limits."
sources:
  - https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS
  - https://github.com/uhop/node-re2
  - https://ota-meshi.github.io/eslint-plugin-regexp/rules/no-super-linear-backtracking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regular expression denial of service

Node runs your request handlers on one thread: one regex taking 30 s on a crafted string stalls every request.

## 1. Dangerous shapes
Nested or overlapping quantifiers that can match the same text many ways, followed by a failing match:
```js
/^(a+)+$/            // "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa!" explodes
/^(\w+\s?)*$/        // same problem with words
/^([a-z0-9]+\.)*[a-z]+@/   // hostname/email validators are a classic source (did not blow up on simple inputs in V8; test with recheck)
/(.*a){12}/          // polynomial, not exponential; fast on short inputs
```
Fix by removing ambiguity: `^a+$`; `^\w+(?:\s\w+)*$`; use atomic-style rewrites, possessive logic via lookahead tricks, or a parser instead of a regex.

## 2. Find them
- `eslint-plugin-regexp` rules `no-super-linear-backtracking`, `no-super-linear-move`.
- `recheck` (CLI/library) proves vulnerability with an attack string; `safe-regex2` heuristic.
- Semgrep rules for `new RegExp(` built from input.
- Benchmark suspicious patterns with growing input: time doubling per char = exponential.

## 3. User-controlled patterns
```js
const escaped = typeof RegExp.escape === "function" ? RegExp.escape(q) : q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const re = new RegExp(escaped, "i");
```
If users must supply real regexes (search filters, rules engines), run them with **RE2** (`re2` npm, Go `regexp`, Rust `regex`): linear time, no backreferences or lookaround.

## 4. Limits
- Cap input length before matching (most validators need < 256 chars).
- JS regexes cannot be timed out; for unavoidable heavy matching, run in a worker thread with a timeout and terminate it.
- V8's experimental non-backtracking engine (`--enable-experimental-regexp-engine`, `/l` flag) exists but is not production standard.

## Verify
- [ ] Lint rule enabled in CI; every validator has a test with a 50 KB adversarial string completing in < 50 ms.

## Checked
- Node 24.22.0: `/^(a+)+$/` on `a`*n+`!` took 42 ms at n=20, 323 ms at 26 and 1.4 s at 28; `/^(\w+\s?)*$/` on `a`*n+`!` took 951 ms at 24 and 5.6 s at 30; the rewrites `^a+$` and `^\w+(?:\s\w+)*$` took 0 ms on 50,000 characters; `/(.*a){12}/` and the hostname-style `^([a-z0-9]+\.)*[a-z]+@` did not slow down on the inputs tried (so they are examples to verify with `recheck`, not guaranteed explosions); `RegExp.escape` exists on Node 24 (it also escapes a leading alphanumeric as `a`) and the manual escape works; the `/l` flag parses only with `--enable-experimental-regexp-engine` (SyntaxError otherwise) and ran in 0 ms; a `Worker` stuck in `/^(a+)+$/` was terminated after about 300 ms while the main thread stayed responsive. `eslint-plugin-regexp`, `recheck`, `safe-regex2` and `re2` exist on npm; none were run.
