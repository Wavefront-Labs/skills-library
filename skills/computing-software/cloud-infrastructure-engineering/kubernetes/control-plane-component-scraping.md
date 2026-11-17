---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-component-scraping
name: control-plane-component-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, prometheus, kube-prometheus-stack, etcd, kube-scheduler, kube-controller-manager, control-plane]
level: practitioner
status: docs-checked
description: "Scrape kube-controller-manager, kube-scheduler and etcd metrics on kubeadm clusters by fixing bind addresses, HTTPS, authorization and Service discovery."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack", "https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml", "https://etcd.io/docs/v3.5/op-guide/monitoring/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/", "https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/master.yaml", "https://docs.aws.amazon.com/eks/latest/userguide/view-raw-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scraping control-plane components

kube-controller-manager serves HTTPS on port 10257 and kube-scheduler on 10259 by default. CIS
checks 1.3.7 and 1.4.2 want `--bind-address=127.0.0.1` (or unset) on both, and etcd exposes metrics on
the URLs given by `--listen-metrics-urls` (the kube-prometheus-stack chart scrapes port 2381 by default).
When those listeners are loopback-only, Prometheus pods cannot reach them and the chart's targets show DOWN.

## Change the bind addresses (this trades off CIS 1.3.7 and 1.4.2)
```yaml
# kubeadm ClusterConfiguration (v1beta4: extraArgs is a list of name/value pairs)
controllerManager:
  extraArgs: [{name: bind-address, value: "0.0.0.0"}]
scheduler:
  extraArgs: [{name: bind-address, value: "0.0.0.0"}]
etcd:
  local:
    extraArgs: [{name: listen-metrics-urls, value: "http://0.0.0.0:2381"}]
```
On running nodes edit the static pod manifests. Prefer binding
to the node IP over `0.0.0.0`, firewall these ports to the monitoring network, and record the accepted
CIS exception.

## Authorization
Controller manager and scheduler serve `/metrics` over HTTPS with delegated authn/authz. The Kubernetes
system-metrics page gives the ClusterRole Prometheus needs:
```yaml
rules:
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
```

## kube-prometheus-stack values
```yaml
kubeControllerManager:
  service: {port: 10257, targetPort: 10257}
  serviceMonitor: {https: true}
kubeScheduler:
  service: {port: 10259, targetPort: 10259}
  serviceMonitor: {https: true}
kubeEtcd:
  service: {port: 2381, targetPort: 2381}
```
In the chart's current `values.yaml` these ServiceMonitors send a bearer token from a chart-managed secret and
use a `tlsConfig` with `insecureSkipVerify: true` and the `kube-root-ca.crt` CA; override `tlsConfig`
(for example etcd client certificates under `kubeEtcd.serviceMonitor`) if you want verification.
If a component is not a pod, list its node IPs in `kubeControllerManager.endpoints` (and the same for the
scheduler and etcd); the chart then uses only `port` and `targetPort` from `service`.

## Managed clusters
Control-plane components are usually not scrapeable. On EKS the scheduler and controller manager metrics
are served through the API server under the `metrics.eks.amazonaws.com` API group
(`kubectl get --raw "/apis/metrics.eks.amazonaws.com/v1/ksh/container/metrics"` for the scheduler); check
your provider's documentation for the others.

## Verify
Targets for kube-controller-manager, kube-scheduler and kube-etcd are UP, and `workqueue_depth` and etcd
metrics such as `etcd_disk_backend_commit_duration_seconds_bucket` return data.

## Checked
2026-10-28. Confirmed: secure ports 10257 and 10259 against the controller-manager and scheduler
references; CIS 1.3.7 and 1.4.2 against kube-bench `cfg/cis-1.9`; `--listen-metrics-urls` against the etcd
monitoring page; port 2381, `endpoints`, `https`, bearer-token authorization and `tlsConfig` defaults
against the chart's `values.yaml`; the `/metrics` ClusterRole against the system-metrics page; list-form
`extraArgs` against the kubeadm v1beta4 page; the EKS metrics API group, scheduler command and
`workqueue_depth` against the EKS "view raw metrics" page and the Kubernetes metrics reference. Removed:
the claim that kubeadm binds etcd metrics to 127.0.0.1:2381 (the kubeadm pages read do not say so; check
the etcd manifest), `etcd_server_has_leader` (not on the pages read), the `serviceMonitor.insecureSkipVerify`
key (current chart uses `tlsConfig`), and the GKE and AKS control-plane metrics claims.
Method: documentation only; no commands were run.
