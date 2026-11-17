---
id: computing-software.search-and-information-retrieval.qdrant.installation-docker
name: installation-docker
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [installation, docker, storage, ports]
level: intro
status: docs-checked
description: "Run Qdrant in Docker with a persistent storage volume, the right ports and a POSIX filesystem."
sources:
  - "https://qdrant.tech/documentation/installation/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The installation page recommends Docker for testing and development, and Kubernetes or Qdrant Cloud for production.

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 \
    -v $(pwd)/path/to/data:/qdrant/storage \
    qdrant/qdrant
```

This starts Qdrant with default configuration, storing data in the mounted directory; the welcome message appears at localhost:6333.

Ports, which every instance needs open:

- 6333: HTTP API, plus the health and metrics endpoints
- 6334: gRPC API
- 6335: distributed deployment

Cluster instances must reach each other on these ports and accept client connections on 6333 and 6334.

Storage requirements:

- Block-level access to a POSIX-compatible file system. Block-level network storage such as iSCSI is acceptable; NFS and object storage such as S3 do not work.
- Use SSD or NVMe if you offload vectors to a local disk.
- Docker/WSL on Windows with mounts is known to cause file system problems and data loss.
- Supported CPUs are 64-bit x86_64/amd64 and AArch64/arm64; 32-bit is not supported.

To change configuration, mount a file over `/qdrant/config/production.yaml`, or mount your own file and start with `./qdrant --config-path config/custom_config.yaml`. The default configuration may not be secure enough for every situation; see the security documentation.

Docker Compose example (single node) maps ports 6333 and 6334, mounts `./qdrant_data` to `/qdrant/storage`, and can inject config inline through the top-level `configs` element, which needs Docker Compose v2.23.1 or above (Docker Engine 25.0.0, Docker Desktop 4.26.0).

For production on plain Docker the docs list extra duties: performant persistent storage, security settings, multiple nodes for high availability, a load balancer, a backup and disaster recovery plan, and monitoring and logging integration. The Helm chart (`helm repo add qdrant https://qdrant.to/helm`, then `helm install qdrant qdrant/qdrant`) has community support only and lacks features such as zero-downtime upgrades and automatic rebalancing that Qdrant Cloud has.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant installation page (landing_page repo, installation.md), read in full. Removed the unconfirmed `:z` volume suffix, the dashboard URL, the image-tag pinning advice and the one-directory-per-node note; added the confirmed requirements and Compose details.
