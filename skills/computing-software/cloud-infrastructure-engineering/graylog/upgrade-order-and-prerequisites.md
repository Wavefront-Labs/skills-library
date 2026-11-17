---
id: computing-software.cloud-infrastructure-engineering.graylog.upgrade-order-and-prerequisites
name: upgrade-order-and-prerequisites
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [upgrade-order, upgrade, rolling-upgrade, docker-upgrade, release-notes]
level: practitioner
status: docs-checked
description: "Upgrade a Graylog stack safely: back up, read release notes, upgrade dependencies first, then Graylog before Data Node; Docker image steps."
sources:
  - https://go2docs.graylog.org/current/upgrading_graylog/upgrading_graylog.html
  - https://go2docs.graylog.org/current/upgrading_graylog/upgrading_graylog_in_docker.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# upgrade order and prerequisites

Rules from the upgrade guide:
- Read the release notes for the target version for breaking changes.
- Follow the incremental upgrade path when coming from older versions.
- Back up Graylog, MongoDB and Data Node (or OpenSearch) first.
- Check the Compatibility Matrix. Upgrade MongoDB and self-managed OpenSearch before Graylog.
- With Data Node, upgrade Graylog first, then Data Node, ending on the same release.
- You must be an administrator.

Docker:
1. `docker images` and `docker ps` to see versions and containers.
2. `docker stop <id>` and `docker rm <id>` for outdated containers.
3. Pull explicit tags (Graylog does not use `latest`); the 7.2 example pulls `mongo:8.0` among others.
4. Recreate the containers from the new images (the page uses `docker-compose up -d` and `--force-recreate`); if you use your own compose file, change each service's image tag.
5. After moving MongoDB to 8.0, check the feature compatibility level with `db.adminCommand( { getParameter: 1, featureCompatibilityVersion: 1 } )` and raise it with `setFeatureCompatibilityVersion: "8.0"` on the primary.

Across several versions, upgrade incrementally through every minor release (the page's example path is 5.2, 6.0, 6.1, 6.2, 6.3, 7.0, 7.1), with all cluster nodes on the same version before the next step. Before moving self-managed OpenSearch to 3.x: indices created under a version older than 2.0 are unsupported, 3.7.x is the maximum supported version, and you cannot return to the previous version afterwards.

On Windows Docker with WSL2, set `kernelCommandLine = "sysctl.vm.max_map_count=262144"` under `[wsl2]` in `.wslconfig`, then `wsl --shutdown`.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/upgrading_graylog/upgrading_graylog.html and https://go2docs.graylog.org/current/upgrading_graylog/upgrading_graylog_in_docker.htm (both read in full, Graylog 7.2 docs).
