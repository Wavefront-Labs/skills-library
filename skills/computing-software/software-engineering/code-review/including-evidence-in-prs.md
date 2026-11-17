---
id: computing-software.software-engineering.code-review.including-evidence-in-prs
name: including-evidence-in-prs
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, pr-evidence, screenshots, test-results, benchmarks, pr-description]
level: intro
status: draft
description: "Include evidence in PRs so reviewers can trust the change: test output, screenshots and recordings for UI, benchmark comparisons, query plans and rollout verification."
sources: ["https://google.github.io/eng-practices/review/developer/cl-descriptions.html", "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository", "https://github.com/sharkdp/hyperfine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Including evidence (test results, screenshots, benchmarks)

Claims in a PR description ("faster", "fixes the crash", "no visual change") need proof the reviewer
can check without re-doing your work.

## By change type
| Change | Evidence |
|---|---|
| Bug fix | failing test before / passing after; link to error or issue; reproduction steps |
| UI | before/after screenshots at relevant breakpoints and themes; short screen recording (GIF/MP4) for interactions; accessibility check output |
| Performance | benchmark numbers before/after with method (`hyperfine --warmup 3 'old' 'new'`, JMH, pytest-benchmark, `benchstat old.txt new.txt`), machine, iterations, variance |
| SQL / migrations | `EXPLAIN (ANALYZE, BUFFERS)` before/after; migration timing on production-sized data; lock behaviour |
| API change | example request/response; generated OpenAPI diff (`oasdiff`) |
| Infra (Terraform/K8s) | `terraform plan` summary (resources added/changed/destroyed), `kubectl diff` |
| Refactor | statement that behaviour is unchanged + which tests cover it; coverage report for touched code |
| Config/flags | which environments, default value, how it was verified in staging |

## Formatting
- Put evidence in the description (or a pinned comment), not only in CI logs that expire.
- Collapse long output: `<details><summary>Benchmark output</summary> ... </details>`.
- Redact secrets, tokens, personal data from screenshots and logs.
- PR templates with sections ("Testing done", "Screenshots") nudge authors to include it.

## Honest evidence
Note what you did **not** test ("not tested on Safari", "benchmark on laptop, not prod hardware").
Don't cherry-pick the best run; report median and spread. Reviewers trust authors who flag gaps.
