---
id: computing-software.devops-ci-cd.verdaccio.scoped-vs-global-registry-and-publishconfig
name: scoped-vs-global-registry-and-publishconfig
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [scoped-registry, publishconfig, registry-routing, scope-routing, publishconfig-registry, registry-choice, client-setup]
level: practitioner
status: docs-checked
description: "Choose between routing only your scope or everything through Verdaccio, per-command registry flags, and publishConfig.registry to stop private packages reaching npmjs."
sources:
  - https://verdaccio.org/docs/cli-registry/
  - https://verdaccio.org/docs/linking-remote-registry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pointing a client at Verdaccio is four steps: set the registry, authenticate, publish, and keep the lockfile from undoing it.

Option 1, route only your scope (safer default for a team):
```
registry=https://registry.npmjs.org/
@my-company:registry=http://localhost:4873/
```
Public packages are unaffected and a registry outage does not block `lodash`. The trade-off is no caching of public packages and no single place to apply rules. Limits of scope routing: scopes only, exact match, one registry per scope, and tokens in `.npmrc` (read from env with `${VERDACCIO_TOKEN}`).

Option 2, route everything and let Verdaccio proxy npmjs:
```
registry=http://localhost:4873/
```
One registry, one policy point, a cache of all installs (builds survive an npmjs outage), but the registry is on the critical path of every install.

Option 3, one command: `--registry <url>` (not persisted, not carried to a later publish).

Prevent accidental publishes elsewhere:
```json
{ "publishConfig": { "registry": "http://localhost:4873/" } }
```
It beats local configuration. Lockfiles record resolved URLs (`pnpm-lock.yaml`, npm `resolved`), so mixed hosts can fail; re-resolve when switching.

Comparison: config file `.npmrc` (pnpm, npm), `.yarnrc.yml` (Yarn 4); Bun reads `.npmrc` too.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Using a private registry (cli-registry) and Linking a Remote Registry. Confirmed: the four steps, scope-only and global routing with their trade-offs, the four scope-routing limits, the token from the environment, --registry per command, publishConfig, lockfile resolved URLs and the config file per client. Removed or corrected: nothing.

Method: documentation only; no commands were run.
