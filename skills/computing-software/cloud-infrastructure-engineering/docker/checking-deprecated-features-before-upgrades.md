---
id: computing-software.cloud-infrastructure-engineering.docker.checking-deprecated-features-before-upgrades
name: checking-deprecated-features-before-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, engine-upgrade, deprecated-features, release-notes, api-version, docker-upgrade, change-management]
level: advanced
status: docs-checked
description: "Prepare Engine upgrades: read release notes and the deprecated features list, check API version minimums for clients, and test daemon.json and workloads on a canary host."
sources: ["https://docs.docker.com/engine/deprecated/", "https://docs.docker.com/engine/release-notes/", "https://docs.docker.com/reference/api/engine/#api-version-matrix", "https://docs.docker.com/reference/cli/dockerd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking deprecated features before upgrades

Docker removes features on a published schedule: deprecated in one major release, removed
in a later one. The **Deprecated Engine Features** page lists each item with the version it
was deprecated and removed.

## Pre-upgrade checklist
1. Read release notes for every major version between current and target (Engine, buildx,
   Compose, containerd.io are separate notes).
2. Grep your estate for deprecated items, examples from past cycles:
   - Storage drivers removed: AuFS (deprecated 19.03, removed 24.0), legacy `overlay` (removed 24.0), device mapper (removed 25.0); check yours with `docker info -f '{{.Driver}}'`.
   - Image manifest v2 schema 1: deprecated 19.03, disabled by default in 26.0, removed in 28.2, so very old images fail to pull.
   - `--link` on the default bridge network: deprecated since v1.10, removal targeted for v30.0 (a warning was added in 29.6).
   - Legacy API versions: deprecation started in 25.0; older clients or SDKs pinned via `DOCKER_API_VERSION` can be refused.
   - Cgroup v1 is deprecated from 29.0 and supported until May 2029.
   - Legacy builder (`DOCKER_BUILDKIT=0`) deprecated since 23.0.
3. Check client compatibility: `docker version --format '{{.Server.MinAPIVersion}}'` on the
   target vs API versions your tools use (CI agents, monitoring, Portainer, SDK pins).
4. Validate configuration with the new binary: `dockerd --validate --config-file ...` on a
   canary host.
5. Run representative workloads on the canary for a few days (networking, logging drivers,
   volume plugins, GPU runtime).

## Commands
```bash
docker version                      # client/server versions, API version, MinAPIVersion
docker info --format '{{json .Warnings}}'    # daemon warnings, if any
```

## Plan the rollout
- Upgrade dev and CI builders first (they surface build behaviour changes), then canary
  production hosts, then the rest.
- Keep the previous package version available locally for rollback (see engine rollback skill).
- Upgrade plugins (volume, logging, authz) and the NVIDIA toolkit in the same window if
  release notes require it.

## Gotchas
- Release notes include default changes that affect only new setups: in Engine 29 the containerd image store became the default for fresh installs (not for daemons configured with `userns-remap`), so newly built hosts can differ from upgraded ones.

## Checked

Checked against docker/docs (latest commit 2026-10-23): the Deprecated Engine Features page (vendored `deprecated.md`), `engine/release-notes/29.md`, the dockerd reference and the Engine API swagger.

- Removal versions for AuFS (24.0), legacy overlay (24.0), device mapper (25.0), schema 1 manifests (removed 28.2), the legacy builder (deprecated 23.0), cgroup v1 (deprecated 29.0, supported until May 2029) and `--link` on the default bridge (deprecated v1.10, target removal v30.0).
- `dockerd --validate --config-file` exists; `MinAPIVersion` is a field of the version response. The 29.x release notes record the minimum API version being raised to 1.44 and later lowered to 1.40, so read the notes for your exact target.
- Engine 29 release notes: containerd image store is the default for fresh installs, not for `userns-remap` daemons.
- Removed as unconfirmed: the Compose v1 end-of-life line, the journalctl and apt-cache commands and the daemon.json renamed-keys bullet.

Method: documentation only; no commands were run.
