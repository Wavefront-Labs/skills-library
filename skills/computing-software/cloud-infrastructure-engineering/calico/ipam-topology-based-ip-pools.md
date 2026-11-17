---
id: computing-software.cloud-infrastructure-engineering.calico.ipam-topology-based-ip-pools
name: ipam-topology-based-ip-pools
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipam, topology, nodeselector, ip-pools, rack, zone, labels, route-aggregation]
level: practitioner
status: docs-checked
description: "Allocate pod IPs by rack, zone or region: label nodes, give each IPPool a nodeSelector, and ensure every node is selected by some pool."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/assign-ip-addresses-topology
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Giving workloads in one region, zone or rack addresses from the same pool reduces the number of routes needed in the network. Annotations cannot do this because they apply only per namespace or pod; Calico instead uses **node-selection IPAM**: node labels plus pool node selectors decide which pools a node allocates from.

**Best practice.** Nodes only assign workload addresses from pools that select them. Make sure every node is selected by at least one pool, or a workload with no address will fail to start.

Basic form, a pool for nodes labelled `zone=west`:

```yaml
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: zone-west-ippool
spec:
  cidr: 192.168.0.0/24
  ipipMode: Always
  natOutgoing: true
  nodeSelector: zone == "west"
```

```bash
kubectl label nodes kube-node-0 zone=west
```

**Rack tutorial** (four nodes over two racks, pod range 192.168.0.0/16, `/24` per rack):

1. Delete the default pool, because it already covers the whole /16: `calicoctl delete ippools default-ipv4-ippool`.
2. Label nodes, for example `kubectl label nodes kube-node-0 rack=0`, and `rack=1` for the second rack.
3. Create one IPPool per rack with a matching `nodeSelector`, using `192.168.0.0/24` for rack 0 and `192.168.1.0/24` for rack 1.

Check with `calicoctl get ippool -o wide`, which shows a SELECTOR column (the default pool shows `all()`).

## Checked

Read in full on 2026-11-08: the Assign IP addresses based on topology page. The node-selection concept, best practice, zone example and the rack tutorial steps and commands match it. Rack pool YAML is described rather than reproduced.

Method: documentation only; no commands were run.
