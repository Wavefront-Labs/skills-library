---
id: computing-software.web-development.node-express.install-scripts-and-typosquatting
name: install-scripts-and-typosquatting
category: computing-software
field: web-development
product: node-express
tags: [vulnerable-dependencies, install-scripts, typosquatting, supply-chain, npm, provenance]
level: practitioner
status: verified
description: "Reducing npm supply-chain risk from install scripts, typosquats and hijacked packages: ignore-scripts, allowlisting builds, provenance, vetting dependencies and CI token scope."
sources:
  - https://docs.npmjs.com/cli/using-npm/scripts#ignoring-scripts
  - https://pnpm.io/settings#allowbuilds
  - https://docs.npmjs.com/generating-provenance-statements
  - https://docs.npmjs.com/trusted-publishers
  - https://github.com/SocketDev/socket-cli
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Install scripts and typosquat risk

## 1. Threat
`preinstall`/`install`/`postinstall` scripts run arbitrary code on developer laptops and CI with access to tokens, SSH keys and cloud creds. Typosquats, maintainer account takeovers and malicious updates in transitive dependencies all use this path.

## 2. Disable scripts by default
```ini
# .npmrc
ignore-scripts=true
```
Then run needed builds explicitly with `npm rebuild esbuild sharp --ignore-scripts=false`: `npm rebuild` obeys `ignore-scripts=true`, so a bare rebuild runs nothing (tested: the dependency's postinstall stayed unrun after `npm rebuild dep` until the flag was added). pnpm does not run unreviewed dependency build scripts; approve packages with `allowBuilds` (pnpm 10.26+; it replaced `onlyBuiltDependencies` in pnpm 11):
```yaml
# pnpm-workspace.yaml
allowBuilds:
  esbuild: true
  sharp: true
```

## 3. Vet new dependencies
- Check exact spelling and the publisher; download counts and repo link; age of the package and of the latest version.
- Look at what it does on install and whether it needs network/fs at all. Tools: `npm view pkg scripts`, Socket CLI (`socket npm install` runs the install through Socket Firewall, which blocks known-malicious packages).
- Prefer fewer, well-maintained dependencies; inline 10-line utilities.
- Use scoped internal packages and configure the registry for your scope to avoid **dependency confusion** (`@acme:registry=https://npm.internal`).

## 4. Provenance and integrity
- Publish from CI with trusted publishing (OIDC, no long-lived tokens; npm CLI 11.5.1+), which generates provenance automatically, or with `npm publish --provenance` plus `id-token: write` when you still use tokens. Consumers: `npm audit signatures` verifies registry signatures and provenance attestations.
- Lockfile `integrity` hashes stop tarball tampering after resolution.

## 5. Limit blast radius
- CI: least-privilege tokens, no publish tokens in install steps, short-lived OIDC creds, network egress restrictions for install jobs.
- Developers: 2FA on registry accounts, separate machine/container for untrusted code (dev containers).
- Minimum release age for updates (Renovate / pnpm `minimumReleaseAge`).

## Verify
`npm ci --ignore-scripts && npm rebuild <allowlist>` builds the app (add `--ignore-scripts=false` to the rebuild if `.npmrc` sets `ignore-scripts=true`); `npm audit signatures` passes; a dependency scan runs on PRs adding dependencies.

## Checked

2026-10-25 against the npm CLI source and docs (npm/cli main, npm/documentation 2026-10-24) and the pnpm docs (2026-10-22). Confirmed: ignore-scripts is a boolean npm config defaulting to false; pnpm approves dependency build scripts through allowBuilds (10.26+), which replaced onlyBuiltDependencies in v11; npm audit signatures verifies registry signatures and provenance attestations; provenance is signed with Sigstore and logged in a public transparency ledger; trusted publishing needs npm CLI 11.5.1+ and Node 22.14+ and supports GitHub Actions, GitLab CI/CD and CircleCI cloud.

Run 2026-11-01 with npm 10.8.2 on Windows (Git Bash), offline, with scratch user and global npmrc files and cache (no registry access; the dependency was a local tarball made by `npm pack`): `ignore-scripts` defaults to false; a tarball dependency's postinstall ran on a default install and not with `ignore-scripts=true` in `.npmrc`; `npm rebuild dep` with that setting did not run it, `--ignore-scripts=false` did; `npm ci --ignore-scripts` then `npm rebuild dep` ran it. Not run: pnpm `allowBuilds`, `npm view`, Socket CLI, `npm audit signatures` and trusted publishing (network or pnpm); these stay as documented.

Method: documentation plus commands run (npm 10.8.2, offline).
