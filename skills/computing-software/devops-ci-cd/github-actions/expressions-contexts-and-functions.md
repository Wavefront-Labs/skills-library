---
id: computing-software.devops-ci-cd.github-actions.expressions-contexts-and-functions
name: expressions-contexts-and-functions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, expressions, contexts, github-context, env-context, steps-context, needs-context, inputs-context, vars-context, secrets-context, runner-context, expression-functions, contains, startswith, format, join, tojson, fromjson, hashfiles, success, failure, always, cancelled, operators, truthiness, type-coercion, context-availability]
level: practitioner
status: verified
description: "Write correct ${{ }} expressions in GitHub Actions: context availability per key, coercion rules, contains/format/toJSON/fromJSON/hashFiles, status functions, injection-safe use."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expressions, contexts and functions

**Goal:** expressions that evaluate the way you expect, in the places they are allowed,
without leaking untrusted strings into shells.

## 1. Which contexts exist where
Not every context is readable at every key. The authoritative list is the "Context availability" table in
the contexts reference; actionlint enforces it (`context "env" is not allowed here`).
- `github`, `inputs`, `vars`: almost everywhere (incl. `concurrency`, `env`, `run-name`).
- `env`: in step keys (`if`, `with`, `run`, `env`, `name` ...) and `container.env.*` / `services.*.env.*`;
  **not** in `jobs.*.if`, `runs-on`, `strategy`, `concurrency` or job-level `env`. Use `vars` or a
  `needs` output instead.
- `secrets`: allowed in `env`, step `with`/`run`/`env`; **not** in any `if` (job or step). Standard trick: map
  the secret to an env var and test the env var in a step `if`, or output a boolean from a prior job.
- `steps`: only after the step with an `id` has run, same job.
- `needs`: `needs.<job>.outputs.<name>` / `needs.<job>.result` in jobs that list `needs`.
- `matrix`: defined under `jobs.*.strategy`; readable in `runs-on`, `name`, `env`, `steps`, not in `jobs.*.if`.
- `runner` (`runner.os`, `runner.temp`, `runner.arch`): step keys, job `outputs`, container/services env.
- `job.status`, `job.container`, `job.services.<id>.id`: step keys.

## 2. Syntax rules
- `${{ }}` required everywhere except `if:` (there it's implicit — but *mixing* a `${{` inside
  an `if` means the **whole** expression must be wrapped; `if: ${{ a }} && b` is a bug).
- Strings use **single** quotes: `'main'`; escape a quote as `''`. Double quotes inside `${{ }}` are an
  error (actionlint: "only single quotes are available for string delimiter").
- Operators: `== != < <= > >= && || !`, `( )`, index `a['b']`/`a.b`, wildcard `a.*.b` (returns
  an array — `contains(needs.*.result, 'failure')`).
- String comparison ignores case (`'MAIN' == 'main'` is true). Equality is loose: when types differ both
  sides are coerced to numbers (null → 0, `true` → 1, `false` → 0, `''` → 0, a numeric string → that
  number, any other string/array/object → NaN). So `'1' == 1` and `null == ''` are true, but
  `'true' == true` is false.
- Truthiness in `if:` — a non-empty string is true, including `'false'`. Always compare
  boolean-looking *strings* explicitly: `if: needs.check.outputs.deploy == 'true'`.
  `inputs.flag` from `workflow_dispatch type: boolean` **is** a real boolean; from
  `github.event.inputs.flag` it is the string `'true'`.

## 3. Functions
| fn | use |
|---|---|
| `contains(search, item)` | string substring (case-insensitive) or array membership: `contains(github.event.pull_request.labels.*.name, 'deploy')` |
| `startsWith(s, p)` / `endsWith` | `startsWith(github.ref, 'refs/tags/')` |
| `format('{0}-{1}', a, b)` | `{{` escapes a brace |
| `join(array, ', ')` | `join(github.event.issue.labels.*.name, ', ')` (default separator is `,`) |
| `toJSON(x)` | pretty-print a context for debugging |
| `fromJSON(s)` | build dynamic matrices and typed values: `strategy: matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}`; `fromJSON('true')` for a real boolean |
| `hashFiles('**/package-lock.json', '!**/node_modules/**')` | cache keys; files must be inside `GITHUB_WORKSPACE`; returns an empty string when nothing matches (runner source) — guard with `hashFiles(...) != ''` |
| `success()` `failure()` `cancelled()` `always()` | status functions, see below |

## 4. Status functions and when steps run
Default step/job `if` is `success()`. `if: failure()` = some previous step failed.
`always()` runs even on cancel — GitHub's docs recommend `!cancelled()` when you want "run on
success or failure but not on cancel" (e.g. upload test reports). `if: failure() && steps.test.conclusion == 'failure'`
narrows to a specific step (`outcome` is before `continue-on-error`, `conclusion` after).

Job-level: a job with `needs: [a, b]` is skipped if a dependency failed **unless** its `if` uses a
status function such as `always()`; then check `needs.a.result` (`success|failure|cancelled|skipped`).

## 5. Script injection — the rule
Never interpolate untrusted context straight into `run:`. GitHub's script-injection guidance treats contexts ending in `body`, `default_branch`, `email`, `head_ref`,
`label`, `message`, `name`, `page_name`, `ref` and `title` as untrusted, for example
`github.event.issue.title`, `github.event.pull_request.body`, `github.head_ref`, commit messages and
author names/emails.
```yaml
- env:
    TITLE: ${{ github.event.pull_request.title }}   # interpolated by the runner into an env var, not the shell
  run: echo "$TITLE" | grep -q WIP && exit 1
```
`${{ }}` is substituted **before** the shell sees the script — a title containing a quote and a
semicolon breaks out of the string (GitHub's own example is a title of `a"; ls $GITHUB_WORKSPACE"`).
The same applies to `${{ }}` inside `actions/github-script` JavaScript.

## 6. Debug patterns
```yaml
- run: echo '${{ toJSON(github) }}'           # whole context
- run: echo "${{ steps.x.outputs.y }}"
- name: Dump needs
  run: echo '${{ toJSON(needs) }}'
```
Never dump the `secrets` context.

## Verify
- [ ] `if:` expressions with a `${{` are fully wrapped; no `'false'`-string truthiness bugs.
- [ ] Untrusted fields reach shells only through `env:`.
- [ ] Report-upload steps use `!cancelled()`, not `always()`.
- [ ] Cache keys guard `hashFiles` returning `''`.
