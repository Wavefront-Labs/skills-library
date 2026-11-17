---
id: computing-software.devops-ci-cd.dagger.adopting-dagger-monorepos
name: adopting-dagger-monorepos
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, adoption, daggerizing, monorepo, ci-migration, best-practices, poc]
level: practitioner
status: docs-checked
description: "Plan Dagger adoption (research, POC, CI integration, expansion, reusable modules) and organize modules in a monorepo with orchestrator or shared patterns."
sources: [https://docs.dagger.io/0.21/reference/best-practices/adopting, https://docs.dagger.io/0.21/reference/best-practices/monorepos]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adopting Dagger and structuring monorepos

Goal: move workflows into Dagger incrementally and organize modules sensibly. Dagger 0.21 docs.

## Adoption phases

1. Research: look at case studies; check red flags. Poor fit if the project is too early for CI, outputs only Windows, Mac, iOS or Android apps, uses a monolithic toolchain (Gradle, Nix, Bazel) with no exceptions, or depends heavily on Windows or Mac runners.
2. POC: pick one workflow with a hair-on-fire problem (cannot run across dev and CI or across CIs, brittle glue, poor caching, painful to change), doable within a week, and within your authority. Choose language to maximize team participation; consider one module per language silo (cross-language linking works). Check SDK availability.
3. Integrate with the dev toolchain: prefer documented `dagger call` commands; wrapping them in make or scripts is fine; embedding Dagger as a library is a last resort (core API only, no modules).
4. Integrate with CI: decide trigger events, map environment inputs to function arguments, write the `dagger call` per workflow, follow the platform page. Run old and new CI in parallel to compare.
5. Expand: incrementally (safest) or all-in alongside a CI migration.
6. Spin out reusable modules: start in one module, extract sub-modules, centralize shared modules for multiple teams, optionally publish to the Daggerverse.

## CI notes from the page

- Dagger workflows are not distributed: one `dagger call` uses one engine. Split large workflows into several calls and let CI dispatch them.
- Ephemeral CI runners start with an empty Dagger cache, so CI can feel slower than local. Add persistent storage for Dagger state; no workflow logic change is needed.
- CI config usually shrinks to enough `dagger call` steps to keep proprietary features such as job scaling and visualization.

## Monorepo patterns

- Top-level orchestrator module with a sub-module per component, modelling logical dependencies. Good when projects differ (SDKs, CLIs, web apps, docs). Benefits: easier debugging, reuse, concurrency from the orchestrator.
- One shared module all projects use. Good when projects are alike (e.g. only microservices). Benefits: reuse, less onboarding friction, shared best practices.
- Layer cache makes unnecessary CI jobs finish almost instantly; CI event filters are a secondary, non-portable optimization.

Related: computing-software.devops-ci-cd.dagger.module-testing-patterns.

## Checked

2026-11-07

Read in full from the Dagger docs source (versioned_docs/version-0.21): reference/best-practices/adopting.mdx and monorepos.mdx. Every phase, red flag, POC criterion, CI note and monorepo pattern in the skill matched the page text. No corrections needed.

Method: documentation only; no commands were run.
