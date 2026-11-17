---
id: computing-software.cloud-infrastructure-engineering.metallb.install-with-helm
name: install-with-helm
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, helm, helm-chart, values, install, speaker, controller, loglevel]
level: practitioner
status: docs-checked
description: "Install MetalLB with the Helm chart, pass a values file, remember CRs must match the release namespace, and set the BGP backend and log levels via values."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install with Helm

```bash
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb
# with a values file (recommended for configs)
helm install metallb metallb/metallb -f values.yaml
```
Chart repo: `https://metallb.github.io/metallb`.

Gotchas:
- If you installed with Helm, the namespace of your configuration CRs must match the namespace MetalLB was deployed into (the docs' examples use `metallb-system`).
- With Helm, the speaker ServiceAccount is `metallb-speaker` (matters for OpenShift SCC, see `computing-software.cloud-infrastructure-engineering.metallb.openshift-and-openstack-prereqs`).
- The chart upgrades CRDs automatically; no manual CRD upgrade is needed.
- The chart default BGP backend is FRR-K8s; set values for others (`computing-software.cloud-infrastructure-engineering.metallb.select-bgp-backend`).
- Other values mentioned in the docs: `loadBalancerClass`, `.controller.loglevel` and `.speaker.loglevel` (set to debug when collecting a bug report), `speaker.gratuitousARPInterval`, `prometheus.prometheusRule.enabled` (default false).
- Enforced pod security needs a labelled namespace: `computing-software.cloud-infrastructure-engineering.metallb.pod-security-privileged-namespace`.

## Checked

2026-11-04. Confirmed against the MetalLB Installation page (helm repo and install commands, values file, chart upgrades CRDs, FRR-K8s chart default, loadBalancerClass, prometheus.prometheusRule.enabled default false), Configuration page (CR namespace must match Helm namespace), Troubleshooting page (.controller.loglevel, .speaker.loglevel) and the layer 2 concepts page (speaker.gratuitousARPInterval). Removed the generic Check line.

Method: documentation only; no commands were run.
