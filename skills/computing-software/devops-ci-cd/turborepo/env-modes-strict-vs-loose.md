---
id: computing-software.devops-ci-cd.turborepo.env-modes-strict-vs-loose
name: env-modes-strict-vs-loose
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, environment-modes, strict-mode, loose-mode, env-mode-flag, cache-safety, unintended-cache-hits]
level: advanced
status: docs-checked
description: "Strict Mode (default) filters task runtime variables to env and globalEnv; Loose Mode exposes all but can restore a stale build from cache."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/using-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environment Modes control which environment variables a task sees at runtime.

**Strict Mode (default)** filters the runtime environment to **only** variables in `globalEnv` and `env`. Tasks that do not account for every variable they need are likely to fail, which is good because you do not want to cache a task that could behave differently in another environment. Warning: it does not guarantee failure. If the app gracefully handles a missing variable, a task can still complete and you can get unintended cache hits.

**Loose Mode** does not filter variables by `globalEnv` and `env`, making it easier to migrate incrementally to Strict Mode. Enable it per invocation with `--env-mode`:

```bash
turbo run build --env-mode=loose
```

As long as the variable exists when `turbo` runs, the script can use it. The danger: you can forget to account for a variable and hit cache when you should not.

The docs' example: code does `fetch(`${process.env.MY_API_URL}/resource/1`)`. You build with a preview `MY_API_URL`, then build for production and see a **cache hit** even though the value changed, so Turborepo restores the preview-pointed build. In Loose Mode the variable is available at runtime even though it is not in the task hash. Prefer Strict Mode so this misconfiguration is more likely to fail.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/using-environment-variables); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
