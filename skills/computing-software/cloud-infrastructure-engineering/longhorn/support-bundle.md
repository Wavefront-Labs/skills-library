---
id: computing-software.cloud-infrastructure-engineering.longhorn.support-bundle
name: support-bundle
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [support-bundle, troubleshooting, logs, manifests, simulator]
level: intro
status: docs-checked
description: "Generate a Longhorn support bundle from the UI, what it contains, the cluster-admin service account it uses and the no-concurrent-generation rule."
sources:
  - https://longhorn.io/docs/1.13.0/troubleshoot/support-bundle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: collect diagnostics for a Longhorn issue.

Since v1.4.0 Longhorn uses the support bundle kit rather than its in-house tool.

Steps: click Generate Support Bundle at the bottom of the Longhorn UI; the browser downloads a zip file of cluster manifests and logs.

During generation Longhorn creates a Deployment for the support bundle manager. It runs under a dedicated `longhorn-support-bundle` service account and a `longhorn-support-bundle` cluster role binding with `cluster-admin` access, so review that before generating in a locked-down cluster.

The bundle can be run as a mocked Kubernetes cluster that works with `kubectl`; the simulator command is in the support bundle kit documentation.

Restriction: concurrent generation is not supported. Wait for the current bundle to finish before starting another; starting a new one while one is in progress overwrites the older bundle.

Attach the zip when reporting an issue, after checking it for anything sensitive in the manifests and logs.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/troubleshoot/support-bundle/ : support bundle contents, service account and cluster-admin binding, concurrency limit. Nothing else was removed.

Method: documentation only; no commands were run.
