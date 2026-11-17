---
id: computing-software.devops-ci-cd.turborepo.turborepo-what-it-is-and-problem-it-solves
name: turborepo-what-it-is-and-problem-it-solves
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, monorepo, build-system, remote-cache, task-scheduling, incremental-adoption, single-package-workspace, package-json-scripts]
level: intro
status: docs-checked
description: "What Turborepo is, why monorepos struggle to scale, and how caching, scheduling and incremental adoption address it."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo is described in its docs as the build system for coding agents, designed for scaling monorepos and also making workflows in single-package workspaces faster.

**The monorepo problem.** Monorepos have many advantages but struggle to scale: each workspace has its own test suite, linting and build, and a single monorepo might have thousands of tasks to execute. The docs illustrate three packages taking 110, 140 and 90 seconds. Slow feedback loops hurt how teams build software.

**The solution.** With Turborepo the same repo can hit cache and complete all three packages' tasks in milliseconds (80 ms in the docs' picture). Two mechanisms:
- **Remote Cache** stores the result of all your tasks, so CI never needs to do the same work twice.
- **Task scheduling**: building, then testing, then linting is hard to schedule by hand; Turborepo schedules tasks for maximum speed, parallelising work across all available cores.

**Adoption.** It can be adopted incrementally and added to any repository in a few minutes. It uses the `package.json` scripts you already wrote, the dependencies you already declared and a single `turbo.json` file. It works with any package manager (`npm`, `yarn`, `pnpm` named) because it leans on npm ecosystem conventions.

For help with jargon the docs link to a glossary page, and questions go to GitHub Discussions, Vercel Community and Twitter.

## Checked

2026-11-04. Read the Introduction page in full: the description, the 110/140/90 second and 80 millisecond figures, the two mechanisms and the adoption claims match. Removed the "four paths" sentence, which is on the Getting started page and was not checked here, and the invented Verify step.

Method: documentation only; no commands were run.
