---
id: computing-software.devops-ci-cd.turborepo.internal-package-best-practices-single-purpose
name: internal-package-best-practices-single-purpose
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, internal-package-design, single-purpose-packages, shared-code, application-packages, prune, package-boundaries]
level: practitioner
status: docs-checked
description: "Give each Internal Package one purpose, keep shared code out of Application Packages, and treat apps as entry points to the Package Graph."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/creating-an-internal-package.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**One purpose per package.** Not a strict rule; it depends on repository, scale, organisation and team needs. Advantages:
- *Easier to understand*: developers find code more easily as the repo scales.
- *Fewer dependencies per package*, so Turborepo can prune the dependencies of the package graph more effectively.

Examples from the docs:
- `@repo/ui`: all shared UI components.
- `@repo/tool-specific-config`: configuration for one tool.
- `@repo/graphs`: a domain-specific library for creating and manipulating graphical data.

**Application Packages do not contain shared code.** Put shared code in a separate package that apps depend on. Application Packages are not meant to be installed into other packages; think of them as entry points to the Package Graph. The docs note there are rare exceptions; the Package Types page gives a package that handles end-to-end testing as the example.

## Checked

2026-11-04. Read the "Best practices for Internal Packages" section of the Creating an Internal Package page in full: one-purpose advice, the two advantages, the three example packages, and the Application Package rule all match. The e2e exception was confirmed on the Package Types page. Removed the invented rule of thumb and Verify step.

Method: documentation only; no commands were run.
