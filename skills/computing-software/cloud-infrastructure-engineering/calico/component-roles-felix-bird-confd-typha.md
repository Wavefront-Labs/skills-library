---
id: computing-software.cloud-infrastructure-engineering.calico.component-roles-felix-bird-confd-typha
name: component-roles-felix-bird-confd-typha
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [architecture, felix, bird, confd, typha, kube-controllers, cni-plugin, dikastes]
level: intro
status: docs-checked
description: "Map each Calico component to its job: Felix, BIRD, confd, Typha, kube-controllers, CNI and IPAM plugins, Dikastes and calicoctl."
sources:
  - https://docs.tigera.io/calico/latest/reference/architecture/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico is a set of cooperating components; knowing which one owns a behaviour tells you where to look.

| Component | Job |
|---|---|
| Felix | Agent on every host that has endpoints. Handles interface management (host answers workload ARP with its own MAC, enables IP forwarding), route programming into the kernel FIB, ACL programming, and state reporting to the datastore |
| BIRD | BGP client on each node running Felix. Takes routes Felix installs and distributes them to peers; can act in route reflector setups |
| confd | Watches the datastore for BGP configuration and global defaults (AS number, logging, IPAM) and generates BIRD config files, then triggers BIRD to reload |
| Typha | Daemon between datastore and Felix/confd; one datastore connection, cached state, deduplicated events |
| CNI plugin | Presents Calico networking to Kubernetes; installed on every node |
| IPAM plugin | Allocates pod IPs from IP pool resources; default for most installs |
| kube-controllers | Policy, namespace, serviceaccount, workloadendpoint and node controllers |
| Calico API server | Lets `kubectl` manage Calico resources; an aggregation API server translating `projectcalico.org/v3` to CRDs |
| Dikastes | Optional Envoy sidecar for Istio, enforcing L3-L7 policy |
| calicoctl | CLI, separate install |

The datastore plugin choice is Kubernetes API datastore (no extra datastore, Kubernetes RBAC and audit logging) or etcd (supported only for protecting non-cluster hosts as of v3.1).

Policy-only mode: set `CALICO_NETWORKING_BACKEND=none` before starting the node container and Felix runs without BIRD and confd. You get policy without route distribution between hosts, as used on managed cloud providers.

With native v3 CRDs the Calico API server is not used; admission policies handle validation and defaulting.

## Checked

Read in full on 2026-11-08: the Component architecture page. The component list, Felix duties, policy-only mode variable, datastore comparison and native CRD remark match it.

Method: documentation only; no commands were run.
