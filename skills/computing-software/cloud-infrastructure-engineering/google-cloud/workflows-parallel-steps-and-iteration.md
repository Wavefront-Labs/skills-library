---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workflows-parallel-steps-and-iteration
name: workflows-parallel-steps-and-iteration
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workflows, workflows-parallel, parallel-for, parallel-branches, shared-variables, concurrency-limit]
level: practitioner
status: docs-checked
description: "Use parallel branches and parallel for loops in Cloud Workflows: shared variables, concurrency limits, exception policy, collecting results, and limits on branches and iterations."
sources: ["https://cloud.google.com/workflows/docs/reference/syntax/parallel-steps", "https://cloud.google.com/workflows/docs/reference/syntax/iteration", "https://cloud.google.com/workflows/quotas"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Workflows parallel steps and iteration

## Parallel for
```yaml
main:
  params: [input]
  steps:
    - init:
        assign:
          - results: {}
    - fanout:
        parallel:
          shared: [results]
          concurrency_limit: 10
          exception_policy: continueAll
          for:
            value: region
            in: '${input.regions}'
            steps:
              - probe:
                  call: http.get
                  args: {url: '${"https://" + region + ".api.example.com/health"}'}
                  result: r
              - save:
                  assign:
                    - results[region]: '${r.code}'
    - done:
        return: '${results}'
```
- Variables written inside parallel steps must be declared before and listed in `shared`.
  Assignments to shared variables are atomic per statement.
- `concurrency_limit` caps simultaneous iterations/branches (useful to protect APIs).
- `exception_policy: continueAll` is the default (and currently the only) policy: no further action is taken on an unhandled exception and all other branches attempt to run. An unhandled branch exception raises a catchable `UnhandledBranchError` for the parallel step.

## Parallel branches
```yaml
- both:
    parallel:
      shared: [a, b]
      branches:
        - getA:
            steps:
              - ca: {call: http.get, args: {url: https://svc-a/x}, result: a}
        - getB:
            steps:
              - cb: {call: http.get, args: {url: https://svc-b/y}, result: b}
```

## Plain iteration
`for: {value: v, index: i, in: '${list}'}` or `range: [1, 10]`; `break`/`continue` via `next`.

## Gotchas
- Limits exist on branches per parallel step, concurrent branches/iterations per execution and
  nesting depth; check the Workflows quotas page before large fan-outs (nested parallel counts too).
- Key results by item rather than by position.

## Verify
- [ ] Execution with 30 regions completes with `concurrency_limit` honored (step timestamps) and all results keyed.

## Checked

2026-10-28. Confirmed against: Workflows parallel-steps and iteration pages (shared variables, atomic assignments, concurrency_limit, exception_policy continueAll as the default, UnhandledBranchError, for/range loops, next: continue) and the Workflows quotas page link.

Removed or rewritten: the claim that the default policy stops scheduling new branches (wrong: continueAll is the default), step-billing and Batch advice, result ordering, and branch-variable scoping.

Method: documentation only; no commands were run.
