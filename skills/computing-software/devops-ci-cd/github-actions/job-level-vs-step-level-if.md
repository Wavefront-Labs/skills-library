---
id: computing-software.devops-ci-cd.github-actions.job-level-vs-step-level-if
name: job-level-vs-step-level-if
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, job-level-if, if-expression-syntax, if-conditionals]
level: practitioner
status: verified
description: "Write correct `if:` at job and step level: implicit ${{ }}, the hidden success() default, contexts allowed per level, and the string-literal trap that makes if always true."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idif", "https://docs.github.com/en/actions/reference/workflows-and-actions/expressions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job-level vs step-level `if:`

## Implicit expression syntax
`if:` is always evaluated as an expression, so `${{ }}` is optional:
```yaml
if: github.ref == 'refs/heads/main'
```
Trap: anything after a `${{ }}` that leaves extra text makes a **non-empty string**, which is truthy:
```yaml
if: ${{ github.ref == 'refs/heads/main' }} && false   # string -> always true
if: ${{ github.ref == 'refs/heads/main' && false }}    # correct
```
Also avoid a bare leading `!`: `if: !cancelled()` is a YAML tag error (PyYAML: `could not determine a
constructor for the tag`). Write `if: ${{ !cancelled() }}` or quote it (`if: "!cancelled()"`).

## Implicit success()
If the expression contains no status function, `success() &&` is prepended. So
`if: github.event_name == 'push'` on a step after a failed step will **not** run. To run anyway add a
status function: `if: always() && github.event_name == 'push'` (or `!cancelled() && ...`).

## Contexts available
| Level | Available |
|---|---|
| `jobs.<id>.if` | github, needs, vars, inputs. **Not** `env`, `secrets`, `steps`, `matrix`, `runner` |
| `steps[*].if` | github, needs, strategy, matrix, job, runner, env, vars, steps, inputs. Still **no** `secrets` |

`env` is not an available context in a job-level `if`; actionlint reports `context "env" is not allowed here`.
Use `vars.X` or a prior job output instead. Secrets cannot be referenced directly in `if:`; map them to a
job-level env var first and test that (see the secret presence checks skill).

## Job vs step behaviour
- Skipped job: dependants also skip unless they use a status function (`always()`, `!cancelled()`) and
  check `needs.<job>.result` (`success`, `failure`, `cancelled` or `skipped`).
- A job skipped by a conditional reports Success for required checks; a job that depends on a failed job
  is skipped and may not block merging (GitHub docs, troubleshooting required status checks).
- Matrix: `jobs.<id>.if` is evaluated before matrix expansion, so `matrix` is not available there;
  filter matrix legs with `exclude` or a step-level if.

## Verify
- [ ] Run with the false branch and confirm the job/step shows "skipped", not run.
- [ ] `actionlint` reports no "context not available" errors.
