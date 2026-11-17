---
id: computing-software.digital-privacy-hygiene.vpn-tools.tunnelvision-dhcp-route-attack
name: tunnelvision-dhcp-route-attack
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, tunnelvision, vpn-limitations, vpn-leak-test]
level: practitioner
status: docs-checked
description: "Understand the TunnelVision DHCP option 121 attack (CVE-2024-3661) that routes traffic outside a VPN, which platforms are affected, and the mitigations."
sources:
  - "https://www.leviathansecurity.com/blog/tunnelvision"
  - "https://nvd.nist.gov/vuln/detail/CVE-2024-3661"
  - "https://mullvad.net/en/blog/evaluating-the-impact-of-tunnelvision"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TunnelVision DHCP route attack

**Goal:** know when a malicious local network can silently pull your traffic out of the VPN tunnel.

## The attack (CVE-2024-3661)
An attacker on the same LAN becomes the DHCP server (by starving the real one, racing DHCPDISCOVER replies, or ARP-spoofing a lease renewal; short leases force renewals). It pushes DHCP option 121 classless static routes (RFC 3442) more specific than the VPN's default route. The DHCP server cannot name an interface, so the client applies them to the interface it got the lease on: traffic leaves unencrypted via the physical interface. The VPN control channel stays intact, so the client keeps showing connected and the kill switch never engages. It is independent of VPN protocol (WireGuard, OpenVPN, IPsec) and encryption strength.

## Who is affected
- Leviathan's tests: Windows, Linux, iOS and macOS affected; any OS with an RFC-compliant DHCP client supporting option 121 is considered affected.
- Android is not affected: it does not implement option 121.
- VPNs relying only on routing rules are vulnerable; self-hosted VPNs without hardened clients are likely vulnerable.
- Mullvad (its own app): desktop firewall rules block traffic to public IPs outside the tunnel, preventing plaintext exposure; iOS was still vulnerable at the time of its post, with a fix not yet shipped.

## Mitigations (Leviathan)
1. Firewall rules blocking inbound and outbound on the physical interface except DHCP and VPN server IPs (causes selective denial of service and a possible traffic-analysis side channel).
2. Ignore option 121 while the VPN is active (must be mandatory; can break legitimate connectivity).
3. Phone hotspot, or a VM with a non-bridged adapter, to keep attackers off the local network.
4. Linux network namespaces: called the strongest fix; unclear for Windows and macOS.
5. Avoid untrusted networks when confidentiality is critical. On networks you run, use DHCP snooping and ARP protections.

## Gotchas
- Leviathan describes no endpoint method for detecting an active attack. Looking at the routing table for unexpected specific routes is a reasonable manual check but is not from the sources.

## Checked
Method: 2026-11-08 read the Leviathan and Mullvad pages in full. The NVD page returned only a generic header via fetch, so the CVE id rests on the other two pages. Removed unsupported claims: "detect via ip route/route print" as a documented method, the NetworkManager tip, and "vendors shipped mitigations after disclosure" as stated fact. The HTTPS-still-protects-content note was also removed.
