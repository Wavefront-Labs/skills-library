---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-controller-manager-concurrency-tuning
name: kube-controller-manager-concurrency-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-controller-manager, kube-controller-manager-flags, concurrent-syncs, controller-qps, kube-api-qps, large-clusters, controllers-flag]
level: advanced
status: docs-checked
description: "Tune kube-controller-manager for large or bursty clusters: --concurrent-*-syncs workers, --kube-api-qps/burst, and the workqueue metrics that show lag."
sources: ["https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/", "https://kubernetes.io/docs/concepts/cluster-administration/flow-control/", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://kubernetes.io/docs/setup/best-practices/cluster-large/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# kube-controller-manager concurrency and client QPS

## Symptoms that point here
- Deployments created in bulk take minutes to get pods; Jobs start slowly.
- EndpointSlices lag after pod churn → traffic to dead pods.
- Namespace deletions sit in Terminating for a long time.
- Metrics: `workqueue_depth{name="deployment"}` growing, `workqueue_queue_duration_seconds`
  p99 high, `rest_client_rate_limiter_duration_seconds` (client-side throttling) non-zero.
- Logs: `Waited for 1.2s due to client-side throttling, not priority and fairness`.

## The knobs
```yaml
# kubeadm ClusterConfiguration controllerManager.extraArgs
- {name: kube-api-qps, value: "100"}       # default 20
- {name: kube-api-burst, value: "200"}     # default 30
- {name: concurrent-deployment-syncs, value: "10"}   # default 5
- {name: concurrent-replicaset-syncs, value: "10"}   # default 5
- {name: concurrent-endpoint-syncs, value: "10"}     # default 5
- {name: concurrent-service-endpoint-syncs, value: "10"}   # EndpointSlice controller, default 5
- {name: concurrent-gc-syncs, value: "40"}           # default 20
- {name: concurrent-namespace-syncs, value: "20"}    # default 10
- {name: concurrent-job-syncs, value: "10"}          # default 5
- {name: concurrent-statefulset-syncs, value: "10"}   # default 5
```
Raise QPS first — more workers behind a 20 QPS client just queue on the rate limiter. Then
raise workers for the controller whose workqueue is deep.

## Guardrails
- The apiserver protects itself with API Priority and Fairness; requests from built-in
  controllers use the `workload-high` priority level, and leader-election requests use the
  `leader-election` level. Raising QPS massively can starve other clients at those levels —
  watch `apiserver_flowcontrol_rejected_requests_total`.
- Disable controllers you do not use with `--controllers=*,-<controller-name>`. Names end in
  `-controller` (for example `ttl-controller`; the flag reference lists them all). Some
  controllers, such as `bootstrap-signer-controller` and `token-cleaner-controller`, are already
  disabled by default, so check the list for your version before editing the flag.
- `--node-monitor-grace-period`, `--terminated-pod-gc-threshold` are also controller-manager
  flags but tune behaviour, not throughput.

## Measure
```bash
# scrape https://<control-plane-node>:10257/metrics (the default --secure-port) with a credential
# that is authorised for the /metrics non-resource URL
# Prometheus:
sum by (name) (workqueue_depth{job="kube-controller-manager"})
histogram_quantile(0.99, sum by (le,name) (rate(workqueue_queue_duration_seconds_bucket{job="kube-controller-manager"}[5m])))
```

## Gotchas
- Only the leader does work; tuning must be applied to every control-plane node's manifest.
- On managed clusters, check whether your provider exposes these flags at all; if not, take
  the workqueue evidence to the provider.

## Verify
- [ ] Workqueue depth returns to ~0 within a minute after a 500-pod burst.
- [ ] No client-side throttling log lines under normal load.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; v1.37 is the latest release): kube-controller-manager reference, API Priority and Fairness page, metrics reference; client-go `rest/request.go`. Confirmed: defaults for `--kube-api-qps` (20), `--kube-api-burst` (30), `--concurrent-deployment-syncs`, `-replicaset-`, `-endpoint-`, `-service-endpoint-`, `-job-`, `-statefulset-` (5), `-gc-` (20), `-namespace-` (10), `--terminated-pod-gc-threshold` (12500), `--node-monitor-grace-period` (50s), `--secure-port` (10257); APF levels `workload-high` and `leader-election`; metric names `workqueue_depth`, `workqueue_queue_duration_seconds`, `rest_client_rate_limiter_duration_seconds`, `apiserver_flowcontrol_rejected_requests_total`; the "client-side throttling, not priority and fairness" log text. Fixed: the controller names in the `--controllers` example (current names are `bootstrap-signer-controller` and `token-cleaner-controller`, both disabled by default), the APF priority level (`system` is not the level for controller traffic) and the unsupported `concurrent-job-syncs` version note. Removed as unconfirmed: the claim that kubeadm needs those controllers for joins and the cloud-controller-manager remark.

Method: documentation only; no commands were run.
