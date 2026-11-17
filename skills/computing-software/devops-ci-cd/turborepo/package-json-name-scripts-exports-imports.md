---
id: computing-software.devops-ci-cd.turborepo.package-json-name-scripts-exports-imports
name: package-json-name-scripts-exports-imports
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, package-name, namespace-prefix, exports-field, imports-field, barrel-files, conditional-exports, repo-namespace, subpath-imports]
level: practitioner
status: docs-checked
description: "Fields that matter in a workspace package.json: unique scoped name, scripts that become tasks, exports instead of barrel files, and optional imports."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/structuring-a-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Think of each package as its own small project with a `package.json`, tooling configuration and source code, with specific entrypoints other packages can use.

- **`name`** identifies the package and should be unique in the workspace. Use a namespace prefix for Internal Packages to avoid conflicts with the npm registry, such as `@acme/package-name`. The docs use `@repo` because it is an unused, unclaimable namespace on npm.
- **`scripts`**: Turborepo uses the script names to decide what to run (if anything) in a package.
- **`exports`** specifies the entrypoints other packages import. For a `@repo/math` package:

```json
{
  "exports": {
    ".": "./src/constants.ts",
    "./add": "./src/add.ts",
    "./subtract": "./src/subtract.ts"
  }
}
```

That example uses the Just-in-Time pattern (exports TypeScript directly); a Compiled package could be used instead. It requires modern Node.js and TypeScript.

**Three benefits of `exports`:** it avoids barrel files (which are hard for compilers and bundlers and cause performance problems); it has more power than `main`, such as Conditional Exports (prefer `exports` over `main`); and it gives IDE auto-completion for the package's entrypoints.

- **`imports`** (optional) creates subpaths to modules within your package, shortcuts resilient to refactors. As of TypeScript 5.4, TypeScript can infer subpaths from `imports`, making it a better option than `compilerOptions#paths`; see the TypeScript guide.

Source code commonly lives in `src` and compiles to a `dist` directory inside the package, though not required.

## Checked

2026-11-04. Read the "Anatomy of a package" section of the Structuring a repository page in full: `name` uniqueness and namespace advice, the `@repo` rationale, `scripts`, the `exports` example, the three benefits, `imports` with the TypeScript 5.4 note, and the `src`/`dist` note all match. The page also notes the `exports` example requires modern Node.js and TypeScript. Removed the invented Verify step.

Method: documentation only; no commands were run.
