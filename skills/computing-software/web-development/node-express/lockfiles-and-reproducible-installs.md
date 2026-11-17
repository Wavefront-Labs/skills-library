---
id: computing-software.web-development.node-express.lockfiles-and-reproducible-installs
name: lockfiles-and-reproducible-installs
category: computing-software
field: web-development
product: node-express
tags: [vulnerable-dependencies, lockfiles, npm-ci, reproducible-builds, supply-chain, pnpm]
level: practitioner
status: gated
description: "Committing and enforcing lockfiles for reproducible installs: npm ci vs npm install, frozen-lockfile in pnpm/yarn, pip hashes, lockfile review and merge conflicts."
sources:
  - https://docs.npmjs.com/cli/commands/npm-ci
  - https://docs.npmjs.com/cli/configuring-npm/package-lock-json
  - https://pnpm.io/cli/install#--frozen-lockfile
  - https://pip.pypa.io/en/stable/topics/secure-installs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lockfiles and reproducible installs

## 1. Commit the lockfile
`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock`/`uv.lock`, `Gemfile.lock`, `Cargo.lock`. Without it, `^1.2.0` resolves to whatever is newest at install time - including a freshly hijacked release.
One package manager per repo: add `"packageManager": "pnpm@9.12.0"` (Corepack) and delete stray lockfiles.

## 2. Install from the lockfile in CI and Docker
| Tool | Command | Behaviour |
|---|---|---|
| npm | `npm ci` | deletes node_modules, installs exactly the lock, fails if lock and package.json disagree |
| pnpm | `pnpm install --frozen-lockfile` (default in CI) | fails if lock needs updating |
| yarn berry | `yarn install --immutable` | same (gated: unconfirmed, source is paywalled or blocked) |
| pip | `pip install --require-hashes -r requirements.txt` | verifies every artifact hash (generate with `pip-compile --generate-hashes` or `uv pip compile`) |
| uv / poetry | `uv sync --locked`, `poetry install --sync` | (gated: unconfirmed, source is paywalled or blocked) |
| bundler | `bundle config set frozen true` | (gated: unconfirmed, source is paywalled or blocked) |
`npm install` in CI can silently rewrite the lock - never use it there. Ran on npm 11.21.1: `npm ci` with a package.json that added `cors` failed with `EUSAGE ... Missing: cors@2.8.6 from lock file`, and it replaced a stray folder in `node_modules`. The lock stores an `integrity` field per package. Ran pip: `--require-hashes` rejects a requirement without a hash and prints the `--hash=sha256:...` line to add (`pip hash <file>` prints the same).

## 3. Review lockfile diffs
- Unexpected new packages or `resolved` URLs pointing to a non-registry host (lockfile injection) are red flags. Tools: `npx lockfile-lint --path package-lock.json --type npm --allowed-hosts npm --validate-https` (the lockfile-lint README shows `--path`, `--type`, `--allowed-hosts` and `--validate-https`).
- Large lock churn in an unrelated PR - ask why.
- `integrity` (sha512) fields protect against tampered tarballs; don't strip them.

## 4. Merge conflicts
Do not hand-merge. Take one side, then re-run the install (`npm install`, `pnpm install`) to regenerate, and commit. pnpm/yarn can auto-resolve lock conflicts on install.

## 5. Updating deliberately
`npm outdated`, `npm update` (within ranges), `npx npm-check-updates -u` for majors; batch via Renovate/Dependabot. Consider a minimum release age (pnpm `minimumReleaseAge`, Renovate `minimumReleaseAge: "3 days"`) so compromised releases are usually yanked before you take them.

## Verify
Fresh clone + `npm ci` twice produces identical `node_modules` (`npm ls --all` diff); CI fails if someone commits package.json without the updated lock.
