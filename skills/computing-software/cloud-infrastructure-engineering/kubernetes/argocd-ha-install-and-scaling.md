---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argocd-ha-install-and-scaling
name: argocd-ha-install-and-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argocd, argocd-ha, argocd-scaling, gitops, controller-sharding, repo-server]
level: advanced
status: docs-checked
description: "Run Argo CD at scale: HA manifests with redis-ha, application-controller sharding, repo-server parallelism and caching, processors, reconciliation timeouts, and what to monitor."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/dynamic-cluster-distribution/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD HA and scaling

## HA install
`manifests/ha/install.yaml`. The HA install requires **at least three different nodes** because of a pod
anti-affinity rule in the manifests.

## Components and their knobs
**application-controller** (StatefulSet): reconciles apps, caches all managed clusters' resources.
- Shard across replicas: set `replicas` and env `ARGOCD_CONTROLLER_REPLICAS` to the same
  number (the Helm chart does this). Each cluster is assigned to one shard; one huge
  cluster cannot be split.
- `controller.sharding.algorithm` (in `argocd-cmd-params-cm`): `legacy` (default, uid based and
  non-uniform), `round-robin` or `consistent-hashing` (both marked experimental in the docs).
  Dynamic cluster distribution (v2.9+, alpha, disabled by default) rebalances shards when
  replicas change.
- `--status-processors` (default 20) and `--operation-processors` (default 10); the docs use
  50 and 25 for 1000 applications.
- `controller.kubectl.parallelism.limit` (flag `--kubectl-parallelism-limit`, default 20) caps
  concurrent cluster operations during sync.
- Memory scales with cluster object count: exclude kinds you do not need Argo CD to track with `resource.exclusions`
  in `argocd-cm`.

**repo-server** (Deployment, stateless): clones repos and renders Helm/Kustomize.
- Scale replicas for render throughput; `reposerver.parallelism.limit` (flag
  `--parallelismlimit`, default 1 in `argocd-cmd-params-cm.yaml`, below 1 means no limit)
  limits concurrent manifest generations and helps avoid OOM.
- The repo-server enforces a 90 second timeout on config management tools such as `helm` or
  `kustomize`; change it with the `ARGOCD_EXEC_TIMEOUT` env variable.
- Monorepos: every commit invalidates cache for all apps in the repo; use
  `argocd.argoproj.io/manifest-generate-paths` annotation (semicolon-separated paths; works
  with or without webhooks since v2.11) to limit refreshes.

**argocd-server**: stateless API/UI; replicas plus `ARGOCD_API_SERVER_REPLICAS` for rate limit math.

## Reconciliation load
- `timeout.reconciliation` (default 3m) polls Git for every app; set Git webhooks and
  raise it at scale; `timeout.reconciliation.jitter` spreads the refreshes (max extra duration
  added to the timeout). Both are in `argocd-cm`; restart the repo-server and controller after
  changing them.
- Hard refresh storms after restarts: expect a spike; size repo-server for it.

## Monitor
```promql
sum(argocd_app_info{sync_status!="Synced"}) by (project)
histogram_quantile(0.95, sum(rate(argocd_app_reconcile_bucket[5m])) by (le))
argocd_cluster_api_resource_objects          # per-cluster cache size
sum(rate(argocd_git_request_total[5m])) by (request_type)
```
Plus repo-server memory/OOMKilled and controller memory per shard.

## Verify
- [ ] Kill a controller pod: its shard is picked up after restart and apps return to Synced.
- [ ] Reconcile p95 stays flat during a busy deploy window.

## Checked

Documentation release: Argo CD stable docs (argo-cd repo docs/, latest release v3.5.6, repo commit 2026-10-25).
Confirmed: HA needs three nodes (anti-affinity); `ARGOCD_CONTROLLER_REPLICAS`; sharding algorithms and `legacy` default; dynamic distribution v2.9 alpha; processor defaults and the 50/25 for 1000 apps; `controller.kubectl.parallelism.limit` default 20; `reposerver.parallelism.limit`; 90 second exec timeout and `ARGOCD_EXEC_TIMEOUT`; reconciliation timeout 3m and jitter; `manifest-generate-paths`; `ARGOCD_API_SERVER_REPLICAS`; metrics `argocd_app_info`, `argocd_app_reconcile`, `argocd_cluster_api_resource_objects`, `argocd_git_request_total`.
Removed because no doc covers them: the Redis cache-only claim, the exclusion examples, the ApplicationSet-controller leader election claim, the 600s example and the `workqueue_depth` query.

Method: documentation only; no commands were run.
