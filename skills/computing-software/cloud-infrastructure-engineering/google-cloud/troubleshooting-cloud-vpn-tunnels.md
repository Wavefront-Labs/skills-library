---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-cloud-vpn-tunnels
name: troubleshooting-cloud-vpn-tunnels
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hybrid-connectivity, vpn-troubleshooting, ike-troubleshooting, cloud-vpn-logs, bgp]
level: advanced
status: docs-checked
description: "Fix Cloud VPN tunnels that won't establish or pass traffic: tunnel status messages, Cloud VPN logs for IKE errors, proposal and PSK mismatches, BGP down, MTU and asymmetric routing."
sources: ["https://cloud.google.com/network-connectivity/docs/vpn/support/troubleshooting", "https://cloud.google.com/network-connectivity/docs/vpn/how-to/viewing-logs-metrics", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations", "https://www.googleapis.com/discovery/v1/apis/compute/v1/rest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Cloud VPN tunnels

## 1. Status first
```bash
gcloud compute vpn-tunnels describe tun-0 --region=REGION --format='value(status,detailedStatus)'
gcloud compute routers get-status havpn-router --region=REGION --format=json
```
| status | Usually |
|---|---|
| `NO_INCOMING_PACKETS` | no incoming packets from the peer |
| `WAITING_FOR_FULL_CONFIG` | Google Cloud is waiting for the rest of the VPN configuration (for Classic VPN: network, gateway, tunnel, forwarding rules, route) |
| `NEGOTIATION_FAILURE` | handshake failed |
| `AUTHORIZATION_ERROR` | auth error, for example a bad shared secret |
| `PEER_IDENTITY_MISMATCH` | peer identity does not match the peer IP, probably behind NAT |
| `TS_NARROWING_NOT_ALLOWED` | traffic selector narrowing not allowed |
| `FIRST_HANDSHAKE` | first handshake with the peer succeeded |
| `ESTABLISHED` but no traffic | check routing, firewall rules, BGP |

## 2. Logs
```
resource.type="vpn_gateway" "establishing IKE_SA failed, peer not responding"
```
The troubleshooting page lists ready-made searches on `resource.type="vpn_gateway"` for IKE_SA initiation, IKE_AUTH events, successful pre-shared key authentication, CHILD_SA events and rekeys, and `Remote traffic selectors narrowed` / `Local traffic selectors narrowed` when selectors do not match.

## 3. Established but broken
- **BGP down**: check the link-local IPs and masks on both sides, the ASNs, and the Cloud Router BGP session status (`routers get-status`).
- **Routes learned but no traffic**: VPC firewall rules don't allow the on-premises ranges, or on-premises lacks a return route.
- **Large packets fail** (SSH works, HTTPS hangs): MTU. The Cloud VPN gateway MTU is 1460 bytes and the payload MTU is lower after IPsec overhead; Cloud VPN does not fragment packets after encapsulation (see the MTU considerations page).
- **Asymmetric routing** with two tunnels and stateful on-prem firewalls: use active/passive by giving the tunnels unequal route priorities.

## 4. Tools
- Connectivity Tests from a VM to an on-prem IP shows which route/tunnel is chosen.
- `tcpdump -ni any host <onprem-ip>` on a VM confirms packets leave and replies come back.

## Verify
- [ ] Tunnel ESTABLISHED, BGP UP with the expected prefix counts, and traffic passes both ways.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: WAITING_FOR_FULL_CONFIG was described as the peer not sending; the Compute API VpnTunnel.status enum says Google Cloud is waiting for the full configuration. FIRST_HANDSHAKE means a successful first handshake, not 'stuck'. The viewing-logs URL in sources returned 404 and was replaced with the logs and metrics page linked from the troubleshooting guide.
- Confirmed (Compute API discovery document, VpnTunnel.status): NO_INCOMING_PACKETS, NEGOTIATION_FAILURE, AUTHORIZATION_ERROR, PEER_IDENTITY_MISMATCH, TS_NARROWING_NOT_ALLOWED and the other values in the table.
- Confirmed (troubleshooting page): resource.type="vpn_gateway" log searches including the peer not responding and traffic selector narrowed messages. Confirmed (MTU page): gateway MTU 1460, no fragmentation after encapsulation.
- Removed: the NO_PROPOSAL_CHOSEN, AUTHENTICATION_FAILED and TS_UNACCEPTABLE strings, the gateway_id label, the eBGP multihop and MD5 advice, the MSS 1360 value and the ping size (not found in the pages read).

Method: documentation only; no commands were run.
