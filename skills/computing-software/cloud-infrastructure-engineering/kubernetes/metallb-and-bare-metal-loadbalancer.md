---
id: computing-software.cloud-infrastructure-engineering.kubernetes.metallb-and-bare-metal-loadbalancer
name: metallb-and-bare-metal-loadbalancer
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, metallb, loadbalancer, bare-metal, layer2-mode, bgp-mode, arp, vrrp, on-prem, service-type-loadbalancer]
level: advanced
status: docs-checked
description: "Give type:LoadBalancer Services a real external IP on bare metal with MetalLB: Layer2 (ARP/VRRP) mode vs BGP mode, and the failover and split-brain traps each has."
sources: ["https://metallb.io/concepts/layer2/", "https://metallb.io/concepts/bgp/", "https://metallb.io/configuration/", "https://metallb.io/configuration/_advanced_bgp_configuration/", "https://metallb.io/usage/", "https://metallb.io/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MetalLB — LoadBalancer Services without a cloud load balancer

**Goal:** make `type: LoadBalancer` work on bare metal/on-prem, and know which of MetalLB's
two modes fits the network you actually have.

## 1. The problem MetalLB solves
Cloud Kubernetes gets a real external IP for `type: LoadBalancer` because a cloud controller
provisions an actual LB resource. On bare metal there is no such controller — without
MetalLB (or an equivalent), `LoadBalancer` Services sit forever in `<pending>` for
`EXTERNAL-IP`. MetalLB fills that gap by announcing a Service's IP onto the local network
itself.

## 2. Layer2 mode — ARP/NDP, simplest, single-node-active
```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata: {name: default-pool, namespace: metallb-system}
spec: {addresses: ["192.168.1.240-192.168.1.250"]}
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata: {name: l2adv, namespace: metallb-system}
spec: {ipAddressPools: [default-pool]}
```
- One node is elected **leader** for each Service IP and answers ARP (IPv4) / NDP (IPv6) for
  it — all traffic for that IP arrives at that one node, and `kube-proxy` spreads it to the
  Service's pods.
- **Not real load balancing** — Layer2 mode sends all traffic for one IP through one node.
  High-throughput Services are bottlenecked by that single node's NIC; scale by spreading
  different Services across different pool IPs, not by expecting one IP to fan out across
  nodes.
- Failover: a failed leader is detected with memberlist and other nodes take over its IPs,
  sending gratuitous ARP/NDP packets. Most operating systems update their neighbour caches
  promptly, so failover typically takes a few seconds, but clients that ignore or mishandle
  gratuitous packets keep stale entries and the IP stays unreachable for them until their
  cache refreshes during an unplanned failover. The docs ask you to report failover slower
  than about 10 seconds. For planned moves, keep the old leader up for a couple of minutes.
- By default gratuitous packets are sent only on failover; `--gratuitous-arp-interval` (Helm
  `speaker.gratuitousARPInterval`, seconds, default 0) re-sends them periodically if switches
  age out forwarding entries between failovers.
- Layer 2 mode works on any Ethernet network with no special hardware.

## 3. BGP mode — real multi-node load balancing
```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata: {name: peer1, namespace: metallb-system}
spec: {myASN: 64512, peerASN: 64512, peerAddress: 192.168.1.1}
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata: {name: bgpadv, namespace: metallb-system}
spec: {ipAddressPools: [default-pool]}
```
- Every MetalLB speaker node runs a BGP session to the upstream router(s) and advertises
  Service IPs as routes — the upstream router does **ECMP** (equal-cost multi-path) across
  all advertising nodes, which is real multi-node load balancing, unlike Layer2 mode.
- Requires a BGP-capable upstream router/switch and someone with the authority to configure
  peering on it — the real blocker in most orgs is organizational (network team buy-in), not
  technical.
- BGP load balancing does not react gracefully to backend-set changes: when a node goes
  down, expect most active connections to that service to break (a one-time hit, not ongoing
  loss), because routers usually rehash connections when the next-hop set changes. A router
  option often called "resilient ECMP" greatly reduces the affected connections. Other
  mitigations in the docs: pin deployments to specific nodes, change deployments during
  low traffic, put an ingress controller in front, and add client retries.
- BGP is implemented by FRR-K8s by default; the plain FRR mode is deprecated.

## 4. Choosing
| Situation | Mode |
|---|---|
| No access to router BGP config, small/simple network | Layer2 |
| Need real multi-node throughput, router team can peer BGP | BGP |
| Mixed: some Services need HA more than throughput | Layer2 is fine; it still fails over, just not load-balances |

## 5. Common gotchas
- IP assignment problems: the `controller` assigns IPs and logs the reasons; check that an
  `IPAddressPool` compatible with the Service exists (including selectors, dual-stack and any
  requested specific IP) and that the pool still has free addresses. The `speaker`s announce
  IPs, so check them when a Service has an IP but is not reachable.
- Invalid configuration is marked stale and MetalLB keeps working with the last valid one;
  look for `failed to parse the configuration` in the logs or the
  `metallb_k8s_client_config_stale_bool` metric.
- `externalTrafficPolicy: Local` in Layer2 mode: kube-proxy on the leader sends traffic only to
  local pods, so pods not on the current leader node receive no traffic (they are only failover
  replicas). In BGP mode only nodes running a local pod attract traffic.

## Debug routine
```bash
kubectl -n metallb-system get pods -o wide
kubectl -n metallb-system logs <speaker-pod> --tail=100      # and the controller pod for IP assignment issues
kubectl get svc myapp -o jsonpath='{.status.loadBalancer.ingress}'
arping -I eth0 192.168.1.240   # confirm which MAC answers, from a client on the same segment
# BGP mode
kubectl -n metallb-system exec <speaker-pod> -c frr -- vtysh -c 'show bgp neigh <neigh-ip>'   # Established = healthy session; FRR-based modes
```

## Verify
- [ ] `kubectl get svc` shows a real `EXTERNAL-IP`, not `<pending>`.
- [ ] Layer2 mode: killing the current leader node triggers failover and the window of
  unreachability is measured, not assumed instant.
- [ ] BGP mode: `show ip bgp` on the upstream router actually lists the Service route with
  multiple next-hops (confirms ECMP, not just one advertising node).
- [ ] `Pending` Services are diagnosed from the controller logs (pool selection or exhaustion), not
  mistaken for a broken deployment.

## Checked
2026-10-26. Checked against the MetalLB website source (repository metallb/metallb, last push 2026-10-22). Confirmed: CRD versions `metallb.io/v1beta1` IPAddressPool, L2Advertisement and BGPAdvertisement and `metallb.io/v1beta2` BGPPeer (v1beta1 BGPPeer is deprecated), all in the MetalLB namespace; layer 2 mode sends all traffic for a service IP to one leader node and kube-proxy spreads it to pods; failover is detected with memberlist and clients receive gratuitous ARP/NDP, usually updating within a few seconds, with slower failover (more than about 10s) worth a bug report; BGP mode balances per connection by packet hash and a change in the node set breaks most active connections unless the router supports resilient ECMP; FRR-K8s is the default BGP backend and the older FRR mode is deprecated; `vtysh show bgp neigh` is the documented session check; `externalTrafficPolicy` Local semantics for both modes. Corrected: the BGP failover claim, the BIRD debug command and the eBPF final-hop claim. Removed as unconfirmed: the pool-exhaustion command, the speaker pod label selector, the version-specific leader-election claim and the same-segment routing claim.
Method: documentation only; no commands were run.
