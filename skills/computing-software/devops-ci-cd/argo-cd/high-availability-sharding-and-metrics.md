---
id: computing-software.devops-ci-cd.argo-cd.high-availability-sharding-and-metrics
name: high-availability-sharding-and-metrics
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, argocd-ha, ha-install, ha-manifests, redis-ha, haproxy, controller-sharding, controller-replicas, statefulset-controller, repo-server-scaling, repo-server-replicas, reposerver-parallelism, manifest-generation-paths, argocd-performance, status-processors, operation-processors, kubectl-parallelism-limit, timeout-reconciliation, argocd-metrics, argocd-prometheus, argocd-monitoring, servicemonitor, grafana-dashboard, app-sync-total, reconcile-duration, repo-server-cache, api-server-replicas, gitops, kubernetes]
level: advanced
status: docs-checked
description: "Run Argo CD at scale: HA manifests with Redis HA, application-controller sharding, repo-server parallelism and manifest caching, controller tuning knobs, Prometheus metrics and alerts."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/metrics/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/dynamic-cluster-distribution/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/server-commands/argocd-application-controller/", "https://github.com/argoproj/argo-cd/tree/master/manifests/ha"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# High availability, sharding and metrics

**Goal:** Argo CD survives a node loss, reconciles a few thousand apps on time, and tells
you via Prometheus when it's falling behind.

## 1. HA install
The HA manifests (`manifests/ha`) run more containers and run Redis in HA mode. The HA install needs at least three different nodes because of pod anti-affinity rules; IPv6-only clusters are not supported.
Argo CD is largely stateless: all data is Kubernetes objects, and Redis is only a disposable cache that can be rebuilt without service disruption.

## 2. Scaling each component
**application-controller** (reconciles apps, watches clusters):
```yaml
# argocd-cmd-params-cm
controller.status.processors: "50"          # default 20; app status reconciles in parallel (docs use 50/25 for 1000 apps)
controller.operation.processors: "25"       # default 10; sync operations in parallel
controller.kubectl.parallelism.limit: "20"  # max concurrent cluster operations during sync (default 20)
controller.repo.server.timeout.seconds: "180"   # default 60
controller.sharding.algorithm: "round-robin"   # legacy (default) | round-robin | consistent-hashing; the latter two are documented as experimental
# argocd-cm: timeout.reconciliation and timeout.reconciliation.jitter set how often Git is polled per app (restart the controller after changing)
```
If the controller manages many clusters and uses too much memory, shard clusters across replicas: raise `replicas` on the `argocd-application-controller` StatefulSet and repeat the number in the `ARGOCD_CONTROLLER_REPLICAS` environment variable. Pin a cluster to a shard with the `shard` field of its cluster Secret. Dynamic cluster distribution (alpha since v2.9) instead runs the controller as a Deployment (kustomize overlay `manifests/ha/base/controller-deployment`) so replicas can change without restarting pods. `argocd admin cluster stats` prints cluster statistics and the inferred shard number. `resource.customizations.ignoreResourceUpdates.<group_kind>` in `argocd-cm` stops noisy status updates from triggering reconciles.

**repo-server** (clones, renders Helm/Kustomize/plugins): CPU-bound, horizontally scaled:
```yaml
reposerver.parallelism.limit: "10"           # concurrent manifest generations (default 1; below 1 means no limit)
reposerver.repo.cache.expiration: "24h"      # default 24h; shorten if manifests change without a repo change
```
`ARGOCD_EXEC_TIMEOUT` (default 90 s, Go duration such as `2m30s`) bounds helm/kustomize runs; `ARGOCD_GIT_ATTEMPTS_COUNT` retries failed `git ls-remote` calls. The repo-server clones into `/tmp` (or `TMPDIR`), so mount a persistent volume if it runs out of disk.
**Monorepo**: the annotation `argocd.argoproj.io/manifest-generate-paths: .;../shared` (semicolon-separated paths) makes a new Git commit re-render only apps whose paths changed. It works with webhooks and, since v2.11, without them.

