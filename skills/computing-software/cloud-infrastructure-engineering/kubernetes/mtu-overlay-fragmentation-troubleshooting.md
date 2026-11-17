---
id: computing-software.cloud-infrastructure-engineering.kubernetes.mtu-overlay-fragmentation-troubleshooting
name: mtu-overlay-fragmentation-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, mtu, vxlan, ipip, overlay, fragmentation, pmtud, path-mtu, jumbo-frames, tcpdump, mss-clamping, networking]
level: advanced
status: docs-checked
description: "Diagnose the 'small requests work, large payloads hang' overlay-MTU bug: VXLAN/IPIP encapsulation overhead, Path MTU Discovery black holes, and MSS clamping."
sources: ["https://docs.tigera.io/calico/latest/networking/configuring/mtu", "https://github.com/flannel-io/flannel/blob/master/Documentation/backends.md", "https://github.com/cilium/cilium/blob/main/install/kubernetes/cilium/values.yaml", "https://www.rfc-editor.org/rfc/rfc1191", "https://man7.org/linux/man-pages/man8/iptables-extensions.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MTU, overlay encapsulation, and the fragmentation bug that only shows up under load

**Goal:** recognize and fix the specific failure signature where small requests (DNS, health
checks, short API calls) work fine but larger payloads (big JSON bodies, TLS handshakes with
large certs, file uploads) hang or reset: almost always an MTU mismatch across an overlay.

## 1. Why overlays break MTU assumptions
- Encapsulation adds a header to every packet. Per Calico's MTU guide the overhead is 20
  bytes for IP-in-IP, 50 bytes for IPv4 VXLAN, 70 for IPv6 VXLAN, 60 for IPv4 WireGuard and
  80 for IPv6 WireGuard (IPv4 VXLAN: 14 Ethernet + 20 IP + 8 UDP + 8 VXLAN = 50). If the
  pod-facing interface's MTU is left equal to the underlay MTU (1500 on both), a full-size
  packet no longer fits once encapsulated. It is then either fragmented or, if the
  "don't fragment" bit is set (normal for TCP using Path MTU Discovery), dropped.
- CNIs normally detect the MTU for you: Calico auto-detects it from the node configuration
  and the enabled encapsulations; Flannel uses the external interface MTU unless a backend
  `MTU` is set; Cilium auto-detects it unless the Helm `MTU` value (agent `--mtu`) overrides
  it. Detection can still be wrong or stale after an image change or a move to a different
  network (Calico's table lists 9001 for AWS jumbo frames and 1460 for GCE, and it notes
  that AKS's underlying network MTU is 1400 even though the interface shows 1500), or when
  an old manual override remains.
  Calico notes that disabling unused encapsulations in the Felix configuration lets
  auto-detection choose the best value.

## 2. The classic symptom
- `curl` with a small response: works.
- `curl` with a response/request body that pushes a TCP segment near or above the effective
  MTU: hangs, then times out. It is **not** an immediate error, because the client's SYN/ACK
  and early handshake packets are small and succeed; only the large-payload packets are lost.
- This is a **Path MTU Discovery black hole** (RFC 1191): the device that would send an
  ICMP "Fragmentation Needed" message back to the sender is missing or ICMP is blocked, so
  the sender never learns to shrink its segments and keeps retransmitting the same
  oversized packet.

## 3. Fixes, in order of how surgical they are
1. **Correct the CNI's MTU setting.** Compare what the CNI programmed
   (`ip link show <iface>` on the node or in a pod's network namespace) with the
   physical MTU minus overhead. Set it explicitly: Calico operator
   `spec.calicoNetwork.mtu` (or `veth_mtu` in the `calico-config` ConfigMap for manifest
   installs, followed by a rolling restart of `calico-node`), Flannel backend `MTU`,
   Cilium Helm `MTU`. Calico's guide says a new MTU applies only to new workloads, and
   recommends the physical MTU minus 60 (IPv4 WireGuard anywhere), minus 80 (IPv6
   WireGuard), minus 50 (IPv4 VXLAN), minus 70 (IPv6 VXLAN) or minus 20 (IP-in-IP only),
   using the smallest value if you mix encapsulations.
2. **MSS clamping** as a stopgap: an iptables `TCPMSS` rule with `--clamp-mss-to-pmtu` on
   the gateway/node, which the iptables manual describes as clamping the MSS to the path MTU
   minus 40 for IPv4. It fixes TCP only; UDP paths (for example DNS with a large response)
   are not helped.
3. **Enable jumbo frames end-to-end** if every hop supports them; one hop that does not
   brings the same bug back at a larger size.

## 4. Confirming with a packet capture, not guessing
```bash
# On a node, capture encapsulated traffic and look for fragmentation or ICMP errors
tcpdump -i eth0 -n 'icmp[icmptype] == icmp-unreach and icmp[icmpcode] == 4'   # Frag Needed
tcpdump -i eth0 -n 'ip[6:2] & 0x2000 != 0 or ip[6:2] & 0x1fff != 0'           # fragmented IP
# Probe the effective MTU with the don't-fragment bit set
ping -M do -s 1472 <peer-ip>   # 1472 + 28 = 1500; raise/lower -s to binary-search the real ceiling
```
- `ping -M do` prohibits fragmentation, so stepping `-s` up and down finds the largest
  size that gets a reply even if ICMP errors are blocked; the packet fails locally when `-s`
  exceeds the local interface MTU, and simply gets no reply when the limit is further along
  the path.
- Cilium exposes counters for this: `mtu_error_message_total` counts ICMP
  `fragmentation_needed` / ICMPv6 `packet_too_big` messages its datapath processed, and
  fragment tracking is on by default (see Cilium's fragment handling page).

## Verify
- [ ] The overlay interface's configured MTU is checked against physical MTU minus the
  specific encapsulation overhead in use, after any infra change.
- [ ] A large-payload request (well above the suspected MTU boundary) is tested directly, not
  inferred from small-request success.
- [ ] If MSS clamping is used as a fix, UDP-based paths (DNS, QUIC/HTTP3 if in use) are
  separately verified, since clamping does not help them.
- [ ] Packet capture or the `ping -M do` search confirms the actual usable size,
  rather than trusting a single config value.

## Checked
2026-10-27. Documentation releases: Calico 3.33 MTU guide, Flannel v0.28.10 backends doc, Cilium v1.20.4 Helm values, agent flags and fragmentation page, iptables-extensions man page, iputils ping docs.
Confirmed: Calico overhead values and recommendations and per-platform MTU table, auto-detection behaviour, the three CNIs' explicit MTU settings, `--clamp-mss-to-pmtu` semantics, `ping -M` option, Cilium MTU-error metric.
Method: documentation only; no commands were run.
