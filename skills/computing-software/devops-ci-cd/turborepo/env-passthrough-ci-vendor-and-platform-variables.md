---
id: computing-software.devops-ci-cd.turborepo.env-passthrough-ci-vendor-and-platform-variables
name: env-passthrough-ci-vendor-and-platform-variables
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, passthroughenv, globalpassthroughenv, ci-variables, platform-environment-variables, vercel-env, turbo-platform-env-disabled]
level: advanced
status: docs-checked
description: "Expose variables to tasks without hashing them via passThroughEnv, account for CI vendor variables in Strict Mode, and note the Vercel platform check."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/using-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Passthrough variables.** In advanced cases a task needs a variable available at runtime without it affecting the hash: changes do not affect outputs, but the task cannot run successfully without them. Add them to `globalPassThroughEnv` and `passThroughEnv`.

**CI vendor compatibility.** Strict Mode filters out environment variables that come from your CI vendors until you account for them with `env`, `globalEnv`, `passThroughEnv` or `globalPassThroughEnv`. If any of these matter to your tasks and are not covered by Framework Inference, include them in `turbo.json`.

**Platform Environment Variables.** When deploying on Vercel you probably already have environment variables configured on the project. Turborepo automatically checks them against your `turbo.json` to confirm you have accounted for them, and warns about missing ones. Disable this with `TURBO_PLATFORM_ENV_DISABLED=true`.

Choosing between keys:
- Value must change the cache key: `env` or `globalEnv`.
- Value must be available but must not change the cache key: `passThroughEnv` or `globalPassThroughEnv`.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/using-environment-variables); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