## 3. Reconciliation storms and backpressure
Symptoms: slow `argocd_app_reconcile`, apps waiting on manifest generation (`argocd_repo_pending_request_total`), many apps polling Git on the default interval without webhooks. Fixes:
configure repo webhooks and raise `timeout.reconciliation`; raise processors; scale and shard the controller; add repo-server replicas and tune `reposerver.parallelism.limit`; lower `controller.kubectl.parallelism.limit` to protect the API server; and use `resource.customizations.ignoreResourceUpdates` for noisy resources.

## 4. Metrics
Endpoints: application controller `argocd-metrics:8082/metrics`, api-server `argocd-server-metrics:8083/metrics`, repo-server `argocd-repo-server:8084/metrics`, commit-server `:8087/metrics`. The metrics page has example `ServiceMonitor` manifests.
Key series:
| metric | watch for |
|---|---|
| `argocd_app_info{sync_status,health_status}` | count of `OutOfSync`/`Degraded` per project (also carries `hydrator_status`) |
| `argocd_app_reconcile_bucket` | p95 reconcile time per app > 30 s |
| `argocd_app_sync_total{phase}` | `Failed`/`Error` rate |
| `argocd_app_k8s_request_total` | API pressure per cluster/verb; 429s |
| `argocd_cluster_api_resource_objects`, `argocd_cluster_cache_age_seconds` | cache size, stale caches |
| `argocd_redis_request_total{failed="true"}` | Redis trouble |
| `argocd_git_request_total{request_type}` / `argocd_git_request_duration_seconds` | Git fetch/ls-remote load — `ls-remote` ≫ fetch means polling with no webhooks |
| `argocd_repo_pending_request_total` | repo-server queue depth > parallelism limit |
Alerts (Prometheus rules):
```yaml
- alert: ArgoAppOutOfSync
  expr: argocd_app_info{sync_status="OutOfSync"} == 1
  for: 30m
- alert: ArgoAppDegraded
  expr: argocd_app_info{health_status="Degraded"} == 1
  for: 15m
- alert: ArgoReconcileSlow
  expr: histogram_quantile(0.95, sum(rate(argocd_app_reconcile_bucket[5m])) by (le)) > 60
  for: 10m
- alert: ArgoRepoServerQueue
  expr: sum(argocd_repo_pending_request_total) > 20
  for: 10m
```
Grafana: the example dashboard `examples/dashboard.json` in the Argo CD repository.
`argocd_app_labels` is disabled by default; enable it with `controller.metrics.application.labels` in `argocd-cmd-params-cm` and keep labels low-cardinality, since each distinct label value becomes a separate series.

## 5. Upgrades without downtime
Read the version-specific upgrade notes in the Argo CD documentation before upgrading.

## Verify
- [ ] Killing one Redis pod/api-server pod causes no failed syncs; UI stays up.
- [ ] `argocd admin cluster stats` shows clusters spread over shards.
- [ ] `argocd_app_reconcile` latency stays within your target at peak; the `ls-remote` rate dropped after webhooks.
- [ ] Alerts above fire in a drill (scale a Deployment by hand with self-heal off).

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: HA node requirement and Redis-as-cache statement, processors defaults (20/10) and 1000-app example (50/25), `controller.kubectl.parallelism.limit`, sharding algorithms and experimental status, `ARGOCD_CONTROLLER_REPLICAS`, cluster `shard` field, dynamic distribution (alpha since v2.9, Deployment overlay), `argocd admin cluster stats`, `reposerver.parallelism.limit` default 1, repo cache expiration 24h, `ARGOCD_EXEC_TIMEOUT` 90 s, `manifest-generate-paths` annotation (the old skill misspelled it as manifest-generation-paths and said webhooks are required), metric names and endpoints (8082, 8083, 8084, 8087), `controller.metrics.application.labels`, example dashboard. Removed unconfirmed claims (Helm values, Redis auth version gate, per-replica cluster capacity, applicationset/notifications ports, `workqueue_depth`, `autosync_enabled` label, Grafana.com id, upgrade timings). Alert thresholds are examples, not documented values.

Method: documentation only; no commands were run.
