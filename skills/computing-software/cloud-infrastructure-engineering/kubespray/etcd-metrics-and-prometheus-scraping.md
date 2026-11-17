---
id: computing-software.cloud-infrastructure-engineering.kubespray.etcd-metrics-and-prometheus-scraping
name: etcd-metrics-and-prometheus-scraping
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [etcd, metrics, prometheus, kube-prometheus-stack, monitoring]
level: practitioner
status: docs-checked
description: "Expose etcd metrics on a separate HTTP port and scrape them with kube-prometheus-stack using etcd_metrics_port, labels for the etcd-metrics service and etcd_listen_metrics_urls."
sources:
  - https://kubespray.io/docs/operations/etcd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To expose etcd metrics on a separate HTTP port, set this in the inventory:

```yaml
etcd_metrics_port: 2381
```

To create a service `etcd-metrics` and its endpoints in the `kube-system` namespace, set labels for it:

```yaml
etcd_metrics_service_labels:
  k8s-app: etcd
  app.kubernetes.io/managed-by: Kubespray
  app: kube-prometheus-stack-kube-etcd
  release: kube-prometheus-stack
```

The last two labels let the kube-prometheus-stack chart scrape the service when it is installed with the release name `kube-prometheus-stack`; if your Helm release has another name, adjust `release`. On the chart side, disable the chart's own service:

```yaml
kubeEtcd:
  service:
    enabled: false
```

To override the exposition URLs completely:

```yaml
etcd_listen_metrics_urls: "http://0.0.0.0:2381"
```

If you instead expose metrics on specific node IPs in `etcd_listen_metrics_urls`, the page shows scraping those endpoints directly by enabling `kubeEtcd` in the chart values and listing each node IP under `endpoints` (the example uses three addresses in 10.141.4.x).

## Checked

2026-11-04. All variable names and YAML blocks were confirmed on the etcd page under Metrics.

Method: documentation only; no commands were run.
