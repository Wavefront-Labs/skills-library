---
id: computing-software.devops-ci-cd.turborepo.root-package-json-devengines-and-lockfile
name: root-package-json-devengines-and-lockfile
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, root-package-json, devengines, lockfile, private-true, turbo-run-scripts, reproducible-builds, devdependencies]
level: practitioner
status: docs-checked
description: "A root package.json is private, wraps turbo run scripts, pins turbo and devEngines.packageManager; a lockfile is needed for predictable turbo behaviour."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/structuring-a-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The root `package.json` is the base for the workspace. The docs' common example:

```json
{
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint"
  },
  "devDependencies": { "turbo": "latest" },
  "devEngines": {
    "packageManager": { "name": "pnpm", "version": "9.0.0" }
  }
}
```

That is the docs' pnpm example. Notes per package manager in the docs: the yarn, npm, bun and nub examples add `"workspaces": ["apps/*", "packages/*"]` (pnpm declares packages in `pnpm-workspace.yaml` instead, so its example omits it). Example `devEngines.packageManager` versions shown are pnpm 9.0.0, yarn 1.22.19, npm 10.0.0, bun 1.2.0 and nub 0.8.3. For aube the workspace file is `aube-workspace.yaml`.

**Lockfile.** A lockfile is key to reproducible behaviour for both your package manager and `turbo`. Turborepo also uses the lockfile to understand dependencies between Internal Packages in the workspace. Without a lockfile present when you run `turbo`, you may see unpredictable behaviour (a warning in the docs).

## Checked

2026-11-04. Read the Root `package.json` and Package manager lockfile sections of the Structuring a repository page: the example, `devEngines` versions for each package manager, `aube-workspace.yaml` and the lockfile wording match. Corrected the example, which mixed the pnpm example with a `workspaces` key the pnpm example does not have. Removed the invented Verify step.

Method: documentation only; no commands were run.
