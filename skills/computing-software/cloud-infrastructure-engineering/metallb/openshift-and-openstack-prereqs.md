---
id: computing-software.cloud-infrastructure-engineering.metallb.openshift-and-openstack-prereqs
name: openshift-and-openstack-prereqs
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, openshift, openstack, scc, anti-spoofing, arp-spoofing, allowed-address, runasuser]
level: advanced
status: docs-checked
description: "Make MetalLB run on OpenShift (remove runAsUser/fsGroup, grant privileged SCC) and on OpenStack (disable ARP spoofing protection or allow addresses) for L2 mode."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/clouds.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/faq/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenShift and OpenStack

## OpenShift OCP
1. Remove the hardcoded UID: delete `spec.template.spec.securityContext.runAsUser` from both the `controller` Deployment and the `speaker` DaemonSet (OpenShift assigns UIDs from its managed range).
2. Also delete `spec.template.spec.securityContext.fsGroup` (allowed group IDs are 5000 through 5999).
3. Grant the speaker elevated privileges for raw networking:
```bash
oc adm policy add-scc-to-user privileged -n metallb-system -z speaker
```
If deployed via Helm the ServiceAccount is `metallb-speaker`.

## OpenStack
For L2 mode, OpenStack's ARP spoofing protection treats MetalLB announcing unknown IPs as an attack. The cloud page says you must disable it on all VMs running Kubernetes, since there is no way to make OpenStack cooperate.

The FAQ gives a finer option: anti-spoofing prevents VMs using IPs not configured in the OpenStack control plane; see `openstack port set --allowed-address` (python-openstackclient) to allow the LoadBalancer IPs.

## Checked

2026-11-04. Confirmed against the MetalLB Cloud Compatibility page (OpenShift runAsUser and fsGroup removal, group ID range 5000 through 5999, the oc adm policy command, Helm ServiceAccount name metallb-speaker, OpenStack ARP spoofing protection) and the FAQ (anti-spoofing and `openstack port set --allowed-address`). Removed the unsupported arping Verify line.

Method: documentation only; no commands were run.
