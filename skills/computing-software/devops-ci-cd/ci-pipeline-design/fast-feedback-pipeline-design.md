---
id: computing-software.devops-ci-cd.ci-pipeline-design.fast-feedback-pipeline-design
name: fast-feedback-pipeline-design
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, ci, continuous-integration, pipeline-design, fast-feedback, flaky-tests, quarantine, merge-queue, commit-build, deployment-pipeline]
level: practitioner
status: docs-checked
description: "Design a CI pipeline for fast, trustworthy feedback: a quick commit build, a slower second stage, flaky-test handling, merge queues and fixing red builds first."
sources: ["https://martinfowler.com/articles/continuousIntegration.html", "https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI pipeline design — fast, trustworthy feedback

**Goal:** a developer learns quickly whether their change is safe to merge, and a red
build almost always means a real problem.

## 1. Keep the build fast, using a staged pipeline
- Fowler: the whole point of CI is rapid feedback, and a long build "sucks the blood" out
  of it. The XP guideline of a ten-minute build is, for most projects, within reason.
  Every minute removed is saved for each developer on every commit.
- For enterprise applications the usual bottleneck is testing, particularly tests that use
  external services such as a database.
- Use a deployment pipeline (staged build): the commit build runs on every push to the
  mainline and must be fast, so it takes shortcuts (for example localised unit tests with
  test doubles such as an in-memory database or stubbed services). A second stage runs
  slower suites that hit a real database and exercise more end-to-end behaviour; Fowler's
  example says that suite might take a couple of hours.
- A second-stage failure lacks the "stop everything" quality, but the team fixes it as
  fast as possible. The second stage may not run on every commit; it runs as often as it can,
  on the last good commit build.
- When the second stage finds a bug, add a test to the commit build that would have caught
  it, where a fast test can expose the bug.
- Parallelism and multiple machines (including cloud environments) are another way to
  speed things up.
- Measure queue time separately from run time, so you know whether to fix the pipeline or
  runner capacity. (Judgement, not from the sources.)

## 2. Fix broken builds immediately
CI only works if the mainline stays healthy. Fowler quotes Kent Beck: nobody has a higher
priority task than fixing the build. Usually the best fix is to revert the latest commit to
the last known good build, unless the cause is obvious and fixed by a new commit. Some teams
use a pending head (pre-tested, delayed or gated commit): commits go to another branch and
reach the mainline only after a green build.

## 3. Flaky tests: detect, mitigate, fix
Google defines a flaky result as a test that shows both a pass and a fail with the same code.
In its corpus about 1.5% of test runs were flaky, and almost 16% of tests had some
flakiness; the blog names concurrency, non-deterministic or undefined behaviour, flaky
third-party code and infrastructure problems as causes. Flakiness teaches people to
ignore real failures.
- Re-running only failing tests, or automatic re-run on failure, reduces false positives, but
  marking a test "flaky" so it fails only after three consecutive failures delays discovery
  of real breakage (a 15-minute test takes 45 minutes to report) and lets developers ignore
  their own flakiness. Google calls this hardly a perfect solution.
- Google also runs a tool that monitors flakiness and automatically quarantines a test
  when it is too high, taking it off the critical path and filing a bug. Quarantine can mask
  a real race condition or other bug, so it needs an owner and follow-up.
- Another tool detects when a test's flakiness level changes and finds the change that
  caused it.

## 4. Gate merges with a merge queue
GitHub's merge queue validates each pull request's changes against the latest version of
the target branch plus the pull requests ahead of it, in first-in-first-out order, using a
temporary `merge_group`. If you use GitHub Actions for required checks, workflows must also
trigger on the `merge_group` event, or the required check is never reported and the merge
fails. A pull request is removed from the queue if required checks fail or conflicts arise
after grouping.

## Verify
- [ ] Commit-build time is measured and visible, and the team has a target for it.
- [ ] Second-stage failures lead to new commit-build tests where possible.
- [ ] Flaky tests are tracked; quarantined tests each have an owner and a bug.
- [ ] A red mainline is reverted or fixed first, before other work.
- [ ] If a merge queue is used, required checks run on its trigger as well as on the pull request.

## Checked
Confirmed 2026-11-09 by reading: Fowler's Continuous Integration article (sections on fixing broken builds, keeping the build fast, deployment pipeline and commit build, pending head; read lines 505-630 and surrounding headings), the Google Testing Blog flaky tests post (full body, comments skimmed), and GitHub's merge queue page (merge_group, FIFO, latest base plus changes ahead, removal on failure).
Removed as unconfirmed: the numeric targets (p50/p90, 95% green, 1-2% flaky), the stage-ordering table with tool names (actionlint, hadolint), pytest-split, Jest, CircleCI and Knapsack sharding flags, the quarantine marker names, random-order plugin flags, "one aggregate ci-ok job", Bors-style and GitLab merge trains, and the shard-balance threshold.
Method: docs-checked 2026-11-09 against martinfowler.com continuousIntegration, testing.googleblog.com 2016/05 flaky tests, docs.github.com managing a merge queue
