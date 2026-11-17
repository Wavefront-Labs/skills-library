---
id: computing-software.devops-ci-cd.turborepo.ci-global-turbo-before-install-pin-turbo-version
name: ci-global-turbo-before-install-pin-turbo-version
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, global-turbo, turbo-version, standalone-binary, ci-bootstrap, docker-prune, installer, powershell]
level: advanced
status: docs-checked
description: "Pin the standalone turbo binary with TURBO_VERSION for CI steps that run before dependencies install, such as turbo prune for Docker."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/constructing-ci.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global `turbo` is convenient in CI and enables Automatic Workspace Scoping. But sometimes you run `turbo` before installing packages with your package manager, for example `turbo prune` to build a Docker image. Then global `turbo` cannot defer to the version in `package.json`, because that version's binary has not been installed yet.

For CI steps before dependency installation, **pin the standalone binary to an exact version compatible with your repository's `turbo` dependency**. Set `TURBO_VERSION` when running the installer:

```sh
curl -fsSL https://turborepo.dev/install | TURBO_VERSION=2.11.5 sh
```

```powershell
$env:TURBO_VERSION = '2.11.5'
irm https://turborepo.dev/install.ps1 | iex
```

**Standalone releases start at 2.11.5.** To use an older version install it with your package manager instead.

Where this matters in practice: the Docker guide's example uses `turbo prune` to create a lean image, which runs before dependencies are installed, so the pinned installer is needed there. Once dependencies are installed, global `turbo` defers to the local version from `package.json`, as described in the installation guide. On Windows runners use the PowerShell form, setting `$env:TURBO_VERSION` before piping the installer script.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/constructing-ci); commands, flags, key names, defaults and example values were matched against it. Removed: an unsourced reason for pinning and the Verify step.

Method: documentation only; no commands were run.
