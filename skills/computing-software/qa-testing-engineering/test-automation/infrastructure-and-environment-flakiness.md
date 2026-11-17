---
id: computing-software.qa-testing-engineering.test-automation.infrastructure-and-environment-flakiness
name: infrastructure-and-environment-flakiness
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [environment-flakiness, flaky-tests, ci-infrastructure, test-environments, resource-contention]
level: practitioner
status: draft
description: "Diagnose flakiness caused by CI infrastructure and environments: resource starvation, shared state, network and DNS, clock, container startup and noisy neighbours."
sources:
  - https://testing.googleblog.com/
  - https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
  - https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infrastructure and environment-induced flakiness

**Goal:** separate flakes caused by where tests run from flakes caused by test or product code, and fix the infrastructure ones at the source.

## Signals that it is the environment
- Failures cluster on certain runners, times of day or parallel worker counts, not on certain tests.
- Many unrelated tests fail in the same run with timeouts or connection errors.
- Failures disappear when run alone or with fewer workers.
- Error text: `ECONNRESET`, `ETIMEDOUT`, DNS resolution failures, `OOMKilled`, `no space left on device`, browser crash ("Target closed").

## Common causes and fixes
- **CPU/memory starvation:** too many workers for the runner size (a 2-vCPU hosted runner with 4 browser workers). Measure, then lower workers or use bigger runners; Playwright `workers: '50%'`.
- **Shared environment state:** parallel runs from different branches using the same test environment and accounts. Isolate data per run (unique prefixes), or use ephemeral environments.
- **Dependency startup:** tests start before DB/containers are ready. Use health checks (`--health-cmd`, Testcontainers wait strategies), not sleeps.
- **Network to third parties:** stub external services in CI; keep a separate scheduled job for live integration checks.
- **DNS and rate limits:** package registries or APIs throttling CI; cache dependencies, use mirrors.
- **Clock and timezone:** runners in UTC vs local developer time; clock skew in containers. Fix the TZ in config and freeze time in tests.
- **Disk:** leftover artefacts on self-hosted runners; clean workspaces, ephemeral runners.
- **Browser/driver version drift:** pin browser and driver versions (Playwright pins its browsers; pin Selenium images by digest).

## Diagnose
Record runner name, worker count, CPU/memory, and timestamps with each result; group failures by those fields. Re-run a failing commit many times on the same runner type to reproduce.

## Verify
Flake data grouped by runner and worker count shows no clustering after fixes, and environment-classified flakes trend down over a month.
