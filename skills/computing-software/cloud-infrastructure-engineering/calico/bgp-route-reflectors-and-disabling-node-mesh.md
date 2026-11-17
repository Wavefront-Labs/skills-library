---
id: computing-software.cloud-infrastructure-engineering.calico.bgp-route-reflectors-and-disabling-node-mesh
name: bgp-route-reflectors-and-disabling-node-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [bgp, route-reflector, node-to-node-mesh, bgpconfiguration, cluster-id, peerselector, migration]
level: advanced
status: docs-checked
description: "Move from the full BGP mesh to route reflectors with minimal disruption: set routeReflectorClusterID, peer by label, verify sessions, then set nodeToNodeMeshEnabled false."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/bgp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Route reflectors cut the number of peerings per node for large clusters: some nodes mesh with each other and the rest peer with a subset of them (typically 2).

**Make a node a reflector** by giving it a cluster ID, typically an unused IPv4 address:

```bash
kubectl annotate node my-node projectcalico.org/RouteReflectorClusterID=244.0.0.1
calicoctl patch node my-node -p '{"spec": {"bgp": {"routeReflectorClusterID": "244.0.0.1"}}}'
```

(Either form.) Label it, then peer by label:

```bash
kubectl label node my-node route-reflector=true
```

```yaml
kind: BGPPeer
apiVersion: projectcalico.org/v3
metadata:
  name: peer-with-route-reflectors
spec:
  nodeSelector: all()
  peerSelector: route-reflector == 'true'
```

**Disruption.** Adding `routeReflectorClusterID` removes that node from the mesh immediately and tears down its sessions; new sessions follow. Expect about 2 seconds of data plane disruption for workloads on that node unless it hosts none (new node, or drained).

**Disable the mesh:**

```bash
calicoctl patch bgpconfiguration default -p '{"spec": {"nodeToNodeMeshEnabled": false}}'
```

This breaks pod networking until replacement BGPPeers exist, so create them first. Create the default BGPConfiguration if missing.

**Zero-disruption migration:**

1. Provision new, unschedulable nodes with the cluster ID and a `route-reflector` label.
2. Create the BGPPeer above.
3. Wait for sessions (`calicoctl node status`, or a CalicoNodeStatus resource).
4. Disable the node-to-node mesh.
5. Uncordon any drained or unschedulable nodes.

## Checked

2026-11-08. The Configure BGP peering page was read in full. Annotation and patch commands, YAML, the 2 second note and the migration steps were confirmed. Removed the unsupported claim that reflectors carry no endpoint data.

Method: documentation only; no commands were run.
