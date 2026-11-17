---
id: computing-software.devops-ci-cd.turborepo.add-turborepo-to-existing-repository-steps
name: add-turborepo-to-existing-repository-steps
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, existing-repository, turbo-json, gitignore, devengines, packagemanager, workspaces, pnpm-workspace, dangerouslydisablepackagemanagercheck]
level: practitioner
status: docs-checked
description: "Step-by-step adoption: install turbo, add turbo.json with build/check-types/dev, ignore .turbo, declare devEngines.packageManager, set workspaces, run."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/add-to-existing-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo can be adopted incrementally in any single or multi-package repository. You do not have to run all tasks for all packages at once; start with one task in a few packages.

1. **Install `turbo`** globally and pin it at the root. For pnpm create `pnpm-workspace.yaml` first, otherwise `pnpm add turbo --save-dev --workspace-root` errors with `--workspace-root may only be used inside a workspace`.
2. **Add `turbo.json`** at the root. Next.js example:

```json
{
  "$schema": "https://turborepo.dev/schema.json",
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": [".next/**", "!.next/cache/**", "!.next/dev/**"] },
    "check-types": { "dependsOn": ["^check-types"] },
    "dev": { "persistent": true, "cache": false }
  }
}
```

For Vite, `build` has `"outputs": ["dist/**"]`. Add a `check-types` script (`tsc --noEmit`). If a Vite starter has `"build": "tsc && vite build"`, split into `build: vite build` and `check-types: tsc --noEmit` so `turbo` can run them in parallel.
3. **Edit `.gitignore`**: add `.turbo`, which the CLI uses to persist logs, outputs and more.
4. **Declare the package manager** with `devEngines.packageManager` (`name` and `version`) in the root `package.json`; the legacy top-level `packageManager` field is also supported. Use `dangerouslyDisablePackageManagerCheck` only while migrating.
5. **Workspaces** (multi-package only): pnpm `pnpm-workspace.yaml` with `packages: ["apps/*", "packages/*"]`; yarn, npm, bun and nub use a `workspaces` array in `package.json`; aube uses `aube-workspace.yaml`.
6. **Run** `turbo build check-types`; run again with no changes and the output shows cached tasks and `>>> FULL TURBO`.
7. **`turbo dev`** starts dev tasks for all packages; little value in a single-package workspace since dev outputs are not cached and there is one script.

Verify: second run prints `Cached: 2 cached, 2 total`.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: getting-started/add-to-existing-repository); commands, flags, key names, defaults and example values were matched against it. Removed: nothing; every claim matched.

Method: documentation only; no commands were run.
