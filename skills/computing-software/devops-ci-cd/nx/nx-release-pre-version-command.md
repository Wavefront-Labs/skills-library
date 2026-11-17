---
id: computing-software.devops-ci-cd.nx.nx-release-pre-version-command
name: nx-release-pre-version-command
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, build, preversioncommand, docker, release-groups]
level: practitioner
status: docs-checked
description: "Run a build before nx release applies versions using preVersionCommand and groupPreVersionCommand, including the Docker variant and its default."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/build-before-versioning.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make sure dist output exists before the new version is written to the package manifest.

Global command, in `nx.json`:

```json
{ "release": { "version": { "preVersionCommand": "npx nx run-many -t build" } } }
```

Any command is allowed, including non-nx ones. It is typically needed when publishing from a custom dist directory, because the dist `package.json` must exist before the version is applied to it.

Per release group (members versioned together), use `groupPreVersionCommand`; it runs in addition to the global `preVersionCommand`:

```json
{ "release": { "groups": { "my-group": {
  "projects": ["my-lib-one", "my-lib-two"],
  "version": { "groupPreVersionCommand": "npx nx run-many -t build -p my-lib-one,my-lib-two" }
} } } }
```

Docker images use a separate section, `release.docker`:

```jsonc
{ "release": { "docker": { "preVersionCommand": "npx nx run-many -t docker:build" } } }
```

If the Docker `preVersionCommand` is not set, the default is `npx nx run-many -t docker:build`, building every project that has a `docker:build` target. For groups use `release.groups.<name>.docker.groupPreVersionCommand` (e.g. `npx nx run-many -t docker:build -p api,microservice`); it also runs in addition to the global Docker `preVersionCommand`.

Note the JS key lives under `version`, the Docker key directly under `docker`.

## Checked

2026-11-07. Confirmed against Build Before Versioning: version.preVersionCommand and its run-many example, any command allowed, the custom dist directory reason, groupPreVersionCommand running in addition to the global command, release.docker.preVersionCommand with its default of npx nx run-many -t docker:build, and the group-level docker.groupPreVersionCommand example. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
