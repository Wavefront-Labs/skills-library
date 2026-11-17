---
id: computing-software.devops-ci-cd.argo-workflows.node-status-offload-and-compression
name: node-status-offload-and-compression
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [node-status-offload, compressed-nodes, workflow-compression-algorithm, etcd-size-limit, persistence]
level: advanced
status: docs-checked
description: "Handle Workflows near the 1MB etcd limit using gzip, zstd or brotli compression of node status and SQL offload with nodeStatusOffLoad."
sources: ["https://argo-workflows.readthedocs.io/en/latest/offloading-large-workflows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large workflow status offload and compression
Workflows are Kubernetes resources, limited to about 1MB, and `/status/nodes` can exceed that. Argo first compresses the node status into `/status/compressedNodes`, and only if still too large stores it in SQL. To enable the SQL step configure Postgres, MySQL or MariaDB under `persistence` and set `nodeStatusOffLoad: true`.

Compression (v4.1 and later): gzip by default. On the controller set `WORKFLOW_COMPRESSION_ALGORITHM` to `gzip`, `zstd` or `brotli`, and `WORKFLOW_COMPRESSION_LEVEL` (gzip 1-9 default 6; zstd 1-4 default 2; brotli 0-11 default 6). Decompression auto-detects, so settings affect only newly written statuses. Warning: non-gzip data cannot be read by older versions or by tooling that gunzips `compressedNodes`, so change algorithm only after every component is upgraded.

Measured on synthetic data relative to gzip: zstd 3 is 82% of the size, brotli 9 is 67%, brotli 11 is 59% but about 80 times slower than brotli 9, which hurts because large workflows are recompressed on every update. zstd 3 and brotli 9 raise the node-count ceiling roughly 20% and 50%.

Errors:
- `etcdserver: request is too large` on submit: use the Argo CLI with `ARGO_SERVER` exported.
- `offload node status is not supported`: even compressed it is too big; enable offload, or shrink the manifest with `withItems`/`withParam`, template defaults, WorkflowTemplates, or workflows of workflows.
- Workflows missing from the database simply were not large enough; offloading is on demand.

## Checked
2026-11-08. Confirmed against the Argo Workflows Offloading Large Workflows page: compression then SQL offload order, `nodeStatusOffLoad`, v4.1 compression, `WORKFLOW_COMPRESSION_ALGORITHM` and `WORKFLOW_COMPRESSION_LEVEL` with their level ranges and defaults, the benchmark ratios, the compatibility warning and the three FAQ errors. Nothing removed.
Method: documentation only; no commands were run.
