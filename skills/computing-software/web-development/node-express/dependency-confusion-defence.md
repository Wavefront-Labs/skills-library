---
id: computing-software.web-development.node-express.dependency-confusion-defence
name: dependency-confusion-defence
category: computing-software
field: web-development
product: node-express
tags: [dependency-confusion, typosquatting, scoped-packages, npmrc, private-registry, supply-chain]
level: practitioner
status: verified
description: "Preventing dependency confusion and typosquatting: scoped internal packages, registry routing in .npmrc, proxy registry rules, release-age delays and install-time review."
sources:
  - https://docs.npmjs.com/cli/v11/configuring-npm/npmrc
  - https://docs.npmjs.com/cli/v11/using-npm/scope
  - https://docs.npmjs.com/cli/v11/commands/npm-ci
  - https://pnpm.io/settings#minimumreleaseage
  - https://pnpm.io/settings#allowbuilds
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dependency confusion and typosquatting

## 1. Dependency confusion
Your app depends on internal `billing-utils@1.2.0` from a private registry. An attacker publishes `billing-utils@99.0.0` on public npm; a misconfigured resolver picks the higher public version and runs its install script in CI.
Defences:
- **Scope everything internal**: `@acme/billing-utils`, and own the `@acme` org on npmjs.com so nobody else can publish into it.
- Route the scope explicitly:
```ini
# .npmrc (committed)
@acme:registry=https://npm.internal.acme.com/
//npm.internal.acme.com/:_authToken=${NPM_INTERNAL_TOKEN}
```
- Proxy registries (Artifactory, Nexus, Verdaccio, GitHub Packages): configure internal names/scopes to resolve **only** from the internal repo, never fall through to public.
- Lockfiles record where each package was `resolved` from; `npm ci` fails when the lockfile and `package.json` disagree.
- For unscoped legacy names, publish placeholder packages on npm under your account.

## 2. Typosquatting and lookalikes
`lodahs`, `cross-env.js`, `@acme-corp/...` (wrong scope), packages named after popular repos.
- Review new dependencies in PRs: name, publisher, age, weekly downloads, repo link, install scripts (Socket/`npm view <pkg>`).
- Copy install commands from official docs, not search results or AI suggestions without checking (package names suggested by an AI assistant may not exist or may be attacker-registered).

## 3. Slow down fresh releases
Compromised versions are usually detected within hours to days:
```yaml
# pnpm-workspace.yaml (setting added in pnpm 10.16; default 1440 since pnpm 11)
minimumReleaseAge: 1440        # minutes; ignore versions younger than 1 day
```
Renovate `minimumReleaseAge: "3 days"` for automated update PRs.

## 4. Limit blast radius
`npm ci --ignore-scripts` in CI where possible (pnpm does not run unreviewed dependency build scripts and fails the install until you review them; approve with `allowBuilds` in `pnpm-workspace.yaml`, which replaced `onlyBuiltDependencies` in pnpm 11); no production secrets in install steps.

## Verify
- [ ] `npm config get @acme:registry` resolves to the internal registry on dev machines and CI; a test publish of an internal name on public npm would not be resolved.

## Checked

2026-10-25 against the npm CLI docs (npm/cli main) and the pnpm docs (pnpm/pnpm.io, 2026-10-22). Confirmed: @scope:registry maps a scope to a registry and ${VAR} substitution works in npmrc files; each npm user or organisation owns its scope and only they can add packages to it; npm ci exits with an error when the lockfile does not match package.json; pnpm minimumReleaseAge is in minutes, added in v10.16.0, default 1440 since v11; pnpm unreviewed dependency build scripts are disallowed and fail install by default (strictDepBuilds true); onlyBuiltDependencies was replaced by allowBuilds.

Run 2026-11-01 with npm 10.8.2 on Windows (Git Bash), offline, with scratch user and global npmrc files and cache (no registry access; the dependency was a local tarball made by `npm pack`): a committed `.npmrc` with `@acme:registry=...` and an `_authToken=${NPM_INTERNAL_TOKEN}` line: `npm config get @acme:registry` returned the internal URL and `npm config list` showed the token as `(protected)`; `npm ci` failed with `EUSAGE ... package.json and package-lock.json ... are not in sync ... Missing: dep2@1.0.0 from lock file` and, without a lockfile, `can only install with an existing package-lock.json`; `npm ci --ignore-scripts` is accepted. Not run: pnpm settings (`minimumReleaseAge`, `allowBuilds`), Renovate, proxy registries; these stay as documented.

Method: documentation plus commands run (npm 10.8.2, offline).
