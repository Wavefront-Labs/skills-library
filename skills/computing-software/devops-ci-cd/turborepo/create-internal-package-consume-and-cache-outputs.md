---
id: computing-software.devops-ci-cd.turborepo.create-internal-package-consume-and-cache-outputs
name: create-internal-package-consume-and-cache-outputs
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, internal-package-consumer, workspace-dependency, lockfile-update, build-outputs, dist-outputs, build-order, cache-rebuild]
level: practitioner
status: docs-checked
description: "Add the new package to an app as a workspace dependency, reinstall to update the lockfile, add dist/** to build outputs, and watch the app build after the library."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/creating-an-internal-package.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Add the package to an application** (for example `apps/web`) in its `package.json` dependencies: `"@repo/math": "workspace:*"` (or `"*"` for yarn and npm).

Warning from the guide: you changed dependencies, so **run your package manager's install command to update the lockfile**.

Then use it in code, for example in a React page: `add(1, 2)` imported from `@repo/math/add`.

**Edit `turbo.json`** so the library's artifacts are cached. Add `dist/**` to `outputs` of `build`:

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "!.next/dev/**", "dist/**"]
    }
  }
}
```

**Run `turbo build`** (global turbo or the package manager's `build` script, which uses `turbo run build`). `@repo/math` builds before `web`, so the runtime code in `./packages/math/dist` is available when `web` bundles. Run it again and `web` rebuilds in milliseconds thanks to caching.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/creating-an-internal-package); commands, flags, key names, defaults and example values were matched against it. Removed: an inferred reminder paragraph and the Verify step.

Method: documentation only; no commands were run.
