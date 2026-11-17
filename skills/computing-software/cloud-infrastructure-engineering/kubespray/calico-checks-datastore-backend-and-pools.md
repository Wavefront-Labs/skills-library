---
id: computing-software.cloud-infrastructure-engineering.kubespray.calico-checks-datastore-backend-and-pools
name: calico-checks-datastore-backend-and-pools
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [calico, calicoctl, datastore, typha, network-backend, ippool]
level: practitioner
status: docs-checked
description: "Check Calico health with calicoctl.sh and set calico_datastore (kdd or etcd), calico_network_backend (bird, vxlan, none) and the default pool CIDRs."
sources:
  - https://kubespray.io/docs/CNI/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Checks.** Confirm the container with `docker ps | grep calico`. `calicoctl.sh` is a wrapper with credentials configured. Useful commands: `calicoctl.sh node status`, `calicoctl.sh get ippool -o wide`, `calicoctl.sh get workloadEndpoint -o wide` and `calicoctl.sh get hostEndpoint -o wide`.

**Datastore.** `calico_datastore` is `kdd` (default, the Kubernetes API datastore, recommended on-premises, Kubernetes workloads only) or `etcd` (best for hybrid deployments). With kdd and more than 50 nodes, consider the `typha` daemon for scaling.

```yml
calico_datastore: kdd
```

**Network backend.** `calico_network_backend` allows `bird`, `vxlan` or `none`; `vxlan` is the default.

```yml
calico_network_backend: none
```

**Pool CIDRs.** The default IP pool uses `kube_pods_subnet` (and `kube_pods_subnet_ipv6`). To add several pools without Kubernetes treating them as external, they must lie within or equal to those ranges. Set the default pool in `k8s_cluster/k8s-net-calico.yml`:

```ShellSession
calico_pool_cidr: 10.233.64.0/20
calico_pool_cidr_ipv6: fd85:ee78:d8a6:8607::1:0000/112
```

The rest of Calico configuration (encapsulation, BGP, eBPF) is covered in sibling skills.

## Checked

2026-11-08. Cited pages re-read in full. Commands and variables were confirmed on the Calico page, up to the pool CIDR section.

Method: documentation only; no commands were run.
