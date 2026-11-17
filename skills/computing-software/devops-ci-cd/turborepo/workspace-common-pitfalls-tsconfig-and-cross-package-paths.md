---
id: computing-software.devops-ci-cd.turborepo.workspace-common-pitfalls-tsconfig-and-cross-package-paths
name: workspace-common-pitfalls-tsconfig-and-cross-package-paths
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, pitfalls, root-tsconfig, package-boundaries, relative-imports, shared-tsconfig, workspace-hygiene]
level: practitioner
status: docs-checked
description: "Two structure pitfalls: a root tsconfig you likely do not need, and reaching across packages with ../ instead of installing the dependency."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/structuring-a-repository.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two common pitfalls from the Structuring a repository guide:

1. **Root `tsconfig.json`.** If you use TypeScript, you likely do not need a `tsconfig.json` in the root of the workspace. Packages should independently specify their own configuration, usually building off a shared `tsconfig.json` from a separate package in the workspace. The TypeScript guide has the details under "You likely don't need a tsconfig.json file in the root of your project".

2. **Crossing package boundaries.** Avoid accessing files across package boundaries as much as possible. If you ever find yourself writing `../` to get from one package to another, you likely have an opportunity to rethink: install the package where it is needed and import it in your code.

Related structure rule: treat each package as its own unit, with its own `package.json`, tooling configuration and source code. The docs call this a good mental model to start from, with limits.

## Checked

2026-11-04. Read the "Common pitfalls" and "Anatomy of a package" intro of the Structuring a repository page; both pitfalls match. Removed the unsupported claim about Package Graph accuracy and cache invalidation, the unsupported next-step line, and the invented Verify step. Thin skill: two bullet points of content.

Method: documentation only; no commands were run.
