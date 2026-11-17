---
id: computing-software.devops-ci-cd.turborepo.ci-best-practices-rely-on-caching-and-troubleshooting
name: ci-best-practices-rely-on-caching-and-troubleshooting
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, ci-best-practices, turbo-run, subcommand-collision, cache-troubleshooting, missing-outputs, wrong-environment, lint-check-types-test]
level: practitioner
status: docs-checked
description: "Keep CI simple with turbo run lint check-types test and turbo build --filter, always write turbo run in CI, and diagnose broken cache hits."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/constructing-ci.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Rely on caching.** Caching and Remote Caching let you build fast pipelines with minimal complexity. Two commands can cover quality checks and building a target app:

- `turbo run lint check-types test`: quality checks for the whole repository; unchanged packages hit cache.
- `turbo build --filter=web`: builds `web` using the registered `build` task; if `web` and its dependencies have not changed, this hits cache too.

Optimise further only after this baseline.

**Use `turbo run` in CI.** `turbo` is an alias for `turbo run`, but subcommands such as `turbo prune` and `turbo generate` exist, and more may be added. A CI step like `turbo deploy` could collide with a future `deploy` subcommand; `turbo run deploy` avoids that.

**Troubleshooting**
- *Hitting cache results in broken builds*: if a task passes when missing cache but fails when hitting it, you likely have not configured the `outputs` key correctly.
- *Deployment uses the wrong environment variables*: if `env` or `globalEnv` is not defined for a task, Turborepo cannot use the variables for hashing, so a task can hit cache despite a different environment. Check those keys.

Next steps from the guide: the Guides section for specific use cases and Core Concepts for depth.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/constructing-ci); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
