---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-network-policy-controller
name: k3s-network-policy-controller
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, network-policy, kube-router, disable-network-policy]
level: practitioner
status: docs-checked
description: "Use or disable the embedded kube-router network policy controller and clean up its iptables rules."
sources:
  - https://docs.k3s.io/networking/networking-services
  - https://docs.k3s.io/installation/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
K3s includes an embedded network policy controller built on kube-router's netpol controller library (no other kube-router features are present).

Disable it by starting each server with `--disable-network-policy`.

Cleanup note: the network policy iptables rules are not removed when you change the configuration to disable the controller. To clean up the kube-router rules, run k3s-killall.sh, or clean them with iptables-save and iptables-restore. This must be done manually on every node:

```
iptables-save | grep -v KUBE-ROUTER | iptables-restore
ip6tables-save | grep -v KUBE-ROUTER | ip6tables-restore
```

Security reminder from the requirements page: Flannel uses the Bridge CNI plugin to create an L2 network. Pods with NET_RAW capability can abuse it for attacks such as ARP spoofing, so use a restricted pod security profile that drops NET_RAW for untrusted pods.

## Checked

2026-11-08. Read the full K3s Networking Services page (docs/networking/networking-services.md) and the full Requirements page (docs/installation/requirements.md) in the k3s-io/docs repo. Confirmed: embedded kube-router netpol library only, --disable-network-policy on each server, the iptables cleanup via k3s-killall.sh or iptables-save/restore on every node, and the Bridge CNI NET_RAW warning with a restricted profile. Removed the HA same-flag claim, the custom-CNI advice, the claim about network policies and NET_RAW, and the related-flags line (none are on the pages).

Method: documentation only; no commands were run.
