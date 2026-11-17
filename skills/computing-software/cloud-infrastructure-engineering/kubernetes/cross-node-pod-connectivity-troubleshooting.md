---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cross-node-pod-connectivity-troubleshooting
name: cross-node-pod-connectivity-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cross-node-connectivity, node-firewall-ports, cni, vxlan, troubleshooting, cka, networking]
level: advanced
status: docs-checked
description: "Pods talk on the same node but not across nodes: isolate overlay vs routing, check CNI firewall ports, cloud source/dest checks, routes, rp_filter and MTU with tcpdump."
sources: ["https://kubernetes.io/docs/reference/networking/ports-and-protocols/", "https://docs.cilium.io/en/stable/operations/system_requirements/#firewall-rules", "https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements", "https://github.com/flannel-io/flannel/blob/master/Documentation/backends.md", "https://docs.aws.amazon.com/vpc/latest/userguide/work-with-nat-instances.html", "https://docs.kernel.org/networking/ip-sysctl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-node pod-to-pod connectivity

## Confirm the shape of the failure
```bash
kubectl get pod -o wide -A | grep -E 'netshoot|target'      # note node + pod IPs
kubectl run a --image=nicolaka/netshoot --overrides='{"spec":{"nodeName":"node1"}}' -- sleep 1d
kubectl run b --image=nicolaka/netshoot --overrides='{"spec":{"nodeName":"node2"}}' -- sleep 1d
kubectl exec a -- ping -c3 <b-pod-ip>          # cross-node
kubectl exec a -- ping -c3 <pod-ip-on-node1>   # same-node control
```
Same-node OK + cross-node fails = encapsulation/routing between nodes, not DNS, not policy
(unless policy differs). Test pod IP directly, never Service names, at this stage.

## Encapsulation ports that must be open node-to-node
| CNI / mode | Port |
|---|---|
| Flannel VXLAN (Linux default), Cilium VXLAN | UDP 8472 |
| Calico VXLAN | UDP 4789 |
| Calico IPIP | IP protocol 4 (not a port: security groups need a "protocol 4" rule) |
| Calico BGP | TCP 179 |
| Calico Typha (if enabled, on the Typha hosts) | TCP 5473 (default) |
| Cilium Geneve | UDP 6081 |
| WireGuard: Calico 51820 (IPv4) / 51821 (IPv6); Flannel 51820 (v6 51821); Cilium 51871 | UDP |
| Cilium health | TCP 4240, plus ICMP echo (type 8, code 0) between nodes |
Flannel's backend `Port` option can change the VXLAN port, so confirm the value actually
configured. Typical misses: cloud security group only allows TCP; on-prem firewalld/ufw on
hosts (Calico's requirements page says to disable firewalld or other iptables managers
that can interfere); IPIP blocked because the rule was written as TCP/UDP.

## Watch the packets
```bash
# on node1 (or kubectl debug node/node1 -it --image=nicolaka/netshoot; the node root is mounted at /host)
tcpdump -ni any 'udp port 8472 or proto 4'      # does encapsulated traffic leave? (use the port your CNI uses)
# on node2: does it arrive? If it leaves node1 but never reaches node2: network/firewall/cloud.
```

## Native routing (no overlay) checks
- `ip route` on each node: a route for every other node's pod CIDR (via BGP or the CNI).
- AWS: every EC2 instance performs a **source/destination check** by default, so it must be
  the source or destination of the traffic it sends or receives; a node that forwards
  traffic for pod IPs that are not its own needs the check disabled (AWS documents the
  same requirement for NAT instances). Other clouds: configure routes for the pod CIDRs as
  the provider's CNI documentation describes.
- `sysctl net.ipv4.ip_forward` = 1. For asymmetric paths, `rp_filter` should be 0 (off) or
  2 (loose); the kernel uses the **maximum** of `conf/all/rp_filter` and the per-interface
  value, so check the interface value too, not just `all`.

## Other causes
- **MTU**: ping works, TCP stalls on large payloads. `ping -M do -s 1422 <ip>` to find the
  limit; per Calico's MTU guide the overlay MTU is the underlay MTU minus 50 (IPv4 VXLAN),
  70 (IPv6 VXLAN) or 20 (IPIP). See the MTU troubleshooting skill.
- **Different node subnets** with a CrossSubnet mode (Calico `VXLANCrossSubnet` or
  `IPIPCrossSubnet`): encapsulation happens only between subnets.
- **Node IP chosen wrong** (multi-NIC): check `INTERNAL-IP` in `kubectl get node -o wide`;
  set kubelet `--node-ip` and the CNI's autodetection (`IP_AUTODETECTION_METHOD` for Calico).

## Verify
- [ ] Ping and `curl <pod-ip>:<port>` work in both directions between every node pair (a
  DaemonSet-based checker such as Bloomberg's goldpinger, which makes calls between its
  instances on every node, exposes this continuously).

## Checked
2026-10-27. Documentation releases: Cilium v1.20.4, Calico 3.33, Flannel v0.28.10, Kubernetes website main (v1.38 dev tree; latest release v1.37.1), Linux kernel ip-sysctl docs.
Confirmed: Cilium ports (8472, 6081, 4240, ICMP 8/0, 51871), Calico ports (179, protocol 4, 4789, 5473, 51820/51821), Flannel default VXLAN 8472 and WireGuard ports, Calico MTU overheads (20/50/70), AWS source/destination check behaviour, rp_filter semantics.
Method: documentation only; no commands were run.
