---
id: computing-software.devops-ci-cd.build-systems.lockfile-enforcement-in-ci
name: lockfile-enforcement-in-ci
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, dependency-pinning, lockfile-enforcement, frozen-lockfile, npm-ci, pnpm-frozen-lockfile, yarn-immutable, poetry-lock-check, uv-locked, cargo-locked, go-mod-verify, require-hashes, lockfile-drift, lockfile-lint]
level: practitioner
status: docs-checked
description: "Fail CI when a lockfile is missing or out of date: frozen/locked install flags per ecosystem, drift checks, hash verification, and lockfile-lint against registry tampering."
sources: ["https://docs.npmjs.com/cli/commands/npm-ci", "https://pnpm.io/cli/install", "https://yarnpkg.com/cli/install", "https://bun.sh/docs/pm/cli/install", "https://docs.astral.sh/uv/concepts/projects/sync/", "https://python-poetry.org/docs/cli/", "https://doc.rust-lang.org/cargo/commands/cargo-build.html", "https://go.dev/ref/mod", "https://docs.gradle.org/current/userguide/dependency_locking.html", "https://bundler.io/man/bundle-config.1.html", "https://github.com/lirantal/lockfile-lint", "https://pip.pypa.io/en/stable/topics/secure-installs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lockfile enforcement in CI

A lockfile only protects you if CI **refuses** to resolve anything not in it. Otherwise
CI quietly installs newer transitive versions than the developer tested.

## Install commands that fail on drift
| Ecosystem | CI command | Fails when |
|---|---|---|
| npm | `npm ci` | `package-lock.json` missing or out of sync with `package.json` (it never writes either file) |
| pnpm | `pnpm install --frozen-lockfile` (the default in CI) | lockfile needs an update |
| Yarn Berry | `yarn install --immutable` (default on CI; `--immutable-cache --check-cache` for zero-installs) | lockfile would change |
| Yarn 1 | `yarn install --frozen-lockfile` | lockfile needs update |
| Bun | `bun install --frozen-lockfile` | `package.json` disagrees with `bun.lock` |
| uv | `uv sync --locked` (`--frozen` = use the lockfile without checking it is up to date) | `uv.lock` stale |
| Poetry | `poetry check --lock && poetry install --no-root` | `poetry.lock` missing or stale for `pyproject.toml` |
| pip | `pip install --require-hashes -r requirements.txt` (hash-checking mode) | unpinned requirement or hash mismatch |
| Cargo | `cargo build --locked` (`--frozen` = `--locked` plus `--offline`) | `Cargo.lock` missing or needs to change |
| Go | `go mod download && go mod verify`; `go build` (acts as `-mod=readonly` since Go 1.16) | `go.mod` needs changes |
| Maven | no native lockfile; pin versions explicitly | |
| Gradle | `dependencyLocking { lockAllConfigurations() }`; write locks with `--write-locks`, CI fails on mismatch | lock state mismatch |
| Bundler | `bundle config set frozen true` (or `BUNDLE_FROZEN=true`) | Gemfile.lock out of date |

## Drift check for "did they forget to commit the lock?"
```bash
uv lock --check
go mod tidy && git diff --exit-code go.mod go.sum
```

## Tamper checks
- `lockfile-lint --path package-lock.json --type npm --allowed-hosts npm --validate-https`
  catches lockfiles rewritten to point at unexpected hosts (a PR can change `resolved:`
  without touching package.json).
- Review lockfile diffs in PRs from outside contributors.

## Policy
- Commit lockfiles for applications and for libraries (a library's lock only affects
  its own CI, which is still worth pinning).
- One package manager per repo: delete stray lockfiles from other tools (for example `yarn.lock` next to `package-lock.json`).
- Bot updates (Renovate/Dependabot) are the only way the lock changes besides deliberate
  developer changes.

## Verify
Edit `package.json` to bump a version without updating the lockfile and push: `npm ci` exits with an error and CI fails at install.

## Checked
Date: 2026-10-25. Documentation: npm CLI `npm-ci.md` (npm/cli), pnpm install docs (pnpm/pnpm.io), Yarn `install` command source (yarnpkg/berry `plugin-essentials`), Bun install docs (oven-sh/bun), uv "Locking and syncing" (astral-sh/uv), Poetry CLI docs, Cargo `--locked/--frozen` option text (rust-lang/cargo), Go modules reference, Gradle dependency locking guide, Bundler `bundle-config` man page (rubygems/rubygems), lockfile-lint README, pip secure-installs.
Confirmed: each command and flag in the table (npm ci never writes lock/package files; pnpm fails in CI when the lockfile needs updating; yarn `--immutable` default on CI and `--immutable-cache`, `--check-cache`; Bun `--frozen-lockfile`; `uv lock --check` and `--locked`/`--frozen`; `poetry check --lock`; `cargo --locked/--frozen`; Go 1.16 `-mod=readonly` behaviour; Gradle `--write-locks`; Bundler `BUNDLE_FROZEN`; `--require-hashes`; lockfile-lint `--allowed-hosts npm --validate-https`).
Removed: the `npm install --package-lock-only` drift check, the `packageManager`/Corepack and GitHub rich-diff statements, the `poetry lock --check` for Poetry before 1.6, the Maven `maven-enforcer-plugin` suggestions, the exact npm error message, `--hashes` generation detail via pip-compile, and Go `go.sum` "mismatch" wording.
Method: documentation only; no commands were run.
