---
id: computing-software.cloud-infrastructure-engineering.calico.ebpf-dataplane-requirements-and-enable
name: ebpf-dataplane-requirements-and-enable
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ebpf, dataplane, bpf, installation, operator, kernel, vxlan, kube-proxy]
level: practitioner
status: docs-checked
description: "Enable the Calico eBPF data plane: kernel and platform support, unsupported cases, the operator patch for kubeadm clusters, manual enablement and effect on existing connections."
sources:
  - https://docs.tigera.io/calico/latest/operations/ebpf/enabling-ebpf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Supported.** x86-64 and arm64; Kubernetes datastore driver (not etcd); generic or kubeadm, kOps, OpenShift, EKS, RKE2 (supports disabling kube-proxy), MKE, and AKS with limitations. Kernel: Ubuntu 22.04; Red Hat 8.4 with kernel 4.18.0-305 or above (features backported); otherwise another distribution with kernel 5.10 or above. Check with `uname -rv`. The network must carry VXLAN between hosts, since eBPF mode uses VXLAN to forward NodePort traffic. IPIP is not supported; use VXLAN if you need an overlay.

**Not supported.** GKE, etcd datastore, mixed eBPF and standard or Windows nodes, floating IPs, SCTP, and VLAN traffic without hardware offload.

**Automatic enablement** (kubeadm-created cluster, operator install, kube-proxy in `kube-system` not managed by Helm or Argo CD):

```bash
kubectl patch installation.operator.tigera.io default --type merge -p '{"spec":{"calicoNetwork":{"linuxDataplane":"BPF", "bpfNetworkBootstrap":"Enabled", "kubeProxyManagement":"Enabled"}}}'
```

The operator configures API server addresses and disables kube-proxy. Nodes switch at slightly different times, which can disturb NodePort traffic briefly.

**Manual enablement.** For operator installs set only `linuxDataplane` to `BPF`. For manifest installs: `calicoctl patch felixconfiguration default --patch='{"spec": {"bpfEnabled": true}}'`.

**Existing connections.** TCP survives because translation lives in conntrack. Non-TCP flows are treated as new, so UDP may move backends, and flows allowed only as established replies are dropped. Connections over VXLAN do not survive, since the device is recreated.

## Checked

2026-11-08. The Enabling the eBPF data plane page was read in full. Support lists, the patch commands and the connection behaviour were confirmed. Corrected the kernel requirements, which previously named Ubuntu 24.04, RHEL 9 and kernel 5.17; the page lists Ubuntu 22.04, Red Hat 8.4 (4.18.0-305+) and kernel 5.10 or above.

Method: documentation only; no commands were run.
