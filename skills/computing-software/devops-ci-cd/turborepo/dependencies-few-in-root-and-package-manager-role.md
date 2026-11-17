---
id: computing-software.devops-ci-cd.turborepo.dependencies-few-in-root-and-package-manager-role
name: dependencies-few-in-root-and-package-manager-role
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, root-dependencies, repository-tools, husky, lint-staged, module-resolution, node-modules-location, package-manager-role]
level: practitioner
status: docs-checked
description: "Root dependencies should be repository-management tools only; Turborepo does not manage dependencies, resolution differs per package manager, and node_modules locations vary."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/managing-dependencies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Few dependencies in the root.** Installing dependencies where used leaves few in the root. Only **tools for managing the repository** belong in the workspace root; dependencies for building apps and libraries go in their packages. Examples: `turbo`, `husky`, `lint-staged`.

**Turborepo does not manage dependencies.** Your package manager downloads the right versions, symlinks and resolves modules. The recommendations are best practices, not enforced by Turborepo.

**Module resolution differs** among package managers, giving behaviour that is hard to predict. The docs' coverage is best effort; adapt for your package manager or repo. If documentation looks universally wrong, file a GitHub issue.

**`node_modules` locations.** Depending on package manager, version, settings and where you install, dependencies may sit in the root `node_modules`, in packages' `node_modules`, or both. As long as scripts and tasks find what they need, the package manager is working.

**Do not reference `node_modules` directly** (for example `node ./node_modules/a-package/dist/index.js`). The layout is not part of package managers' public API, so a dependency's location can change with other dependency changes. Rely on Node.js ecosystem conventions to access modules.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/managing-dependencies); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
