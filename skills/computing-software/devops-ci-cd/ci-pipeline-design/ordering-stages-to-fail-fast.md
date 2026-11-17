---
id: computing-software.devops-ci-cd.ci-pipeline-design.ordering-stages-to-fail-fast
name: ordering-stages-to-fail-fast
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, fail-fast-ordering, deployment-pipeline, pipeline-stages]
level: practitioner
status: docs-checked
description: "Order pipeline stages and jobs so failures surface early: quick checks first, parallel jobs, the needs keyword, skipping unneeded jobs and superseded pipelines."
sources: ["https://docs.gitlab.com/ci/pipelines/pipeline_efficiency/", "https://martinfowler.com/bliki/DeploymentPipeline.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ordering stages to fail fast

Goal: a developer learns about the most likely failure in the shortest time, and expensive
stages run only on candidates that passed cheap ones. Fowler's deployment pipeline idea: each
stage gives increasing confidence at the cost of extra time, so early stages find most
problems for faster feedback while later stages probe slower and more thoroughly.

## What GitLab's pipeline efficiency guide says
- **Fail fast:** a very long job keeps a pipeline from returning a failed status until it
  finishes. Design pipelines so jobs that can fail fast run earlier: for example add an early
  stage and move syntax checks, style linting and Git commit message verification there.
  Decide whether it matters for long jobs to run early, before feedback from faster jobs;
  early failures may show that the rest of the pipeline should not run, saving resources.
- **Warning sign:** tests that fail at the end of a long pipeline but could be in an earlier
  stage cause delayed feedback. Flaky tests, failures that could safely be ignored but halt
  the pipeline, and coverage drops are other patterns to look for.
- **Parallel jobs:** running jobs that test different things in parallel in the same stage
  reduces overall runtime, at the cost of needing more runners at the same time.
- **`needs`:** in a basic configuration jobs wait for all jobs in earlier stages. That is the
  simplest but usually slowest. Pipelines with the `needs` keyword and parent/child pipelines
  are more flexible and can be more efficient, but harder to understand and analyse. The full
  pipeline graph can show `needs` dependencies and help analyse the critical path.
- **Reduce how often jobs run:** use `rules` to skip tests that are not needed (for example
  backend tests when only the frontend changed), and `interruptible` to stop old pipelines
  superseded by a newer one.
- **Measure:** job, stage and total pipeline runtime are the easiest indicators of an
  inefficient pipeline; the critical path sets the minimum and maximum duration. Improve
  iteratively: make small changes, monitor the effect, then iterate.

## Anti-patterns drawn from the above
- Lint or other quick checks placed after long suites.
- One giant serial job.
- Letting superseded pipelines run to completion.

## Verify
- [ ] The earliest stage holds the quick checks that fail most often.
- [ ] Time to first failure for failing pipelines is tracked.
- [ ] Jobs that need not run are skipped by rules.

## Checked
Confirmed 2026-11-09 by reading the whole GitLab Pipeline efficiency page and Fowler's Deployment Pipeline page. The O'Reilly book landing page was cited but gives no checkable content and was dropped.
Removed as unconfirmed: the numbered ordering heuristic and failure-probability-over-duration formula, GitHub matrix `fail-fast`, `workflow:auto_cancel:on_job_failure`, Jenkins `parallelsAlwaysFailFast()`, the pytest `--ff` and Jest `--onlyFailures` flags, the "security scans nightly" anti-pattern and the 5-minute time-to-first-failure target.
Method: docs-checked 2026-11-09 against docs.gitlab.com/ci/pipelines/pipeline_efficiency and martinfowler.com/bliki/DeploymentPipeline
