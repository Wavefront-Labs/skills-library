---
id: computing-software.cloud-infrastructure-engineering.kubernetes.operator-metrics-controller-runtime-and-secure-serving
name: operator-metrics-controller-runtime-and-secure-serving
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, controller-runtime-metrics, kube-rbac-proxy, operators, kubebuilder, prometheus, observability]
level: advanced
status: docs-checked
description: "Expose and protect operator metrics: built-in controller-runtime reconcile/workqueue metrics, custom metrics, secure serving that replaced kube-rbac-proxy, and scraping RBAC."
sources: ["https://book.kubebuilder.io/reference/metrics", "https://book.kubebuilder.io/reference/metrics-reference", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/metrics/server", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/metrics/filters", "https://github.com/brancz/kube-rbac-proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator metrics: controller-runtime and kube-rbac-proxy

## Built-in metrics worth alerting on
| Metric | Meaning |
|---|---|
| `controller_runtime_reconcile_total{controller,result}` | results: success, error, requeue, requeue_after |
| `controller_runtime_reconcile_errors_total` | rising = broken reconcile |
| `controller_runtime_reconcile_time_seconds` | histogram; slow API calls or external deps |
| `workqueue_depth{name}` | backlog; sustained growth = cannot keep up |
| `workqueue_queue_duration_seconds` | time items wait before processing |
| `workqueue_retries_total` | hot-looping objects |
| `controller_runtime_active_workers` vs `max_concurrent_reconciles` | saturation |
| `rest_client_requests_total{code}` | API throttling (429) and errors |

## Secure serving (current Kubebuilder scaffold)
Projects initialised with Kubebuilder v3.14 or lower protect metrics with the kube-rbac-proxy
sidecar, and the `gcr.io/kubebuilder/kube-rbac-proxy` images are unavailable from early 2025.
Projects initialised with v4.1.0 or higher use controller-runtime's own authn/authz:
```go
import (
  metricsserver "sigs.k8s.io/controller-runtime/pkg/metrics/server"
  "sigs.k8s.io/controller-runtime/pkg/metrics/filters"
)
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
  Metrics: metricsserver.Options{
    BindAddress:    ":8443",
    SecureServing:  true,
    FilterProvider: filters.WithAuthenticationAndAuthorization,
    // CertDir: "/tmp/k8s-metrics-server/metrics-certs"  // cert-manager cert; self-signed otherwise
  },
})
```
The operator ServiceAccount then needs permission to review tokens and access
(the scaffold's `metrics_auth_role.yaml` and `metrics_auth_role_binding.yaml`).

## Scraper RBAC
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata: {name: myop-metrics-reader}
rules:
- nonResourceURLs: [/metrics]
  verbs: [get]
```
Bind it to the Prometheus service account (scaffolded as `metrics_reader_role.yaml`). ServiceMonitor:
```yaml
endpoints:
- port: https
  scheme: https
  path: /metrics
  bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
  tlsConfig: {}   # verify with the CA from the cert-manager secret (see the book's cert-manager section); the default certificate is self-signed
```

## Custom metrics
```go
var reconcileDrift = prometheus.NewCounterVec(
  prometheus.CounterOpts{Name: "myop_drift_corrections_total", Help: "Drift fixed"},
  []string{"kind"})
func init() { metrics.Registry.MustRegister(reconcileDrift) }   // controller-runtime's registry
```
Registering on the default Prometheus registry instead means the metric never appears.
Keep labels low-cardinality: kind/namespace, never object name for large fleets.

## Verify
```bash
kubectl -n myop-system port-forward deploy/myop-controller-manager 8443 &
TOKEN=$(kubectl create token prometheus-k8s -n monitoring)
curl -sk -H "Authorization: Bearer $TOKEN" https://localhost:8443/metrics | grep controller_runtime_reconcile_total
```

## Checked
2026-10-26. Checked against the Kubebuilder book metrics pages and the controller-runtime metrics source (repositories kubernetes-sigs/kubebuilder, last commit 2026-10-25, and kubernetes-sigs/controller-runtime, last commit 2026-10-19). Confirmed: metric names in the reference (`controller_runtime_reconcile_total` with labels controller and result and values success, error, requeue, requeue_after; `controller_runtime_reconcile_errors_total`; `controller_runtime_reconcile_time_seconds`; `controller_runtime_active_workers`; `controller_runtime_max_concurrent_reconciles`; workqueue metrics; `rest_client_requests_total`); projects initialised with Kubebuilder v3.14 or lower used kube-rbac-proxy and `gcr.io/kubebuilder/kube-rbac-proxy` images are unavailable from early 2025; v4.1.0 or higher use `filters.WithAuthenticationAndAuthorization`; default metrics port 8443; scaffold files `metrics_auth_role.yaml`, `metrics_auth_role_binding.yaml`, `metrics_reader_role.yaml`; custom metrics register with `metrics.Registry.MustRegister`; certificates are self-signed unless cert-manager is enabled. Removed as unconfirmed: the 401 response and the insecureSkipVerify scrape setting as a recommendation.
Method: documentation only; no commands were run.
