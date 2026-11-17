---
id: computing-software.cloud-infrastructure-engineering.azure.azure-mtu-fragmentation-and-tcp-mss-clamping
name: azure-mtu-fragmentation-and-tcp-mss-clamping
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, network-troubleshooting, mtu, mss-clamping, fragmentation, vpn-gateway, jumbo-frames]
level: advanced
status: docs-checked
description: "Diagnose MTU and fragmentation issues in Azure VNets, VPN and ExpressRoute paths, set MSS clamping on tunnels, and test path MTU correctly."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-network-tcpip-performance-tuning", "https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpn-devices", "https://learn.microsoft.com/azure/virtual-network/how-to-virtual-machine-mtu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MTU, fragmentation and MSS clamping in Azure

**Goal:** fix "small requests work, big ones hang" symptoms caused by packet size.

## Facts
- Default MTU for Azure VMs is **1500** bytes. Larger values are possible on some adapters (per-adapter values are on the VM MTU how-to page); keep 1500 unless measured.
- Azure drops fragmented packets that arrive at the VM out of order, so avoid fragmentation instead of relying on it.
- IPsec on VPN gateways adds overhead, so clamp TCP MSS on the on-premises tunnel device; derive the value from the measured path MTU (MSS = MTU - 40 for IPv4 TCP).

## Diagnose
```bash
# Linux: largest payload that passes without fragmentation (1472 + 28 = 1500)
ping -M do -s 1472 10.1.0.4
tracepath 10.1.0.4               # discovers path MTU
```
```powershell
ping -f -l 1472 10.1.0.4        # Windows: don't-fragment + size
```
(ICMP may be blocked; use the TCP test of a large HTTP response with `curl -v` as confirmation.)

Packet capture (Network Watcher or tcpdump) showing repeated retransmits of full-size segments and no ICMP "fragmentation needed" = PMTUD black hole.

## Fix
- On-prem firewall tunnel interface: clamp TCP MSS to the value derived from the measured path MTU, using your vendor's MSS-adjust setting.
- NVAs in Azure that terminate tunnels: clamp MSS there too.
- Guest OS: do not lower MTU fleet-wide as a first fix; fix at the tunnel.
- For larger MTU inside a VNet, set the same MTU on both VMs and verify with `ping -M do -s <mtu-28>`.

## Verify
- [ ] Large transfer (for example `curl -o /dev/null https://host/100MB`) completes across the tunnel.
- [ ] `ping -M do -s <mtu-28>` succeeds end to end at the MTU you chose.

## Checked
2026-10-28. Confirmed on the VM MTU how-to and TCP/IP performance tuning pages: default MTU 1500, per-adapter MTU settings differ, fragmented packets arriving out of order are dropped.
Removed (not confirmed in the fetched pages): the ~4000 MTU figure, the 1350 MSS / 1400 tunnel MTU values, vendor MSS syntax, the claim that the VPN gateway clamps MSS, and the `netsh` line.

Method: documentation only; no commands were run.
