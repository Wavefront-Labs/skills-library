---
id: computing-software.cloud-infrastructure-engineering.calico.nftables-dataplane-install
name: nftables-dataplane-install
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [nftables, dataplane, kube-proxy, kubeadm, install, linuxdataplane, operator]
level: practitioner
status: docs-checked
description: "Install Calico in nftables data plane mode: kube-proxy must also use nftables, kernel 5.13 or later with nft 1.0.1, and the Installation with linuxDataplane Nftables."
sources:
  - https://docs.tigera.io/calico/latest/getting-started/kubernetes/nftables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubernetes added a beta nftables kube-proxy mode in v1.31. Calico's nftables data plane is compatible with it, and **the cluster's kube-proxy must also be in nftables mode**:

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: nftables
```

Host requirements: x86-64, arm64, ppc64le or s390x, 2 CPU, 2 GB RAM, 10 GB disk, Linux kernel 5.13 or later with `nft` 1.0.1 or newer, and Calico must be able to manage `cali` and `tunl` interfaces (see the NetworkManager note if present).

The guide builds a single-host cluster with a kubeadm config that includes a `KubeProxyConfiguration` document with `mode: nftables` and `podSubnet: "192.168.0.0/16"` (change it if that range is in use), then `sudo kubeadm init --config=config.yaml`.

Install the CRDs and operator as in the standard operator install, then create the Installation with the nftables data plane:

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    linuxDataplane: Nftables
    ipPools:
    - name: default-ipv4-ippool
      blockSize: 26
      cidr: 192.168.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()
---
apiVersion: operator.tigera.io/v1
kind: APIServer
metadata:
  name: default
spec: {}
```

Adjust the CIDR to your pod network before applying, then `watch kubectl get pods -n calico-system`. On a single node, remove the control-plane taint to schedule workloads.

## Checked

2026-11-04. Requirements, kube-proxy prerequisite, kubeadm configuration and Installation YAML were confirmed on the Calico nftables data plane page.

Method: documentation only; no commands were run.
