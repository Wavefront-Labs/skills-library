---
id: computing-software.devops-ci-cd.turborepo.upgrading-to-turborepo-2-codemod-and-package-manager
name: upgrading-to-turborepo-2-codemod-and-package-manager
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, upgrade-2-0, turbo-codemod, migrate, devengines, packagemanager-field, eslint-config-turbo-upgrade, breaking-changes]
level: practitioner
status: docs-checked
description: "Upgrade from 1.x to 2.0 by running @turbo/codemod migrate, adding a package manager declaration and updating eslint-config-turbo."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/upgrading.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Step 1: update `turbo.json`.** Run the codemod:

```bash
npx @turbo/codemod migrate
```

(also `pnpm dlx`, `yarn dlx`, `bunx`, `nubx`, `aubx`). It updates your `turbo.json` files for many of the 1.x to 2.0 breaking changes and adds a `name` field to any workspace `package.json` lacking one. Each codemod can be run individually (see the codemods reference).

**Step 2: declare the package manager.** Turborepo 2.0 requires a package manager declaration, for stability and predictability. Add `devEngines.packageManager` to the root `package.json`, for example:

```json
{ "devEngines": { "packageManager": { "name": "pnpm", "version": "9.2.0" } } }
```

Docs examples: yarn 1.22.19, npm 10.8.1, bun 1.2.0, nub 0.8.3, aube 2.2.9. The legacy top-level `packageManager` field is also supported for backwards compatibility.

**Step 3: update `eslint-config-turbo`** to match your major version if you use it; it helps identify environment variables that belong in the `env` key.

**Step 4: review `turbo run` behaviour changes** (next skill).

## Checked

2026-11-04. Read the "Upgrading to 2.0" page in full: the codemod command per package manager, the `name` field addition, the `devEngines.packageManager` requirement and example versions, and the `eslint-config-turbo` step match. Removed the invented Verify step.

Method: documentation only; no commands were run.
