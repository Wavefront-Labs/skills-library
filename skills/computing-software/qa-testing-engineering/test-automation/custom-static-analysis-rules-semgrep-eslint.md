---
id: computing-software.qa-testing-engineering.test-automation.custom-static-analysis-rules-semgrep-eslint
name: custom-static-analysis-rules-semgrep-eslint
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [custom-lint-rules, semgrep, eslint, static-analysis, code-patterns]
level: practitioner
status: verified
description: "Write custom static analysis rules to ban a defect pattern: Semgrep YAML rules with tests, ESLint custom rules with RuleTester, and CI rollout."
sources:
  - https://semgrep.dev/docs/writing-rules/rule-syntax
  - https://semgrep.dev/docs/writing-rules/testing-rules
  - https://eslint.org/docs/latest/extend/custom-rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom static analysis rules (Semgrep, ESLint)

**Goal:** turn a defect found once (in review, incident or test) into a rule that blocks it forever.

## Semgrep rule
```yaml
# rules/no-requests-without-timeout.yaml
rules:
  - id: requests-without-timeout
    languages: [python]
    severity: ERROR
    message: requests call without timeout can hang workers; pass timeout=
    patterns:
      - pattern-either:
          - pattern: requests.$METHOD(...)
      - pattern-not: requests.$METHOD(..., timeout=$T, ...)
      - metavariable-regex:
          metavariable: $METHOD
          regex: ^(get|post|put|patch|delete|request)$
```
Test file `rules/no-requests-without-timeout.py`:
```python
# ruleid: requests-without-timeout
requests.get(url)
# ok: requests-without-timeout
requests.get(url, timeout=5)
```
`semgrep --test rules/` runs annotations (`All tests passed` on Semgrep 1.182 on Windows); `semgrep --config rules/ --error src/` in CI (exits 1 on a finding; `# nosemgrep: requests-without-timeout` suppressed it).

## ESLint custom rule (flat config)
```js
// eslint-rules/no-date-now.js
export default {
  meta: { type: "problem", messages: { avoid: "Use clock.now() so tests can control time." }, schema: [] },
  create(context) {
    return {
      "CallExpression[callee.object.name='Date'][callee.property.name='now']"(node) {
        context.report({ node, messageId: "avoid" });
      },
    };
  },
};
```
Register (checked with ESLint 10 flat config): `plugins: { local: { rules: { "no-date-now": noDateNow } } }, rules: { "local/no-date-now": "error" }`. Test with `RuleTester` (`valid` / `invalid` arrays with expected `errors`; the example rule passed `new RuleTester().run(...)` and reported `local/no-date-now` on `Date.now()`). `// eslint-disable-next-line local/no-date-now -- reason` suppressed it.

## Rollout
1. Run the rule on the whole repo; count hits.
2. Fix or baseline existing hits (`# nosemgrep: <id>` with reason, ESLint `// eslint-disable-next-line local/no-date-now -- reason`).
3. Enforce as error on changed files, then everywhere.

## Gotchas
- Overly broad patterns produce noise and get disabled; always include `ok:` cases.
- Semgrep matches syntax, not types across files (unless using its cross-file Pro engine). Plain `import requests as r; r.get(u)` was still matched in a run (import aliases are resolved), but calls through wrapper functions or objects returned from other modules will not be.
- Require a reason on suppressions (the `require-description` rule exists in `@eslint-community/eslint-plugin-eslint-comments`).

## Verify
Rule tests pass, CI fails on a new violation, and suppressions each carry a justification.
