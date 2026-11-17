---
id: computing-software.cloud-infrastructure-engineering.calico.wireguard-encryption-enable-and-per-node-disable
name: wireguard-encryption-enable-and-per-node-disable
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [wireguard, encryption, felixconfiguration, wireguardenabled, pod-traffic, eks, aks, openshift]
level: practitioner
status: docs-checked
description: "Encrypt inter-node pod traffic with Calico WireGuard: FelixConfiguration patches, EKS/AKS host-network encryption, per-node opt-out."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/encrypt-cluster-pod-traffic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico manages WireGuard tunnels between nodes. There is no sidecar, so traffic is encrypted only between nodes, not for the whole pod-to-pod path.

**Support (from the page).** Inter-node pod traffic: IPv4. Inter-node host-network traffic: only on managed EKS and AKS clusters. Not supported: same-node pod traffic, GKE, custom keys.

**Prerequisites.** WireGuard in the node OS (in the kernel from 5.6, backported in some distributions; reboot may be needed). Not every node needs it, but traffic to or from a node without it is not encrypted. Each node needs an IP, which autodetection provides. AKS nodes already have it. The page gives a default Amazon Linux AMI procedure and an OpenShift 4.8 MachineConfig procedure.

**Enable** (both parameters are in FelixConfiguration):

```bash
kubectl patch felixconfiguration default --type='merge' -p '{"spec":{"wireguardEnabled":true}}'
```

Use `wireguardEnabledV6` for IPv6, or set both in one patch. `calicoctl patch` takes the same arguments. For EKS or AKS using the cloud provider CNI (not Calico CNI), also encrypt host-network traffic:

```bash
calicoctl patch felixconfiguration default --type='merge' -p '{"spec": {"wireguardHostEncryptionEnabled": true}}'
```

**Disable on one node** with a node-specific FelixConfiguration named `node.<node name>`:

```yaml
apiVersion: projectcalico.org/v3
kind: FelixConfiguration
metadata:
  name: node.my-node
spec:
  logSeverityScreen: Info
  reportingInterval: 0s
  wireguardEnabled: false
  wireguardEnabledV6: false
```

No traffic to or from that node is encrypted. Review MTU after enabling.

## Checked

2026-11-08. The whole Encrypt in-cluster pod traffic page was read: support and unsupported lists, prerequisites (Linux 5.6+, AKS preinstalled, node IPs), the kubectl and calicoctl patch commands, wireguardHostEncryptionEnabled, the node.<name> FelixConfiguration override, and the MTU recommendation all match.

Method: documentation only; no commands were run.
