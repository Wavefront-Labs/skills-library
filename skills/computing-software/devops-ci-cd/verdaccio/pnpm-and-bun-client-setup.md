---
id: computing-software.devops-ci-cd.verdaccio.pnpm-and-bun-client-setup
name: pnpm-and-bun-client-setup
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [pnpm, bun, bunfig, pnpm-login, pnpm-publish, bunfig-toml, minimumreleaseage]
level: practitioner
status: docs-checked
description: "Configure pnpm and bun against Verdaccio: .npmrc registry, pnpm login and publish, _authToken in CI, pnpm 11 differences, and bunfig.toml."
sources:
  - https://verdaccio.org/docs/setup-pnpm/
  - https://verdaccio.org/docs/setup-bun/
  - https://verdaccio.org/docs/cli-registry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm reads the same `.npmrc` files as npm.
```
pnpm config set registry http://localhost:4873/ --location=project
pnpm config get registry
pnpm install --registry http://localhost:4873/
pnpm login --scope=@my-company --registry http://localhost:4873/
pnpm publish --registry http://localhost:4873/
```
Scope-only routing: `@my-company:registry=http://localhost:4873/` in `.npmrc`. In CI skip login and append:
```
echo "//localhost:4873/:_authToken=${VERDACCIO_TOKEN}" >> .npmrc
```
Do not use `_auth` (Basic): Verdaccio 7 rejects it with E401.

pnpm specifics:
- `pnpm publish` runs prepublishOnly and prepack and publishes from a temp directory; `pnpm publish -r` publishes workspace packages not yet on the registry.
- pnpm's own settings live in `pnpm-workspace.yaml`; `pnpm config set <key> --location=project` routes to the right file.
- Since pnpm 11, `search`, `star`, `token`, `whoami`, `owner`, `profile` are not implemented; use npm for them.
- The lockfile stores resolved URLs; after switching registries delete it and reinstall.

bun: create `bunfig.toml`:
```
[install]
registry = "http://localhost:4873"

[install.scopes]
"@scope" = { token = "$npm_token", url = "https://localhost:4873/" }
```
Bun reads `.npmrc` too (client overview page); the bun page sets the token in `bunfig.toml` as shown above.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Setup pnpm, Setup bun and Using a private registry. Confirmed: the pnpm registry and login commands, CI _authToken, the _auth E401 warning, the pnpm specifics, the pnpm 11 unimplemented commands, the lockfile note and the bunfig.toml settings. Removed or corrected: the unconfirmed claim that Bun has no login command and uses the token npm adduser saved.

Method: documentation only; no commands were run.
