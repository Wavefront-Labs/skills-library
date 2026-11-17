---
id: computing-software.cloud-infrastructure-engineering.metallb.install-with-operator
name: install-with-operator
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, operator, operatorhub, olm, csv, metallb-bgp-type, frr-k8s]
level: practitioner
status: docs-checked
description: "Deploy MetalLB through the OperatorHub MetalLB Operator and switch its BGP backend to frr-k8s by editing the METALLB_BGP_TYPE env var in the ClusterServiceVersion."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MetalLB Operator

The MetalLB Operator (operatorhub.io/operator/metallb-operator) eases deployment and life-cycle of MetalLB and lets you configure it through CRDs.

Enable the recommended FRR-K8s backend: edit the ClusterServiceVersion named `metallb-operator`:
```bash
kubectl edit csv metallb-operator
```
and set on the `manager` container:
```yaml
- name: METALLB_BGP_TYPE
  value: frr-k8s
```
FRR mode is deprecated; if you use it via the Operator, plan to migrate to `frr-k8s` with the same change.

Debug logging: the Operator's MetalLB CRD has a loglevel field (use debug when collecting a bug report, see `computing-software.cloud-infrastructure-engineering.metallb.bug-report-collection`).

## Checked

2026-11-04. Confirmed against the MetalLB Installation page (OperatorHub operator, `kubectl edit csv metallb-operator`, METALLB_BGP_TYPE=frr-k8s on the manager container, FRR mode deprecated) and the Troubleshooting page (operator loglevel field in the MetalLB CRD). Removed the unsupported pod-check line.

Method: documentation only; no commands were run.
