---
id: computing-software.devops-ci-cd.turborepo.configuring-tasks-with-key-and-side-effects
name: configuring-tasks-with-key-and-side-effects
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, with-key, persistent, long-running-tasks, cache-false, deploy-task, side-effects, dev-task]
level: advanced
status: docs-checked
description: "Run a companion long-running task with the with key since a persistent task cannot be depended on, and mark side-effect tasks such as deploy with cache false."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Long-running tasks with runtime dependencies.** A long-running task never exits, so nothing can depend on it. When a task needs another task running at the same time, use the `with` key. In `apps/web/turbo.json` (a Package Configuration):

```json
{ "tasks": { "dev": { "with": ["api#dev"], "persistent": true, "cache": false } } }
```

Whenever `web#dev` runs, `api#dev` runs too.

**Performing side-effects.** Some tasks must always run no matter what, like a deployment script after a cached build. Add `"cache": false`:

```json
{
  "tasks": {
    "deploy": { "dependsOn": ["^build"], "cache": false },
    "build": { "outputs": ["dist/**"] }
  }
}
```

`build` stays cacheable with outputs; `deploy` always executes after dependencies' builds.

**Package Configurations and composition.** Package Configurations are `turbo.json` files placed in a package so it can define behaviour for its own tasks without affecting the rest of the repo; useful in large monorepos with many teams. They can be composed: extend shared configuration packages, and use the `$TURBO_EXTENDS$` microsyntax to add to inherited arrays such as `outputs` and `env` instead of replacing them (see the package configuration reference skills).

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/configuring-tasks); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
