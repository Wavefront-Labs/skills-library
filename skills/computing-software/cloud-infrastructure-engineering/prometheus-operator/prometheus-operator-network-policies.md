---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-network-policies
name: prometheus-operator-network-policies
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [network-policy, alertmanager-mesh-port, node-exporter-networkpolicy, kube-state-metrics-networkpolicy, default-deny]
level: advanced
status: docs-checked
description: "Write NetworkPolicies for an operator-based monitoring stack: Alertmanager web and mesh, Prometheus, Grafana, node-exporter and kube-state-metrics."
sources:
  - https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/network-policies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With a default-deny posture, the monitoring components need explicit allowances. The Prometheus Operator docs first apply a `default-deny-all` policy to the `monitoring` namespace (denying all ingress), say the example was only tested with the Calico provider, then apply these `NetworkPolicy` objects:

- **Alertmanager web:** allow inbound TCP 9093 from any source to pods labelled `alertmanager: main` and `app.kubernetes.io/name: alertmanager`.
- **Alertmanager mesh:** allow TCP and UDP port 9094 from pods labelled `app=alertmanager` and `alertmanager=main` to pods labelled `alertmanager: main` and `app.kubernetes.io/name: alertmanager`.- **Grafana:** allow inbound TCP 3000 from any source to pods `app: grafana`.
- **Prometheus:** allow inbound TCP 9090 from any source to pods `app.kubernetes.io/name: prometheus` and `prometheus: k8s`.
- **node-exporter:** allow inbound TCP 9100 only from pods labelled `app=prometheus` and `prometheus=k8s`, to pods `app: node-exporter`.
- **kube-state-metrics:** allow inbound TCP 8080 only from the same Prometheus pods, to `app: kube-state-metrics`.

## Notes
Adjust labels to your instance names. The Prometheus ingress rule is open to any source; narrow it if the UI is only reached by Grafana or an ingress controller. The page covers ingress policies only.

## Checked

2026-11-08. Read the network policies page in full. Ports and selectors match. Added the Alertmanager 9093 policy, the default-deny step and the Calico-only testing note; removed an unsourced egress remark.

Method: documentation only; no commands were run.
