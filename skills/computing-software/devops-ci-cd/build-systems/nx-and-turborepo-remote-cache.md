---
id: computing-software.devops-ci-cd.build-systems.nx-and-turborepo-remote-cache
name: nx-and-turborepo-remote-cache
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, monorepo, nx, nx-cloud, nx-replay, turborepo, turborepo-remote-cache, turbo-remote-cache, vercel-remote-cache, self-hosted-remote-cache, ducktors-turborepo-remote-cache, cache-inputs, namedinputs, turbo-json]
level: practitioner
status: draft
description: "Share JS monorepo task outputs across CI and developers: Nx Cloud/self-hosted caches and Turborepo remote cache (Vercel or self-hosted), with correct inputs, env hashing and read-only tokens."
sources: ["https://nx.dev/ci/features/remote-cache", "https://nx.dev/recipes/running-tasks/configure-inputs", "https://turborepo.com/docs/core-concepts/remote-caching", "https://turborepo.com/docs/reference/configuration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nx and Turborepo remote cache

Both hash a task's inputs (files, deps, env, command) and restore outputs + terminal logs
on a hit. Remote cache shares those hits between CI runs and developers.

## Nx
```bash
npx nx connect                    # links the workspace to Nx Cloud, writes nxCloudId in nx.json
```
```json
// nx.json
{
  "nxCloudId": "....",
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": ["default", "!{projectRoot}/**/*.spec.ts", "!{projectRoot}/jest.config.ts"],
    "sharedGlobals": ["{workspaceRoot}/tsconfig.base.json", { "runtime": "node -v" }]
  },
  "targetDefaults": {
    "build": { "cache": true, "inputs": ["production", "^production"], "outputs": ["{projectRoot}/dist"] },
    "test":  { "cache": true, "inputs": ["default", "^production", { "env": "API_URL" }] }
  }
}
```
- Tokens: CI gets a read-write token (`NX_CLOUD_ACCESS_TOKEN` secret); developers use
  personal or read-only access so laptops can't poison CI.
- Self-hosting: Nx Powerpack / enterprise self-hosted cache (S3, GCS, Azure, shared FS
  packages like `@nx/s3-cache`); check current licensing for your Nx version, it has
  changed across releases.
- `nx show project api --web` / `nx run api:build --verbose` shows the hash inputs.

## Turborepo
```bash
npx turbo login && npx turbo link          # Vercel Remote Cache
# CI: env TURBO_TOKEN (secret) and TURBO_TEAM
```
```json
// turbo.json (v2)
{
  "$schema": "https://turborepo.com/schema.json",
  "globalDependencies": ["tsconfig.base.json"],
  "globalEnv": ["NODE_ENV"],
  "tasks": {
    "build": { "dependsOn": ["^build"], "inputs": ["$TURBO_DEFAULT$", "!**/*.test.ts"], "outputs": ["dist/**", ".next/**", "!.next/cache/**"], "env": ["NEXT_PUBLIC_*"] },
    "test":  { "dependsOn": ["^build"], "outputs": [] }
  },
  "remoteCache": { "signature": true }       // HMAC-sign artifacts with TURBO_REMOTE_CACHE_SIGNATURE_KEY
}
```
Self-hosted: any server implementing the Turborepo remote cache API (e.g.
`ducktors/turborepo-remote-cache` on S3/GCS/Azure). Point with `TURBO_API=https://cache.example.com`,
`TURBO_TOKEN`, `TURBO_TEAM`. Read-only for devs: `TURBO_CACHE=local:rw,remote:r`
(older: `--remote-only`/`--remote-cache-read-only`).

## Correctness rules (same for both)
- **Declare env vars** that affect output (`env`/`globalEnv` in Turbo, `{ "env": ... }`
  inputs in Nx). Turbo 2 strict env mode hides undeclared vars from tasks, exposing
  mistakes early.
- **Declare all outputs**, or a hit restores logs but not files and later tasks fail.
- Exclude test files from build inputs so editing a test doesn't rebuild.
- Never cache tasks with side effects (deploy, publish, db migrate).

## Verify
Run the pipeline twice for the same commit on different CI machines: the second shows
`Nx read the output from the remote cache` / `cache hit, replaying logs` and finishes in
seconds. `turbo run build --dry=json` lists each task's hash and inputs for debugging misses.
