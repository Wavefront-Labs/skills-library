---
id: computing-software.devops-ci-cd.argo-workflows.security-network-and-server
name: security-network-and-server
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [argo-server-security, network-policy, transport-layer-security, server-read-only, metrics-port]
level: advanced
status: docs-checked
description: "Secure the Argo Server in layers and plan NetworkPolicy ingress and egress for server, controller and database access."
sources: ["https://argo-workflows.readthedocs.io/en/latest/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Server and network security
The Argo Server is secured in three layers: enable TLS so data cannot be read in transit, enable an auth mode so unknown users cannot run workflows, and configure the `argo-server` Role and RoleBinding with correct permissions. For a read-only server, give that role only `get`, `list` and `watch`.

Network needs, useful for NetworkPolicy on the argo namespace:
- Argo Server: usually exposed for ingress (Ingress or load balancer) for UI users, and mandatory if webhooks are used. You can also run `argo server` locally with your kubeconfig and open https://localhost:2746.
- Argo Server egress: to the artifact provider (S3, GCS, MinIO, Artifactory, Azure Blob Storage) if you want artifact download through the UI, because it streams the artifact.
- Workflow controller: exposes Prometheus metrics at `workflow-controller-metrics:9090`. Prometheus typically lives in another namespace, so allow cross-namespace ingress to that Service.
- Database: if workflow archiving or offloading is enabled, both the controller and the argo-server Deployments need egress to the external database.

## Checked
2026-11-03. Confirmed against the Argo Workflows Security page (Argo Server Security, Read-Only and Network Security sections): the three layers, read-only verbs, ingress and egress needs, the metrics Service on port 9090 and database egress. Removed an uncited SECURITY.md instruction.
Method: documentation only; no commands were run.
