---
id: computing-software.devops-ci-cd.verdaccio.yarn-client-setup-and-plugins
name: yarn-client-setup-and-plugins
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [yarn, yarnrc, yarn-plugin, yarn-berry, npmregistryserver, yarn-npm-login, yarn-import]
level: practitioner
status: docs-checked
description: "Configure Yarn 4 for Verdaccio in .yarnrc.yml, log in with --auth-type=legacy, and add missing registry commands via Verdaccio yarn plugins."
sources:
  - https://verdaccio.org/docs/setup-yarn/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Yarn modern ignores `--registry` and `.npmrc`; use `.yarnrc.yml`:

```yaml
npmRegistryServer: 'http://localhost:4873'
unsafeHttpWhitelist:
  - localhost          # only when not using valid https
```
Scoped setup:
```yaml
npmRegistryServer: 'https://registry.npmjs.org'
npmRegistries:
  'https://registry.myverdaccio.org':
    npmAlwaysAuth: true
    npmAuthToken: <TOKEN>
npmScopes:
  my-company:
    npmRegistryServer: https://registry.myverdaccio.org
    npmPublishRegistry: https://registry.myverdaccio.org
```
Unscoped packages still resolve from the public registry; `@my-company/*` resolves and publishes through Verdaccio. `publishConfig.registry` in package.json overrides `npmRegistryServer` on publish. Log in: `yarn npm login --scope my-company`.

Yarn 4 lacks `npm ping`, `unpublish`, `deprecate`, `star`, and `yarn npm login` only speaks the web flow. The experimental (0.0.x) Verdaccio plugins (verdaccio/yarn-plugin-npm) add them; they need Yarn 4.x and Node.js >= 24:
```
yarn dlx @verdaccio/yarn-import npm-ping
yarn dlx @verdaccio/yarn-import npm-login
yarn dlx @verdaccio/yarn-import npm-unpublish
yarn dlx @verdaccio/yarn-import npm-deprecate
yarn dlx @verdaccio/yarn-import npm-star
```
Pin a version by appending it, and in CI. Check with `yarn plugin list`. All accept `--registry <url>`, `--scope <scope>` and `--json`; `unpublish` and `deprecate` also take `--otp <code>`.

With `npm-login` installed, a self-hosted Verdaccio login is `yarn npm login --auth-type=legacy --registry http://localhost:4873`. `--auth-type=auto` is the default (web flow first, legacy on 404/501). In CI pass `--user`, `--password` and `--email`.

Yarn 4.15 defaults `npmMinimalAgeGate` to `1d` (introduced off in 4.10), hiding versions published in the last day, including your own fresh publishes. Exempt your scope with `npmPreapprovedPackages: ['@my-company/*']` or set `npmMinimalAgeGate: 0` under `npmScopes.<scope>`.

Yarn classic reads `.npmrc` plus `.yarnrc` (`registry "http://localhost:4873"`) and needs `always-auth` on (`npm config set always-auth true`) for private installs; it is unmaintained. Staged publishing (`npm stage`) is not available in Yarn.

## Checked

Method: docs-checked 2026-11-09 against the Verdaccio setup-yarn page (website source, read in full); documentation only, no commands were run.
