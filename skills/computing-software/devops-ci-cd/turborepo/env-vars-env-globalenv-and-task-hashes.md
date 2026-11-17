---
id: computing-software.devops-ci-cd.turborepo.env-vars-env-globalenv-and-task-hashes
name: env-vars-env-globalenv-and-task-hashes
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, environment-variables, env-key, globalenv, task-hash, wildcards, cache-correctness, preview-vs-production]
level: practitioner
status: docs-checked
description: "Account for environment variables with env (per task) and globalEnv (all tasks) so that value changes miss cache; failing to do so can ship the wrong configuration."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/using-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three questions for environment variables in Turborepo: are they in the task hash, which Environment Mode applies, and have `.env` files been handled?

**Failing to account for environment variables can ship your app with the wrong configuration**, such as preview deployments shipped to production. Turborepo also reads its own System Environment Variables; this page is about your tasks' variables.

Use `env` and `globalEnv` in `turbo.json`:

```json
{
  "globalEnv": ["IMPORTANT_GLOBAL_VARIABLE"],
  "tasks": { "build": { "env": ["MY_API_URL", "MY_API_KEY"] } }
}
```

- **`globalEnv`**: a change in any listed variable's value changes the hash of **all** tasks.
- **`env`**: changes affect only that task, giving finer granularity. A `lint` task probably should not miss cache when `API_KEY` changes, but `build` likely should.

Wildcards are supported so you can account for all variables with a given prefix (see the `env` wildcards reference).

Verify: change a listed variable's value and re-run; the task should miss cache.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/using-environment-variables); commands, flags, key names, defaults and example values were matched against it. Removed: nothing; every claim matched.

Method: documentation only; no commands were run.
