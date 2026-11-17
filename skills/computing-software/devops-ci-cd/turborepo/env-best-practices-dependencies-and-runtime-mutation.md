---
id: computing-software.devops-ci-cd.turborepo.env-best-practices-dependencies-and-runtime-mutation
name: env-best-practices-dependencies-and-runtime-mutation
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, env-best-practices, package-env, app-env-files, eslint-config-turbo, runtime-mutation, summarize-env, env-from-dependencies]
level: advanced
status: docs-checked
description: "Declare variables a no-build dependency exposes in the consuming app, keep .env files in apps, lint with eslint-config-turbo, and never mutate variables mid-task."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/using-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Variables from dependencies.** When an app consumes a package that relies on environment variables, account for them for cache correctness. Two cases with app `docs` and package `common`:
1. `docs#build` depends on `common#build` (`dependsOn: ["^build"]`) and `common` declares the variable in its own `turbo.json`: Turborepo handles it. Changing the variable makes `common` miss, rebuild, and so `docs` rebuilds.
2. `common` has no build step but exposes variables `docs` reads at build time (like `process.env.MY_VAR`): `docs` **must** declare it directly, for example `apps/docs/turbo.json` with `"build": { "env": ["MY_VAR"] }`.

**`.env` placement.** A root `.env` is not recommended. Put `.env` files in the Application Packages where used: this models runtime behaviour per app and prevents variable leakage across apps as the repo grows. A root `.env` may be easier during incremental migration (tools like dotenv can load from different locations), but aim to drop it afterwards.

**`eslint-config-turbo`** finds variables used in code but missing from `turbo.json`.

**Do not create or mutate variables at runtime.** Turborepo hashes variables at task start. For `"dev": "export MY_VARIABLE=123 && next dev"` the variable is added after the task started, so it is not hashed.

**Troubleshooting:** add `--summarize` to `turbo run` and diff the `globalEnv` and `env` sections to find missing variables.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/using-environment-variables); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
