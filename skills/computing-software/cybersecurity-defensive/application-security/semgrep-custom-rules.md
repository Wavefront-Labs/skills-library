---
id: computing-software.cybersecurity-defensive.application-security.semgrep-custom-rules
name: semgrep-custom-rules
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sast, semgrep-rules, semgrep, custom-rules, taint-mode, rule-testing, code-scanning]
level: advanced
status: verified
description: "Write and test custom Semgrep rules for your codebase's footguns: pattern and taint modes, metavariables, autofix, rule tests and CI rollout with low false positives."
sources: ["https://docs.semgrep.dev/writing-rules/data-flow/taint-mode/overview", "https://docs.semgrep.dev/ignoring-files-folders-code", "https://github.com/semgrep/semgrep-rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Semgrep rules

**Goal:** encode a bug class found in review into a rule that catches every recurrence in CI.

## Pattern rule
```yaml
rules:
- id: raw-sql-helper-with-fstring
  languages: [python]
  severity: ERROR
  message: db.raw() with an f-string allows SQL injection; pass params instead
  patterns:
    - pattern: db.raw(f"...", ...)
  fix: db.raw("...", params)
  metadata: {cwe: "CWE-89", owasp: "A03:2021"}
```
Operators: `pattern-either`, `pattern-not`, `pattern-inside`, `pattern-not-inside`, `metavariable-regex`, `metavariable-pattern`, `focus-metavariable`.

## Taint rule
```yaml
- id: flask-ssrf
  mode: taint
  languages: [python]
  severity: ERROR
  message: request data reaches an outbound HTTP call
  pattern-sources:
    - pattern: flask.request.$ANY
  pattern-sanitizers:
    - pattern: validate_url(...)
  pattern-sinks:
    - pattern: requests.$M($URL, ...)
      focus-metavariable: $URL
```
Write patterns that contain commas in block style as above. The one-line flow form
`[{pattern: requests.$M($URL, ...), ...}]` splits at the comma and fails with "null values prohibited"
(semgrep 1.182.0, `semgrep --validate --config rule.yaml`). Put taint rules under a top-level `rules:` key.

## Test it
Put annotated examples next to the rule (`rule.yaml` + `rule.py`):
```python
# ruleid: raw-sql-helper-with-fstring
db.raw(f"select * from t where id={x}")
# ok: raw-sql-helper-with-fstring
db.raw("select * from t where id=%s", [x])
```
Run `semgrep --test rules/` (prints `All tests passed`; the test file must share the rule file's base name, `r.yaml` with `r.py`, and
the `# ruleid:` / `# ok:` comment goes on the line before the code). Use the Semgrep playground for iteration.
Use `semgrep --validate --config rules/` first to catch YAML errors.

## Roll out
1. Run across the monorepo: `semgrep --config rules/ --json`; triage hits.
   Rule ids in output are prefixed with the directory path (`rules.raw-sql-helper-with-fstring`).
2. Start as comment-only (non-blocking) in PRs; promote to blocking once precision is high.
3. Diff-aware scans in PRs (`semgrep scan --baseline-commit <sha>`, or `semgrep ci`) keep noise to new code.

## Gotchas
- Over-broad patterns (`$X.raw(...)`) flood developers; anchor on imports/types.
- Taint across functions and files needs the Pro engine (Semgrep docs: interprocedural taint is a Pro feature; intrafile needs `--pro-intrafile`); Community Edition taint is intraprocedural.
- Generated and vendored code: exclude via `.semgrepignore` (`.gitignore` syntax). The built-in defaults already skip `node_modules/`, `vendor/`, `.venv/`, `test/`, `tests/` and `*_test.go`, so rules never see code under those paths unless you override the file.

## Verify
- [ ] `semgrep --test` passes for every custom rule.
- [ ] The original bug's code is flagged by the rule.
