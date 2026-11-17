---
id: computing-software.devops-ci-cd.turborepo.create-internal-package-math-compiled-walkthrough
name: create-internal-package-math-compiled-walkthrough
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, create-internal-package, compiled-package, tsc-build, package-name-import, tsconfig-extends, outdir-rootdir, exports-types-default]
level: practitioner
status: docs-checked
description: "Build the @repo/math internal package: package.json name and exports, tsconfig extending the shared base, src files, and why the name is the import path."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/creating-an-internal-package.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Internal Packages are the building blocks of a workspace. Turborepo reads their `package.json` dependencies to build the Package Graph. The guide builds `./packages/math` with the Compiled Package pattern in a `create-turbo`-style repo.

**1. Directory and package.json.** The `name` determines how the package is imported everywhere (`@repo/math` means `import { add } from '@repo/math/add'`); renaming means updating all imports.

```json
{
  "name": "@repo/math",
  "type": "module",
  "scripts": { "dev": "tsc --watch", "build": "tsc" },
  "exports": {
    "./add": { "types": "./src/add.ts", "default": "./dist/add.js" },
    "./subtract": { "types": "./src/subtract.ts", "default": "./dist/subtract.js" }
  },
  "devDependencies": { "@repo/typescript-config": "workspace:*", "typescript": "latest" }
}
```

(The npm tab uses `"*"` instead of `workspace:*`.) Because it depends on `@repo/typescript-config`, Turborepo treats `@repo/math` as a dependent of it when ordering tasks.

**2. tsconfig.json** at the package root:

```json
{
  "extends": "@repo/typescript-config/base.json",
  "compilerOptions": { "outDir": "dist", "rootDir": "src" },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

`outDir` matches the directory in `exports`; `rootDir` keeps the output structure the same as `src`; `include` and `exclude` are not inherited from the base config per the TypeScript specification, so they are repeated here.

**3. Source:** `src/add.ts` exports `add = (a, b) => a + b` and `src/subtract.ts` exports `subtract`; they map to the `dist` outputs `tsc` creates.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/creating-an-internal-package); commands, flags, key names, defaults and example values were matched against it. Removed: the claim that yarn uses a bare star version for the typescript-config dependency (the page uses workspace:* for yarn, star only for npm).

Method: documentation only; no commands were run.
