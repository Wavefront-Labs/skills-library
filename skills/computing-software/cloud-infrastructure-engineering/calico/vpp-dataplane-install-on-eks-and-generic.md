---
id: computing-software.cloud-infrastructure-engineering.calico.vpp-dataplane-install-on-eks-and-generic
name: vpp-dataplane-install-on-eks-and-generic
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [vpp, dataplane, eks, dpdk, hugepages, calico-vpp-config, install, operator]
level: practitioner
status: docs-checked
description: "Install Calico with the VPP data plane: operator-only, blank cluster, EKS with aws-node removed, and the calico-vpp-config ConfigMap fields SERVICE_PREFIX and uplinkInterfaces."
sources:
  - https://docs.tigera.io/calico/latest/getting-started/kubernetes/vpp/getting-started
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VPP is a userspace data plane from fd.io. Advantages named by the page: higher throughput especially with WireGuard, better encryption performance with IPsec, native service handling without kube-proxy (lower first-packet latency, client source IP preserved to the pod), and optional `memif` userspace interfaces for pods. VPP nodes can coexist with regular nodes, which allows gradual migration. Only operator-based installs are supported, and some features differ or are unsupported (see the known-issues page).

**Requirements.** A blank cluster where no CNI was ever configured, plus the base requirements minus those about `cali*`, `tunl*` and `vxlan.calico`. With kubeadm, pass `--pod-network-cidr`, for example `sudo kubeadm init --pod-network-cidr=192.168.0.0/16`. Optional hugepages: at least 512 x 2MB, and the `vfio-pci` or `uio_pci_generic` module loaded.

**Generic cluster sequence.**

1. Create the CRDs and `tigera-operator.yaml` as usual.
2. Apply `installation-default.yaml` from the projectcalico/vpp-dataplane repository (review the pool CIDR first).
3. Download `calico-vpp.yaml` (with hugepages) or `calico-vpp-nohuge.yaml` (without, or if unsure) from the same repository.
4. Edit the `calico-vpp-config` ConfigMap, then apply.

Required ConfigMap settings: `SERVICE_PREFIX`, the service CIDR (`kubectl cluster-info dump | grep -m 1 service-cluster-ip-range`; default `10.96.0.0/12`), and the uplink:

```yaml
CALICOVPP_INTERFACES: |-
  {
      "uplinkInterfaces": [ { "interfaceName": "eth0" } ]
  }
```

The interface must be up with an address that is the Kubernetes node address.

**EKS.** Create the cluster with `eksctl create cluster --name my-calico-cluster --without-nodegroup`, delete the `aws-node` DaemonSet, use `installation-eks.yaml` and `calico-vpp-eks.yaml`, then add nodes with `--max-pods-per-node 50`. A separate DPDK variant needs hugepage preparation of the workers.

## Checked

2026-11-04. Advantages, requirements, file names and ConfigMap fields were confirmed on the Get started with VPP networking page.

Method: documentation only; no commands were run.
