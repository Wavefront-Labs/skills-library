---
id: computing-software.cloud-infrastructure-engineering.kubespray.calico-bgp-peering-and-route-reflectors
name: calico-bgp-peering-and-route-reflectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [calico, bgp, route-reflector, calico-rr, peers, as-number]
level: sme
status: docs-checked
description: "Peer Calico with border routers via Kubespray, define peers, advertise service IPs, set global_as_num and use calico_rr route reflectors."
sources:
  - https://kubespray.io/docs/CNI/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Border router peering.** To route pod subnets without NAT, set `peer_with_router: true` (default false) and optionally `nat_outgoing: false` (default true), and add a `local_as` host variable per node:

```ShellSession
node1 ansible_ssh_host=95.54.0.12 local_as=xxxxxx
```

**Peers.** Define them with the `peers` variable. Global peers go in group_vars with `scope` set to `global`; per-node peers go in hostvars or group_vars with `scope` unset or `node`. Ansible's `hash_behaviour` defaults to `replace`, so defining both global and node peers leaves only node peers; to keep both, define the global peers in hostvars for each host as well. Node-scope peers accept `filters`, `sourceAddress` and `numAllowedLocalASNumbers`.

**Advertising services** in `k8s_cluster/k8s-net-calico.yml`: `calico_advertise_cluster_ips: true` (Calico 3.4+), and from 3.10 `calico_advertise_service_external_ips` as a list of CIDRs.

`global_as_num` defaults to `64512`.

**Route reflectors.** At scale, disable the full node-to-node mesh. Add a `calico_rr` group (it can overlap `kube_node` and `kube_control_plane`) and a `cluster_id` per reflector group. The page's inventory puts `rr0` and `rr1` in `calico_rr`, all hosts in `[rack0]`, with:

```ini
[rack0:vars]
cluster_id="1.0.0.1"
calico_rr_id=rr1
calico_group_id=rr1
```

## Checked

2026-11-08. Cited pages re-read in full. All variables and the rack0 inventory excerpt were confirmed on the Calico page BGP sections.

Method: documentation only; no commands were run.
