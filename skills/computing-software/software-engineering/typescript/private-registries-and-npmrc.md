---
id: computing-software.software-engineering.typescript.private-registries-and-npmrc
name: private-registries-and-npmrc
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, npmrc, private-registry, scoped-registry, github-packages, dependency-confusion, npm]
level: practitioner
status: verified
description: "Configure .npmrc for private registries: scope-to-registry mapping, auth tokens from env vars, CI setup, GitHub Packages/Artifactory/Verdaccio, and avoiding dependency confusion."
sources:
  - https://docs.npmjs.com/cli/configuring-npm/npmrc
  - https://docs.npmjs.com/cli/using-npm/config
  - https://docs.npmjs.com/cli/commands/npm-whoami
  - https://docs.npmjs.com/cli/commands/npm-ci
  - https://github.com/actions/setup-node/blob/main/docs/advanced-usage.md
  - https://github.com/actions/setup-node/blob/main/action.yml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private registries and .npmrc

**Goal:** install internal packages locally and in CI without committing secrets or
letting a public package hijack an internal name.

## .npmrc levels
npm reads the command line, environment variables (`npm_config_<key>`) and four `.npmrc` files: project (`./.npmrc`, committed), user (`~/.npmrc`), global (`$PREFIX/etc/npmrc`) and built-in; a setting in the user file overrides the global file. Inspect: `npm config list -l`,
`npm config get registry`.

## Scope mapping (committed project .npmrc)
```ini
@acme:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NPM_TOKEN}
```
- Everything `@acme/*` resolves from the private registry; everything else from npmjs.
- `${NPM_TOKEN}` is expanded from the environment at runtime - the file is safe to commit.
- Auth lines are keyed by registry URL without protocol (`//host/path/:_authToken`).

## CI
```yaml
- uses: actions/setup-node@v7
  with: { node-version: 24, registry-url: https://npm.pkg.github.com, scope: "@acme" }
- run: npm ci
  env: { NODE_AUTH_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
```
setup-node writes an .npmrc referencing `NODE_AUTH_TOKEN`. Use read-only tokens for installs,
write tokens only in the publish job.

## Dependency confusion
If an internal package name is **unscoped** (`acme-utils`) and also requested from a registry
chain that includes npmjs, an attacker can publish `acme-utils@99.0.0` publicly and get
installed. Defences:
- Always use a scope you own on npmjs (`@acme`, register it even if unused publicly) and map it.
- `npm ci` with a committed lockfile containing integrity hashes.

## Troubleshooting
- Auth failures: check the identity with `npm whoami --registry=<url>`; auth settings must be scoped to the registry URL (`//host/path/:`) per the npmrc docs.
- A scoped package that cannot be found: check the `@scope:registry` mapping.
- `--loglevel verbose` increases npm's log output.

## Verify
- [ ] No literal tokens in committed files (`git grep _authToken` shows only `${...}`).
- [ ] Fresh clone + `npm ci` works in CI with only the env token provided.

## Checked
Checked 2026-10-25 against the npm CLI docs (npmrc, config, npm-whoami, npm-ci, scope) and the actions/setup-node README, action.yml and advanced-usage (current major v7). Confirmed: the four npmrc files and that user overrides global; `${VAR}` expansion in npmrc; auth settings must be scoped to a registry URL (`//host/path/:`); `@scope:registry` mapping; `npm_config_` environment variables; `npm config list -l` and `npm config get`; `npm whoami`; `npm ci` needs a lockfile; setup-node `registry-url` and `scope` inputs with `NODE_AUTH_TOKEN`. Updated setup-node from v4 to v7. Removed `always-auth` (not in the current npm docs), the proxy-registry vendor claims and the error-code explanations.
Run 2026-11-01 with npm 10.8.2 on Windows (Git Bash), offline, with scratch user and global npmrc files and cache (no registry access; the dependency was a local tarball made by `npm pack`): `npm config get registry` (default `https://registry.npmjs.org/`) and `@acme:registry`; `${VAR}` expansion in `_authToken` (the list shows `(protected)`, the literal value never appeared); precedence: a user file setting beat the global file, and a project `.npmrc` beat the user file, `npm config list -l` naming each source; `npm_config_registry` in the environment overrode the files; `npm ci` needs a lockfile. Not run: `npm whoami`, GitHub Packages, Artifactory and Verdaccio, and the setup-node steps (network or CI; documentation only).

Method: documentation plus commands run (npm 10.8.2, offline).
