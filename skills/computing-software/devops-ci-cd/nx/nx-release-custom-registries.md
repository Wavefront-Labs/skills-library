---
id: computing-software.devops-ci-cd.nx.nx-release-custom-registries
name: nx-release-custom-registries
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, npm, registry, npmrc, publish, scopes]
level: practitioner
status: docs-checked
description: "Publish with nx release to private or multiple npm registries via .npmrc scopes, per-project registry options and CI auth tokens."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/configure-custom-registries.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send packages to a registry other than https://registry.npmjs.org/ (GitHub Packages, Artifactory, Azure Artifacts, Verdaccio).

Nx Release publishes through the npm CLI, so configure the root `.npmrc`:

```
registry=https://my-custom-registry.com/
//my-custom-registry.com/:_authToken=<TOKEN>
```

The second line is the CI authentication token.

Multiple registries (recommended): use npm scopes.

```
@my-scope:registry=https://my-custom-registry.com/
//my-custom-registry.com/:_authToken=<TOKEN>
@other-scope:registry=https://my-other-registry.com/
//my-other-registry.com/:_authToken=<OTHER_TOKEN>
registry=https://my-default-registry.com/
//my-default-registry.com/:_authToken=<DEFAULT_TOKEN>
```

`@my-scope/pkg-1` goes to the first, `@other-scope/pkg-2` to the second, unscoped `pkg-3` to the default.

Per-package registry (project.json). Two parts:

1. Version step, only if `version.currentVersionResolver` is `registry`:
```json
{ "release": { "version": { "currentVersionResolverMetadata": { "registry": "https://my-unique-registry.com/", "tag": "next" } } } }
```
2. Publish step, options on the `nx-release-publish` target:
```json
{ "targets": { "nx-release-publish": { "options": { "registry": "https://my-unique-registry.com/", "tag": "next" } } } }
```

Tokens for per-package registries must still be in the root `.npmrc` in CI.

Gotcha: avoid `publishConfig.registry` in package.json. `npm publish` prefers it over `--registry`, so Nx Release's `--registry` option (and the programmatic API) cannot override it, breaking e.g. local end-to-end publishing. See nx-release-local-registry for testing against Verdaccio.

## Checked

2026-11-07. Confirmed against Configure Custom Registries: npm CLI under the hood, root .npmrc registry and _authToken lines, scope-based multi-registry example and its three package mappings, per-project currentVersionResolverMetadata and nx-release-publish registry and tag options, the authentication note, and the publishConfig warning. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
