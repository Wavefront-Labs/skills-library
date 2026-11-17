---
id: computing-software.devops-ci-cd.turborepo.install-turbo-global-binary-and-pin-in-repository
name: install-turbo-global-binary-and-pin-in-repository
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, install-turbo, global-install, local-turbo, create-turbo, devdependency, install-script, support-policy]
level: intro
status: docs-checked
description: "Install the standalone turbo binary globally, pin a version as a root devDependency so the local copy takes precedence, and use create-turbo."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/installation.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start a new repo with `create-turbo` (`npx create-turbo@latest`, `pnpm dlx create-turbo@latest`, `yarn dlx create-turbo@latest`, `bunx create-turbo@latest`). The starter has two deployable applications and three shared libraries; see the basic starter README on GitHub.

**Global installation** brings flexibility and speed to local workflows:

```sh
curl -fsSL https://turborepo.dev/install | sh    # macOS and Linux
irm https://turborepo.dev/install.ps1 | iex      # Windows x64, PowerShell
```

The binaries are also available in the GitHub release assets, starting with 2.11.5; for older versions use your package manager. See the support policy for supported platforms.

After installing you can run: `turbo build` (build scripts in dependency order), `turbo build --filter=docs --dry` (print an outline of the `docs` build without running it), `turbo generate` (generators), and `cd apps/docs && turbo build` (the package and its dependencies, Automatic Package Scoping). **`turbo` is an alias for `turbo run`.**

**Repository installation** pins the version used by the repo: add `turbo` as a root `devDependency` (`pnpm add turbo --save-dev --ignore-workspace-root-check`, `yarn add turbo --dev --ignore-workspace-root-check`, `npm install turbo --save-dev`, `bun install turbo --dev`). When you invoke the global binary inside the repo it **defers to the installed local version**.

For CI see the Constructing CI page section on global turbo.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: getting-started/installation, getting-started/index); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
