---
id: computing-software.devops-ci-cd.ci-pipeline-design.mutation-testing-in-ci
name: mutation-testing-in-ci
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, mutation-testing, mutation-score, pitest, stryker, stryker-mutator, mutmut, cargo-mutants, go-mutesting, incremental-mutation, test-effectiveness, surviving-mutants]
level: advanced
status: docs-checked
description: "Measure test effectiveness with mutation testing in CI: PIT, Stryker, mutmut, cargo-mutants; diff-scoped runs on PRs, full nightly runs, score thresholds and triaging survivors."
sources: ["https://pitest.org/quickstart/", "https://stryker-mutator.io/docs/", "https://mutants.rs/", "https://github.com/boxed/mutmut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutation testing in CI

Coverage shows which lines ran; mutation testing shows whether tests **notice** when a
line is wrong. The tool makes small changes (mutants: `>` to `>=`, `+` to `-`, remove a
call, return null) and runs the tests; a **killed** mutant failed a test, a
**survived** mutant means a gap. Each tool defines its own mutation score formula.

## Tools
| Stack | Tool | Command |
|---|---|---|
| Java/Kotlin | PIT (pitest) | see the pitest.org quickstart |
| JS/TS | StrykerJS | `npx stryker run` |
| Python | mutmut | `mutmut run` |
| Rust | cargo-mutants | `cargo mutants` |

## It is slow: scope it
Full runs cost N mutants x test time. Pattern:
1. **PRs: changed code only.**
   - Stryker: `npx stryker run --incremental` (results are stored in a file; cache it between runs) or `--mutate` with changed files.
   - cargo-mutants: `git diff origin/main... > pr.diff && cargo mutants --in-diff pr.diff`.
2. **Nightly: full run**, publish the HTML report as an artifact, trend the score.
3. Run only fast unit tests against mutants (exclude integration tests); configure
   per-mutant timeouts in the tool's settings.

## Gating
```js
// stryker.conf.json excerpt
"thresholds": { "high": 80, "low": 60, "break": 50 }
```
Start
the break threshold just below the current score so it only prevents regression; raise
it as tests improve. On PRs, gate "no new surviving mutants in changed lines" rather than
a global score.

## Triaging survivors
- Real gap: add an assertion that would fail (often the test calls code but asserts
  nothing about the result).
- **Equivalent mutant** (behaviour identical, e.g. mutating a log message or a redundant
  bound): exclude via config (for example `# pragma: no mutate` in mutmut; other tools have their own exclusion comments or config), with a comment why.
- Don't mutate generated code, DTOs, logging, or config classes: exclude by path.

## Verify
Delete an assertion in a test: the next run reports new survivors in that function and
the PR check fails; restore it and the mutants are killed.

## Checked

2026-10-28. Confirmed: StrykerJS `--incremental` (stores results in a file) and `--mutate`, and the `thresholds` option with defaults high 80, low 60, break null; cargo-mutants `--in-diff DIFF_FILE`; mutmut `mutmut run` and `# pragma: no mutate`. Removed: PIT commands and options (page unreadable), `dotnet stryker`, Scala and Go rows, `mutmut results`, `timeoutFactor`, the stryker-incremental.json path, the Stryker disable comment, and the fixed score formula.

Method: documentation only; no commands were run.
