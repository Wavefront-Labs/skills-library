---
id: computing-software.cloud-infrastructure-engineering.minio.deployment-architecture
name: deployment-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, deployment-architecture, server-pool, load-balancer, site-replication-topology, signature-v4, signature-mismatch, pool-expansion, jbod]
level: advanced
status: docs-checked
description: "Design a production MinIO layout: four or more homogeneous hosts, JBOD XFS drives, load balancer, pool growth, Signature V4 header passthrough and multi-site latency."
sources: ["https://github.com/minio/docs/blob/main/source/operations/concepts/architecture.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO deployment architecture

## Distributed deployment
- A production deployment has at least **4 hosts** with homogeneous storage, compute and network, aggregated as a pool presented as one service.
- Best performance: locally attached NVMe or SSD on a PCIe controller in HBA mode, presenting XFS drives as JBOD with no RAID or pooling layers. Avoid drive or controller caching, which causes I/O spikes.
- MinIO groups drives into erasure sets striped symmetrically across nodes and picks an object's set by deterministic hashing of its path (`computing-software.cloud-infrastructure-engineering.minio.erasure-coding`).
- Every node knows the whole topology and routes internal requests, so clients can contact any node. Put a load balancer (for example NGINX, least connections or round robin) in front rather than hard-coding nodes.
- Expanding adds a pool, an independent group of nodes with its own erasure sets. Every pool is queried to find the right set, so more pools add internode traffic per call. Update the load balancer to include the new nodes; clients keep one URL.

## Clients and signatures
MinIO strictly implements the S3 API and requires AWS Signature V4 (or legacy V2). Signatures cover client headers, so load balancers, proxies or security tools that modify headers cause signature mismatch errors. Make sure intermediaries pass headers through unaltered. Use S3 SDKs rather than raw curl.

## Replicated deployments
Site replication synchronises independent deployments across racks, datacenters or regions for BC/DR or geo-local access. Replication lag depends on latency between peers and on spare I/O; the page's example with 100 ms to peers gives at least 110 ms to full sync. A global load balancer with health probes should redirect applications from a failed site to a healthy peer.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Deployment Architecture page (architecture.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
