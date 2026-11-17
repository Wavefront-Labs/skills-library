---
id: computing-software.devops-ci-cd.github-actions.step-outcome-vs-conclusion
name: step-outcome-vs-conclusion
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, step-outcome, step-conclusion, steps-context, steps-outcome, continue-on-error, failure-after-continue, step-id, retry-step, soft-fail, report-failed-step, if-steps-outcome, job-status, if-conditionals, job-outputs]
level: practitioner
status: verified
description: "Use steps.<id>.outcome (raw result) vs steps.<id>.conclusion (after continue-on-error) to retry, report or fail later; the pattern for soft-failing a step and still turning the job red."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#steps-context", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepscontinue-on-error"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# steps.<id>.outcome vs conclusion

**Goal:** let a flaky or informational step fail without aborting the job, then decide
later what that failure means.

## 1. The two fields
For a step with `id: t`:
- `steps.t.outcome` — the **raw** result: `success`, `failure`, `cancelled`, `skipped`.
- `steps.t.conclusion` — the result **after** `continue-on-error` is applied: a failed step
  with `continue-on-error: true` has `outcome: failure` but `conclusion: success`.
Both are properties of the `steps` context, so they exist only for steps with an `id:` in the same job.

## 2. Core pattern: soft-fail now, hard-fail at the end
```yaml
steps:
  - id: tests
    continue-on-error: true
    run: npm test
  - name: Upload report (even on failure)
    if: always()
    uses: actions/upload-artifact@v4
    with: { name: junit, path: reports/ }
  - name: Fail the job if tests failed
    if: steps.tests.outcome == 'failure'
    run: exit 1
```
Without the last step the job is green although tests failed — `continue-on-error` converts
the job-level conclusion too. Checking `outcome` restores the red.

## 3. Retry a step once
```yaml
  - id: first
    continue-on-error: true
    run: ./flaky-integration.sh
  - if: steps.first.outcome == 'failure'
    run: ./flaky-integration.sh        # second attempt; its failure fails the job
```
For bounded retries use `nick-fields/retry` (current major `v4`; `v3` also exists). Its inputs include
`max_attempts`, `timeout_minutes`, `retry_wait_seconds` and `retry_on: any|timeout|error`, and it exposes
`total_attempts` and `exit_code` outputs.

## 4. Status functions vs step results
`failure()` returns true when any previous step of the job fails (and, across jobs, when any ancestor job
fails). `steps.x.outcome` is the pre-`continue-on-error` result, so use it to test one specific step.
`always()` runs even when the run is cancelled; GitHub's docs recommend `!cancelled()` for steps that
should run on success or failure but not on cancel.

## 5. Gotchas
- `outcome` of a `skipped` step is `skipped`; comparing to `'failure'` is false, so a step
  that never ran is not treated as failed.
- Job-level `continue-on-error: true` stops that job failing the workflow run (and, in a matrix, other
  legs keep running).
- Exit code 0 with stderr noise is `success` — the runner does not inspect output.

## Verify
- [ ] A deliberately failing soft step leaves the job red via the outcome check.
- [ ] Artifacts/report steps run on failure (`if: always()` or `!cancelled()`).
- [ ] No step is referenced by id that lacks an `id:` (expression resolves to empty).
