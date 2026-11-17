---
id: computing-software.cloud-infrastructure-engineering.calico.bgp-peers-global-per-node-and-as-numbers
name: bgp-peers-global-per-node-and-as-numbers
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [bgp, bgppeer, peering, asnumber, localasnumber, top-of-rack, nodeselector, calicoctl]
level: practitioner
status: docs-checked
description: "Configure Calico BGP peers: global versus per-node BGPPeer with nodeSelector, default and per-node AS numbers, localASNumber per peer, and calicoctl node status."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/bgp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico nodes exchange routes over BGP. Default topology is a full iBGP node-to-node mesh (fine for roughly 100 nodes or fewer). On premises you often peer with the physical top-of-rack routers instead. Significant topology changes can briefly drop pod connectivity, so schedule them. calicoctl must be installed.

**Global peer** (every node peers with it):

```yaml
apiVersion: projectcalico.org/v3
kind: BGPPeer
metadata:
  name: my-global-peer
spec:
  peerIP: 192.20.30.40
  asNumber: 64567
```

**Per-node peer**: select nodes by exact name or label, for example a rack:

```yaml
apiVersion: projectcalico.org/v3
kind: BGPPeer
metadata:
  name: rack1-tor
spec:
  peerIP: 192.20.30.40
  asNumber: 64567
  nodeSelector: rack == 'rack-1'
```

**AS numbers.** Nodes default to AS 64512.

```bash
calicoctl patch bgpconfiguration default -p '{"spec": {"asNumber": "64513"}}'
calicoctl patch node node-1 -p '{"spec": {"bgp": {"asNumber": "64514"}}}'
kubectl patch bgppeer [peer_name] -p '{"spec": {"localASNumber": 64577}}'
```

Those set the global default, one node's AS, and a local AS for a single peer (overriding the node and global values). If the default BGPConfiguration does not exist, create it first.

**Status.** Create a `CalicoNodeStatus` resource, or run `calicoctl node status` on the node itself (it talks to the local agent).

Azure blocks IP-in-IP, so use VXLAN there.

## Checked

2026-11-04. YAML, commands, defaults and the topology notes were confirmed on the Configure BGP peering page.

Method: documentation only; no commands were run.
