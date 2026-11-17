---
id: computing-software.cybersecurity-defensive.network-defence.proxy-bypass-detection
name: proxy-bypass-detection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [proxy-bypass-detection, doh-blocking, vpn-detection, tor-detection, egress-control, web-filtering, anonymizer]
level: practitioner
status: draft
description: "Detect and block web proxy bypass: direct egress, DoH/DoT, personal VPNs, Tor, anonymiser proxies and tunnelling, with firewall App-ID, DNS canary domains and SIEM queries."
sources: ["https://support.mozilla.org/en-US/kb/canary-domain-use-application-dnsnet", "https://www.cisa.gov/sites/default/files/publications/CISA_Encrypted_DNS_Implementation_Guidance.pdf", "https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/app-id"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proxy bypass detection

## Bypass routes and controls
| Route | Prevent | Detect |
|---|---|---|
| Direct 80/443 egress | Firewall default-deny outbound except from proxy | Firewall allow/deny logs from client subnets to internet |
| DNS over HTTPS / DoT | Block TCP/UDP 853; block known DoH resolver IPs/hostnames (category or list); Firefox canary `use-application-dns.net` NXDOMAIN; browser policies `DnsOverHttpsMode=off` | TLS to known DoH endpoints, DNS query volume dropping for a host |
| Personal/commercial VPN | App-ID (openvpn, wireguard, ipsec, nordvpn etc.), block UDP 1194/51820 and IKE to the internet | Long-lived UDP flows to residential/VPN provider ASNs |
| Tor | Block Tor App-ID and relay list EDL | Connections to Tor relays (consensus list as feed) |
| Web anonymisers | URL category "proxy avoidance and anonymizers" blocked | Hits on that category |
| Tunnelling over DNS/ICMP/SSH | DNS only via internal resolvers; ICMP out restricted; SSH egress blocked | See protocol anomaly detection |
| Mobile hotspots | Endpoint policy (Wi-Fi restrictions on managed devices), SWG agent with always-on | Device on unknown network without SWG agent telemetry |

## Endpoint-based enforcement
Cloud SWG agents (Zscaler Client Connector, Netskope, Defender for Endpoint network protection) enforce off
network too; detect agent disabled/tampered events.

## SIEM queries (examples)
- Firewall: allowed sessions to dst port 443 where src is a workstation subnet and the proxy is not the source.
- Proxy logs vs DHCP: hosts active on the network with zero proxy traffic for a day.

## Gotchas
- Some legitimate apps embed DoH (or QUIC); block QUIC (UDP 443) if the proxy cannot inspect it - browsers fall back to TCP.
- Blocking all VPN protocols breaks partner VPN access; allow by destination.

## Verify
- [ ] Test DoH in a browser (policy-controlled) fails or is detected.
- [ ] Direct egress attempts generate firewall denies and an alert for repeated attempts.
