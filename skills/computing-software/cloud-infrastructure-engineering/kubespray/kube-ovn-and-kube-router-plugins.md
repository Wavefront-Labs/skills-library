---
id: computing-software.cloud-infrastructure-engineering.kubespray.kube-ovn-and-kube-router-plugins
name: kube-ovn-and-kube-router-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [kube-ovn, kube-router, cni, bgp, daemonset, ipvsadm, gobgp]
level: practitioner
status: docs-checked
description: "Enable and verify Kube-OVN (kernel 3.10.0-862 bug, kube-ovn namespace) and kube-router (BGP routing, Pod Toolbox, annotations) in Kubespray."
sources:
  - https://kubespray.io/docs/CNI/kube-ovn.md
  - https://kubespray.io/docs/CNI/kube-router.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Kube-OVN** integrates OVN-based network virtualization with Kubernetes. Enable it in `group_vars/k8s_cluster/k8s_cluster.yml`:

```yml
kube_network_plugin: kube-ovn
```

Warning: the kernel (`cat /proc/version`) must not be `3.10.0-862`; kube-ovn will not start and prints that it has a NAT bug and needs a version greater than `3.10.0-898`. Verify with `kubectl get pod -n kube-ovn` (expect `kube-ovn-cni`, `kube-ovn-controller`, `ovn-central`, `ovs-ovn` pods) and `kubectl get subnet`, which lists `join` (100.64.0.0/16) and `ovn-default` (10.16.0.0/16) in the sample.

**Kube-router** is an L3 CNI provider that sets up IPv4 routing between nodes. It runs as a DaemonSet in `kube-system`:

```ShellSession
kubectl get pod --namespace=kube-system -l k8s-app=kube-router -owide
kubectl logs --namespace=kube-system -l k8s-app=kube-router | grep Peer.Up
```

The second shows BGP "Peer Up" lines. Each pod bundles a Pod Toolbox with `ipvsadm` for IPVS and `gobgp` for BGP peering and routes; use `kubectl exec -it` into the container.

Override `kube_router_...` variables from `roles/network_plugin/kube-router/defaults/main.yml`. For advanced BGP, annotations are applied with:

```yml
kube_router_annotations_master: []
kube_router_annotations_node: []
kube_router_annotations_all: []
```

## Checked

2026-11-08. Cited pages re-read in full. Both plugins' enablement, verification and variables were confirmed on the Kube-OVN and Kube-router pages.

Method: documentation only; no commands were run.
