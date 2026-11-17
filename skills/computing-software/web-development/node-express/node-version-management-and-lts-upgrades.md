---
id: computing-software.web-development.node-express.node-version-management-and-lts-upgrades
name: node-version-management-and-lts-upgrades
category: computing-software
field: web-development
product: node-express
tags: [nvm, node-lts-upgrade, fnm, nvmrc, node-versions]
level: practitioner
status: verified
description: "Managing Node versions: the LTS release schedule, pinning with .nvmrc or .node-version, nvm, fnm, Volta and mise, aligning CI and Docker, and a checklist for major LTS upgrades."
sources:
  - https://nodejs.org/en/about/previous-releases
  - https://github.com/nvm-sh/nvm
  - https://github.com/Schniz/fnm
  - https://nodejs.org/en/blog/migrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node version management and LTS upgrades

## 1. Release schedule
From the Node release team's `schedule.json` (fetched 2026-10-21): v20 end-of-life 2026-04-30; v22 LTS from 2024-10-29, Maintenance from 2025-10-21, end 2027-04-30; v24 LTS from 2025-10-28, Maintenance from 2026-10-20, end 2028-04-30; v25 (odd, Current only) ended 2026-06-01; v26 LTS starts 2026-10-28, end 2029-04-30. LTS start to end is 30 months, matching the claim below.
- Even-numbered majors become **LTS** in October and get ~30 months of support (Active then Maintenance LTS). Odd majors are short-lived "Current" releases - don't run them in production.
- Production should be on an Active or Maintenance LTS line; plan upgrades before end-of-life (EOL dates on nodejs.org/en/about/previous-releases).

## 2. Pin the version per repo
```bash
echo "22" > .nvmrc                  # or ".node-version" (fnm, mise, many CI tools read it)
```
```json
{ "engines": { "node": ">=22.12 <23" } }
```
Version managers:
| Tool | Notes |
|---|---|
| nvm (POSIX) / nvm-windows | `nvm install`, `nvm use` (reads .nvmrc); not run here |
| fnm | Rust, fast; `fnm use --install-if-missing` and the `fnm env --use-on-cd` shell hook (both flags confirmed in fnm 1.39.0 `--help`); reads .nvmrc/.node-version |
| Volta | pins in package.json `volta` field; transparent switching |
| mise (asdf-compatible) | multi-language, `.tool-versions` or `mise.toml` |

## 3. Keep environments aligned
- CI: `actions/setup-node` with `node-version-file: .nvmrc`.
- Docker: `FROM node:22-slim` (match major; pin minor/digest for reproducibility and update via Renovate/Dependabot).
- Hosting platforms: set the runtime version explicitly (Vercel/Netlify project settings, `engines`, Heroku).

## 4. Major upgrade checklist
1. Read the release notes and the migration guides for each skipped major (breaking changes, removed APIs, OpenSSL changes, default flags like `--experimental-require-module` becoming default).
2. Update `.nvmrc`, `engines`, Docker base image, CI matrix (test on old and new during transition).
3. Rebuild native modules (`npm rebuild`; check `node-gyp`/prebuild availability for bcrypt, sharp, sqlite3).
4. Run the full test suite and `node --trace-deprecation` to surface deprecated APIs; watch for changed defaults (e.g. fetch, ESM loading, permission model, TypeScript stripping).
5. Canary deploy and compare memory/CPU and latency; V8 upgrades can change performance characteristics.
6. Upgrade dependencies that declare `engines` incompatible with the new version.

## Verify
- [ ] Local, CI, Docker and production report the same `node -v` major; current line is supported LTS with an upgrade planned before EOL; native modules rebuilt and tests green on the new version.
