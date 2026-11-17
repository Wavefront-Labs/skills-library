---
id: computing-software.devops-ci-cd.turborepo.create-turbo-examples-and-starter
name: create-turbo-examples-and-starter
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, create-turbo, examples, starter-template, community-examples, core-maintained-examples, example-flag]
level: intro
status: docs-checked
description: "Bootstrap with create-turbo --example using core-maintained or community examples, or any GitHub repository URL."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/examples.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/installation.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`create-turbo` bootstraps a repository, either from the default template or from an example for your favourite tooling.

```bash
# Use an example listed below
npx create-turbo@latest --example [example-name]
# Use a GitHub repository from the community
npx create-turbo@latest --example [github-url]
```

The same forms exist for `pnpm dlx`, `yarn dlx`, `bunx`, `nubx` and `aubx`.

**Core-maintained examples** are maintained by the Turborepo core team: dependencies are kept as up to date as possible and GitHub issues are accepted and addressed.

**Community-maintained examples** are curated by the community to show common tools and libraries with Turborepo. GitHub issues for them are closed; if you find problems, submit a pull request with fixes.

The default starter (via the Installation page) has two deployable applications and three shared libraries; its README is the basic starter on GitHub.

Getting started offers four learning paths: use `create-turbo` (start with a template), use an example (framework-specific), follow the in-depth guides (zero to monorepo), or add to an existing repository (make your current repo fast).

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: getting-started/examples, getting-started/installation, getting-started/index); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
