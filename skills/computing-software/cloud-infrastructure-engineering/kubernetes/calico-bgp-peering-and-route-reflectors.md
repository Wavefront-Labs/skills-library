---
id: computing-software.cloud-infrastructure-engineering.kubernetes.calico-bgp-peering-and-route-reflectors
name: calico-bgp-peering-and-route-reflectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, calico, bgp, bgp-peering, route-reflector, cni, bare-metal, tor-switch]
level: advanced
status: docs-checked
description: "Peer Calico with top-of-rack routers and replace the node-to-node mesh with route reflectors: BGPConfiguration, BGPPeer selectors, cluster IDs, and safe cutover."
sources: ["https://docs.tigera.io/calico/latest/networking/configuring/bgp", "https://docs.tigera.io/calico/latest/reference/resources/bgppeer", "https://docs.tigera.io/calico/latest/reference/resources/bgpconfig", "https://docs.tigera.io/calico/latest/reference/resources/node", "https://docs.tigera.io/calico/latest/networking/configuring/advertise-service-ips"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calico BGP peering and route reflectors

## When
- Pod/Service IPs must be routable from outside the cluster (no overlay, no SNAT).
- The default full node-to-node iBGP mesh works well up to about 100 nodes; the docs recommend route reflectors beyond that.

## Inspect current state
```bash
calicoctl get bgpconfig default -o yaml
calicoctl node status            # run on a node: lists peers and Established/Idle state
calicoctl get bgppeers
```
The default AS for all nodes is 64512 (override globally in the default BGPConfiguration, or per node in the Node `bgp.asNumber`).

## Peer with ToR routers
Global peer (every node peers with the router):
```yaml
apiVersion: projectcalico.org/v3
kind: BGPPeer
metadata: {name: tor-a}
spec:
  peerIP: 10.0.0.1
  asNumber: 65001
```
Per-rack peer using node labels:
```yaml
spec:
  nodeSelector: rack == 'r1'
  peerIP: 10.1.0.1
  asNumber: 65001
```
Advertise Service IPs as well:
```yaml
apiVersion: projectcalico.org/v3
kind: BGPConfiguration
metadata: {name: default}
spec:
  asNumber: 64512
  serviceClusterIPs: [{cidr: 10.96.0.0/12}]
  serviceExternalIPs: [{cidr: 192.0.2.0/24}]
```

## Route reflectors inside the cluster
1. Provision new, unschedulable nodes to act as route reflectors (or drain existing nodes first):
   adding `routeReflectorClusterID` removes a node from the mesh immediately, tearing down its sessions
   and causing about 2 seconds of data plane disruption for workloads on that node.
```bash
kubectl label node rr1 rr2 route-reflector=true
calicoctl patch node rr1 -p '{"spec":{"bgp":{"routeReflectorClusterID":"244.0.0.1"}}}'
calicoctl patch node rr2 -p '{"spec":{"bgp":{"routeReflectorClusterID":"244.0.0.1"}}}'
```
2. Peer every node with the RRs, and RRs with each other:
```yaml
apiVersion: projectcalico.org/v3
kind: BGPPeer
metadata: {name: peer-with-rrs}
spec:
  nodeSelector: all()
  peerSelector: route-reflector == 'true'
```
3. Confirm sessions are `Established` on a normal node (`calicoctl node status` shows the RRs).
4. Only then disable the mesh:
```bash
calicoctl patch bgpconfig default -p '{"spec":{"nodeToNodeMeshEnabled":false}}'
```
Disabling the mesh breaks pod networking until replacement BGPPeer sessions are up, so wait for step 3. Mark the
reflector nodes schedulable again (`kubectl uncordon`) only if you made them unschedulable.

## Gotchas
- Give redundant route reflectors the same `routeReflectorClusterID` (the docs example uses `244.0.0.1`).
- Most public clouds support IPIP; Azure blocks IPIP traffic, so use VXLAN there (see the VXLAN/IPIP docs).
- `nodeToNodeMeshEnabled` and `serviceClusterIPs`/`serviceExternalIPs` are only valid on the global `default`
  BGPConfiguration. External IPs are advertised only if they fall inside a listed block.
- `calicoctl node status` (run on the node) shows BGP peering state; a `CalicoNodeStatus` resource gives the same
  information through the API.

## Verify
- [ ] `calicoctl node status` Established to every intended peer, on several nodes.
- [ ] ToR router shows pod CIDR blocks (/26 by default for IPv4) learned from nodes.
- [ ] Pod-to-pod across racks works after mesh disabled; external host reaches a pod IP.

## Checked

Documentation release: Calico docs (tigera/docs repo, calico/ docs, repo commit 2026-10-23; Calico release v3.33.0).
Confirmed in networking/configuring/bgp and the BGPPeer, BGPConfiguration and Node references: default AS 64512, full-mesh behaviour and the 100-node guidance, `nodeToNodeMeshEnabled`, `routeReflectorClusterID` (`244.0.0.1` example), `BGPPeer` with `peerIP`, `asNumber`, `nodeSelector`, `peerSelector`, the cutover order (peerings first, then disable mesh) and the 2 second disruption note, `calicoctl node status`, Service IP advertisement fields, default block size 26.
Removed because the docs do not state them: the TCP 179 firewall line, the AWS source/destination check advice, the operator read-only `kubectl get` claim, and the graceful-restart timer claim.

Method: documentation only; no commands were run.
