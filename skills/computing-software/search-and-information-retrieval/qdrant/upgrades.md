---
id: computing-software.search-and-information-retrieval.qdrant.upgrades
name: upgrades
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [upgrade, rolling-restart, minor-version, client-compatibility, upgrades]
level: practitioner
status: docs-checked
description: "Upgrade Qdrant safely one minor version at a time, with rolling restarts and clients upgraded after the server."
sources:
  - "https://qdrant.tech/documentation/upgrades/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Upgrade rules from the upgrades page:

- Upgrade to the latest patch version of each intermediate minor version first: from 1.15 to 1.17, first upgrade every node to 1.16.3. A 1.17 node is compatible with a 1.16 node but not with a 1.15 node. A single-node cluster cannot skip versions either.
- In a cluster, restart nodes one after another. If every collection has a replication factor of at least 2 this is zero-downtime; with a single node or replication factor 1 expect a short downtime.
- Upgrade the server cluster before client SDKs.
- Keep the client SDK within one minor version of the cluster; larger gaps might work but are not tested.
- As of v1.20.0 the internal gRPC API enforces authentication by default when an API key is configured; see the Qdrant security page before upgrading a cluster that sets only `read_only_api_key` or only `alt_api_key`.

Per platform, the page shows:

- Helm: upgrade the release (`helm upgrade qdrant qdrant/qdrant --version <target-version> -n <namespace>`); Kubernetes performs a rolling update of the StatefulSet.
- Docker: pull the new image and restart the containers one after another.
- Docker Compose: change the image version and restart the service.
- Qdrant Cloud does the intermediate steps automatically.

## Checked

2026-11-03. Confirmed on the Qdrant upgrades page: intermediate-minor rule with the 1.16.3 example, single-node rule, rolling restarts and replication factor 2, client within one minor version, cluster before clients, the v1.20 internal-authentication note, Helm and Docker procedures. Removed the unconfirmed snapshot, release-notes, `/readyz` and downgrade steps; the snapshot version rule belongs to the snapshots skills.

Method: documentation only; no commands were run.
