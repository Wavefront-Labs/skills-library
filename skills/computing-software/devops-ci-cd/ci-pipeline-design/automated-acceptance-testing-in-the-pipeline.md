---
id: computing-software.devops-ci-cd.ci-pipeline-design.automated-acceptance-testing-in-the-pipeline
name: automated-acceptance-testing-in-the-pipeline
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, acceptance-tests, end-to-end-tests, e2e-in-pipeline, playwright, contract-tests, flaky-e2e, test-ownership]
level: advanced
status: docs-checked
description: "Run acceptance and end-to-end tests in CI: few core E2E journeys, user-term acceptance tests, Playwright CI settings (workers, global timeout, report upload), contract tests."
sources: ["https://martinfowler.com/articles/practical-test-pyramid.html", "https://playwright.dev/docs/ci", "https://docs.pact.io/pact_broker/can_i_deploy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated acceptance testing in the pipeline

## 1. What acceptance tests are (Practical Test Pyramid)
Higher in the pyramid you test, as a black box, whether features work from a user's
perspective, in given/when/then terms (given a logged in user and an article "bicycle", when the
user opens the page and clicks add to basket, then the article is in the basket). Fowler says
the name (functional, acceptance, broad-stack) matters less than having the tests: pick a term
and stick to it. BDD-style writing shifts the mindset to user needs, but full BDD tools such
as Cucumber are not required; well-factored helper functions can make tests read as user
behaviour (his Python example builds on helpers such as `a_user_with_empty_basket()`).

## 2. Keep end-to-end tests few
Fowler's cautions about UI end-to-end tests:
- They are notoriously flaky, often failing as false positives; the more sophisticated the UI,
  the flakier. Causes include browser quirks, timing issues, animations and unexpected
  dialogs.
- Ownership is unclear when they span multiple services; a centralised QA team is called an
  anti-pattern in a DevOps world, and there is no easy answer.
- They need a lot of maintenance and run slowly; with many microservices you cannot run
  them locally.
- Aim for a bare minimum: tests of the core value journeys (his e-commerce example: search,
  basket, checkout), perhaps one or two more. Edge cases are already covered at lower levels,
  so do not repeat them higher up.
- Where a UI test is too flaky, REST API-driven end-to-end tests are a less flaky option that
  still covers a broad part of the application.

## 3. Contract tests reduce cross-service E2E
Consumer-driven contract tests make consumers publish their requirements and providers verify
them. With a Pact Broker, `pact-broker can-i-deploy --pacticipant <name> --version <v>
--to-environment <env>` exits 0 or 1 on compatibility; Pact describes this as replacing the
old practice of deploying pre-tested sets of applications together. See the component
pipelines skill.

## 4. Playwright in CI (Playwright docs)
- Install browsers and OS dependencies with `npx playwright install --with-deps`, or use the
  Docker image on Linux agents.
- Playwright recommends `workers: process.env.CI ? 1 : undefined` for stability and
  reproducibility, enabling parallelism only on a powerful self-hosted CI system; for wider
  parallelism use `--shard=<n>/<total>` across CI jobs.
- Always set `globalTimeout` (for example `60 * 60 * 1000`): by default a run has no upper
  bound, and a hung suite killed by the runner produces no report. If you add a job-level
  timeout, keep it comfortably above `globalTimeout`.
- Upload the report even on failure, for example `actions/upload-artifact` with
  `if: ${{ !cancelled() }}` and `path: playwright-report/`.

## Verify
- [ ] End-to-end tests cover only the core journeys; edge cases sit lower in the pyramid.
- [ ] The suite has a global timeout and always publishes its report.
- [ ] Someone named owns the end-to-end suite.

## Checked
Confirmed 2026-11-09 against the Practical Test Pyramid (acceptance and end-to-end sections, lines 1058-1100 and 1239-1283), the Playwright CI page (workers, globalTimeout, install, report upload, sharding) and the Pact can-i-deploy page, from local text copies.
Removed as unconfirmed: the Humble and Farley chapter 8 three-layer model, ephemeral Kubernetes and kind/Helm environments, preview environments, docker compose and Testcontainers advice (the guide was never read), data isolation and seeding rules, fake-clock tips, retry and quarantine policies and the two-week deletion rule, the 60-minute budget and 5x rerun check, trace and video options, and the Actions pipeline sketch.
Method: docs-checked 2026-11-09 against martinfowler.com practical-test-pyramid, playwright.dev docs/ci, docs.pact.io can_i_deploy
