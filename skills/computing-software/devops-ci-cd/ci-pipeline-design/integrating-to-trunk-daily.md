---
id: computing-software.devops-ci-cd.ci-pipeline-design.integrating-to-trunk-daily
name: integrating-to-trunk-daily
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, daily-commits, continuous-integration, trunk-based-development]
level: practitioner
status: docs-checked
description: "Make \"everyone integrates to trunk at least daily\" real: slicing work into mergeable increments, hiding unfinished work, and the team agreements that keep trunk safe."
sources: ["https://dora.dev/capabilities/continuous-integration/", "https://martinfowler.com/articles/continuousIntegration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integrating to trunk at least daily

DORA: developers integrate all their work into the main version of the code (trunk, main or
mainline) on a regular basis, and the 2015 State of DevOps Report shows teams perform better
when developers merge to trunk at least daily. Automated tests run before and after the
merge; if they fail, the team stops to fix the problem immediately. Without daily merging
you get long-lived branches that are much harder to integrate and long feedback loops.

## Why frequent integration
Fowler: integration is primarily communication. With commits every few hours a conflict is
found within hours, when little has happened and it is easy to resolve; conflicts undetected
for weeks can be very hard. His rule of thumb is that every developer commits to the
mainline every day, and people experienced with CI integrate more often. Semantic conflicts
(a renamed function that new code calls) are why self-testing code matters.

**Semi-integration is not CI.** Regularly pulling mainline into a feature branch and testing
does not count: full integration means pushing work back so others can see it. Fowler says
no code should sit on a branch longer than a few hours without being pushed to mainline.

## Slicing work into mergeable increments
Frequent commits push developers to break work into small chunks of a few hours. DORA says CI
requires breaking large features into smaller incremental steps; it can take longer to
finish a large feature, but you optimise for getting changes reviewed, integrated, tested and
deployed quickly. Techniques from Fowler for hiding work in progress (latent code, which
must still be production quality and tested):
- **Keystone interface:** add the interface that exposes the new feature last; tests can
  exercise everything beneath it.
- **Dark launching:** test some changes in production before users see them.
- **Feature flags** for latent code that a keystone cannot hide: set per environment so the
  code is active in test and disabled in production; remove the flag promptly once the
  feature is released.
- **Branch by abstraction:** an internal interface that routes between old and new logic,
  useful for large infrastructural changes.
- **Parallel change (expand-contract):** split a change into reversible steps, for example
  add the new field, write to both, copy data, read from the new field, then remove the old.

## Team agreements
- The build triggers on every push to the mainline in a reference environment, and the
  developer's integration is complete only when that build is green.
- When the build breaks, fixing it takes priority over other work (DORA and Fowler). If the
  build cannot be fixed in a few minutes, identify and revert the breaking change (DORA).
- Fast tests: DORA says tests should run in a few minutes, with an upper limit of about 10
  minutes per its research.
- Make build status visible to the team; DORA prefers chat notifications to email.

## Measuring CI (from DORA)
Percentage of commits that trigger a build and automated tests without manual intervention;
percentage of builds and tests that succeed each day; availability of acceptance and
performance test feedback within a day; time from a broken build to its fix or revert.

## Anti-patterns
- "Semi-integration": branches that pull from mainline but never push back.
- Merging half-done work with no way to hide it (keystone, flag or abstraction).
- Using the CI service on many branches and calling it Continuous Integration; Fowler says
  the CI service needs only monitor the single mainline.

## Verify
- [ ] Commits reach mainline at least daily per developer, and each triggers a build.
- [ ] Unfinished features are hidden by a keystone, flag or abstraction, not left on a branch.
- [ ] Broken builds are fixed or reverted promptly.

## Checked
Confirmed 2026-11-09 by reading the DORA continuous integration capability page in full and Fowler's Continuous Integration article (lines 410-505 on daily integration, semi-integration and builds, lines 640-695 on hiding work in progress).
Removed as unconfirmed: the gh CLI snippets, the "median PR open under 1 day / no branch over 3 days" targets, the stacked-PR tool names, the review SLA of 2 hours, the 10-minute red-trunk rule, and the "integration branch per team" anti-pattern.
Method: docs-checked 2026-11-09 against dora.dev/capabilities/continuous-integration and martinfowler.com continuousIntegration
