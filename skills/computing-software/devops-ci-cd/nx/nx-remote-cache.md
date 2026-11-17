---
id: computing-software.devops-ci-cd.nx.nx-remote-cache
name: nx-remote-cache
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-cloud, remote-cache, ci, cache-security, access-tokens]
level: practitioner
status: docs-checked
description: "Share Nx cache across machines with Nx Cloud: nx connect, what is stored, token scoping against cache poisoning, availability and --skipRemoteCache."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/CI%20Features/remote-cache.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let CI jobs and developers reuse each other's task results.

Connect: `npx nx@latest connect`. In `nx.json`, `nxCloudId` identifies the workspace, and `nxCloudUrl` points at a different Nx Cloud instance.

Behaviour: Nx checks the local cache first, then remote. A remote hit restores terminal output and declared `outputs` as if local. If the remote is down, local hits still work and Nx runs everything else. Workers also share artifacts through it: when a task needs output from another agent, Nx restores it first. Entries hold stdout/stderr, files matching `outputs`, and the hash; never source files.

Security model (cache poisoning, CREEP CVE-2025-36852):
- Cache entries are immutable; no later run overwrites one.
- Use a read-write CI token only on protected branches such as `main`; other branches use a read-only token that reads shared cache and writes to a cache isolated to that run.
- Developers log in; workspace settings decide whether each developer or unauthenticated machine gets read-write, read-only or no access.
- End-to-end encryption: set `nxCloudEncryptionKey` or `NX_CLOUD_ENCRYPTION_KEY`; the key never reaches Nx Cloud.
- For deployable artifacts, skip the cache when building them.

Skip: `--skipRemoteCache` for one command (see also `--skip-nx-cache`, nx-local-cache-settings).

Fix misses: Nx Cloud Analytics, Cache inputs and outputs, and a task's Report tab show files read/written outside declared inputs/outputs; Ultracache (nx-ultracache-trial-mode) handles most of them.

Pairing: with `nx affected` the unaffected-but-selected tasks (the same ones selected on every push to a PR) are cache hits.

## Checked

2026-11-07. Confirmed against Remote caching: npx nx@latest connect, restore of terminal output and declared outputs, local-first lookup and behaviour when the remote is down, Workers sharing artifacts, what an entry stores (stdout/stderr, outputs files, hash, never inputs), the security list (immutable entries, read-write token only on protected branches, read-only token isolation, CREEP CVE-2025-36852, developer login and workspace access settings, end-to-end encryption, skipping the cache for deployable artifacts), Analytics > Cache inputs and outputs and the Report tab, nx affected pairing, and --skipRemoteCache. From the nx.json reference: nxCloudId, nxCloudUrl, nxCloudEncryptionKey with NX_CLOUD_ENCRYPTION_KEY, and --skip-nx-cache. Removed: the claim that self-hosted caching is free for everyone (not on the page), the claim that connect writes nxCloudId, and the invented Verify step.

Method: documentation only; no commands were run.
