---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-troubleshooting-servicemonitor
name: prometheus-operator-troubleshooting-servicemonitor
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [troubleshooting, servicemonitor-not-picked-up, target-discovery, port-name-vs-number, rejected-resources, events]
level: practitioner
status: docs-checked
description: "Diagnose a ServiceMonitor that Prometheus does not use: selectors, Service existence, port name versus number, generated config, and rejection events."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A ServiceMonitor references a **Service** (not a Deployment or Pod) by labels and by **port name**. Walk the chain.

1. **Selection:** the monitor and its namespace must match `serviceMonitorSelector` and `serviceMonitorNamespaceSelector` on the Prometheus. The Prometheus ServiceAccount must be allowed to get, list and watch Services and Endpoints in the target namespace.
2. **Is it in the generated config?** Grep the Secret:
```sh
kubectl -n monitoring get secret prometheus-k8s -ojson | jq -r '.data["prometheus.yaml.gz"]' | base64 -d | gunzip | grep "my-service-monitor"
```
Or port-forward `svc/prometheus-operated 9090:9090` and look at configuration and targets.
3. **In config but not under Service Discovery:** no Service matches `.spec.selector`. List Services with the monitor labels.
4. **Port:** use the Service port **name**. `port: "8080"` fails with `spec.endpoints.port in body must be of type string: "integer"`; use `web`, the name defined on the Service. The Service port name is optional in Kubernetes but required here.
5. **Rejected objects:** the operator rejects invalid `AlertmanagerConfig`, `PrometheusRule`, `ServiceMonitor`, `PodMonitor`, `Probe` and `ScrapeConfig` and emits events:
```sh
kubectl get events --field-selector=involvedObject.name="<name>" -n "<namespace>"
```
kube-prometheus ships the `PrometheusOperatorRejectedResources` alert.

6. **Kubelet 403 Forbidden (all targets down):** the docs report fixing this on kubeadm clusters by enabling `--authentication-token-webhook=true` on the kubelet (in its kubeadm systemd drop-in) and changing `--address=127.0.0.1` to `--address=0.0.0.0` in the kube-controller-manager and kube-scheduler static pod manifests.

## Checked

2026-11-08. Read the troubleshooting page in full. Rewrote the kubelet 403 item to state exactly what the docs changed (kubelet token webhook, address flags on controller-manager and scheduler).

Method: documentation only; no commands were run.
