---
id: computing-software.systems-network-administration.immich.upgrading
name: upgrading
category: computing-software
field: systems-network-administration
product: immich
tags: [upgrade, immich-version, semver, docker-compose, breaking-changes]
level: practitioner
status: docs-checked
description: "Upgrade an Immich Docker Compose install: read release notes, pull and restart, prune images, pin major versions, and mobile and downgrade rules."
sources:
  - https://docs.immich.app/install/upgrading
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: upgrade safely.

1. Read the release notes and the docs' list of versions with breaking changes.
2. If `.env` sets `IMMICH_VERSION`, change it to the version you want (the docs' default is a major tag such as `v3`).
3. In the directory with `docker-compose.yml` run:

```bash
docker compose pull && docker compose up -d
```

4. Optionally reclaim disk space from obsolete images:

```bash
docker image prune
```

Versioning policy: Immich uses semantic versioning (`<major>.<minor>.<patch>`). Breaking changes, including to the API or deployment, are intended only for major releases. A metatag such as `:v3` follows the current major version and ignores release candidates.

Compatibility:

- The mobile app is typically compatible with the current and prior major version, but the server only works with the matching major version. Upgrade all mobile clients before the server.
- Patches are not backported; run the latest stable release.
- Downgrading, even within a minor version, is not supported.

If startup warns about the deprecated pgvecto.rs extension, follow the VectorChord migration skill before further upgrades. Do not downgrade below 1.133.0 after migrating.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: install/upgrading (Versioning Policy, Migrating to VectorChord).
Removed or reworded: the claim that the old docker-compose command is unsupported.
Method: documentation only; no commands were run.
