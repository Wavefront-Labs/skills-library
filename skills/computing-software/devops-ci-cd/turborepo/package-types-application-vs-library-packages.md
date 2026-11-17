---
id: computing-software.devops-ci-cd.turborepo.package-types-application-vs-library-packages
name: package-types-application-vs-library-packages
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, package-types, application-package, library-package, package-graph, apps-directory, end-to-end-testing, internal-packages]
level: intro
status: docs-checked
description: "Distinguish Application Packages (deployed, ends of the graph) from Library Packages (shared code) and know the rare exception for installing apps."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/package-types.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo talks about two kinds of packages.

**Application Packages** are deployed from your workspace: Next.js, Svelte, Vite or CLI applications, commonly found in `./apps`. Best practice is that they are the **end** of the Package Graph: they are not installed into other packages. CI/CD pipelines usually finish at these nodes of the Package and Task Graphs.

**Installing an application into another package** should be the exception, and if you do it often the docs suggest rethinking your package structure. The documented example is a package that handles end-to-end testing: once the Application Package is installed there, the e2e package can depend on it and so knows about re-deploys of the application.

**Library Packages** contain code you intend to share around the workspace. They are not independently deployable; they support Application Packages to create the final deployables of the repository. You may also call them Internal Packages, which have their own sub-types (just-in-time, compiled, publishable; see the compilation strategies skills).

## Checked

2026-11-04. Read the Package types page in full: both package types, the end-of-graph best practice, the rare exception and the e2e example match. Removed the invented Verify step.

Method: documentation only; no commands were run.
