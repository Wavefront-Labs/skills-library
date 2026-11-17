---
id: computing-software.cloud-infrastructure-engineering.metallb.pod-security-privileged-namespace
name: pod-security-privileged-namespace
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, pod-security, privileged, namespace-labels, pod-security-admission, speaker]
level: practitioner
status: docs-checked
description: "Label the MetalLB namespace privileged so the speaker, which needs elevated permissions, can run under Kubernetes pod security admission."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod security admission

The speaker pod needs elevated permission for its network functions. If your Kubernetes version enforces pod security admission (beta in k8s 1.23 per the docs), the namespace MetalLB runs in must carry these labels:

```yaml
  labels:
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: privileged
    pod-security.kubernetes.io/warn: privileged
```

`metallb-system` is the namespace the manifests deploy into.

OpenShift uses SCCs instead: `computing-software.cloud-infrastructure-engineering.metallb.openshift-and-openstack-prereqs`.

## Checked

2026-11-04. Confirmed against the MetalLB Installation page note (speaker needs elevated permission, pod security admission beta in k8s 1.23, the three privileged labels, metallb-system namespace). Removed the kubectl label command and the symptom/events check, which the page does not give.

Method: documentation only; no commands were run.
