---
id: computing-software.cloud-infrastructure-engineering.aws.site-to-site-vpn-troubleshooting-with-tunnel-logs
name: site-to-site-vpn-troubleshooting-with-tunnel-logs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, site-to-site-vpn, vpn-tunnel-logs, tunnel-down, ike-negotiation, bgp-troubleshooting, tunnelstate]
level: advanced
status: docs-checked
description: "Diagnose a Site-to-Site VPN tunnel that is down or flapping: tunnel logs, IKE/IPsec error meanings, BGP status, routing and traffic checks, and monitoring alarms."
sources: ["https://docs.aws.amazon.com/vpn/latest/s2svpn/monitoring-logs.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/Troubleshooting.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/monitoring-cloudwatch-vpn.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/vpn-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site-to-Site VPN troubleshooting

## 1. Status first
```bash
aws ec2 describe-vpn-connections --vpn-connection-ids vpn-0abc \
  --query 'VpnConnections[0].VgwTelemetry[].{ip:OutsideIpAddress,status:Status,msg:StatusMessage,changed:LastStatusChange,routes:AcceptedRouteCount}'
```
`IPSEC IS UP` with 0 accepted routes suggests IPsec is fine but BGP is not (dynamic VPN) or static routes
are missing. CloudWatch `AWS/VPN` `TunnelState`: for BGP VPNs 1 = ESTABLISHED and 0 = any other state; for
static VPNs 1 = UP and 0 = DOWN; values between 0 and 1 mean at least one tunnel is not up (dimension
`VpnId`; `TunnelIpAddress` filters one tunnel). `TunnelDataIn` / `TunnelDataOut` are bytes (use Sum).

## 2. Turn on tunnel logs
Tunnel options, `LogOptions.CloudWatchLogOptions` (format `json` or `text`). Two logs are published, with
stream names built from the VPN connection ID and tunnel outside IP: the tunnel activity log (fields
`ike_phase1_state`, `ike_phase2_state` = Established / Rekeying / Negotiating / Down, `nat_t_detected`,
`dpd_enabled`, `details`) and the tunnel BGP log (`type` BGPStatus or RouteStatus, `status`, `message`).
CloudWatch Logs resource policies are limited to 5120 characters: name the log group with the
`/aws/vendedlogs/` prefix to avoid hitting it.
Logs Insights:
```
fields @timestamp, details
| filter @logStream like /203.0.113.11/
| sort @timestamp desc | limit 100
```

## 3. Messages and what they mean (from the logs page)
| Log message (abridged) | Meaning | Fix |
|---|---|---|
| `Peer is not responsive - Declaring peer dead` (IKEv1) / `AWS tunnel DPD timed out after N retransmits` (IKEv2) | Peer stopped answering DPD; the DPD timeout action is enforced | CGW reboot or path loss; review the DPD timeout action |
| `No Proposal Match Found by AWS` | Proposed phase 1/2 attributes (encryption, hashing, DH group) are not supported by AWS, for example 3DES | Align the suites with the tunnel options |
| `AWS tunnel detected a pre-shared key mismatch` / `payload decryption was unsuccessful due to invalid Pre-shared Key` | PSK differs | Configure the same PSK on both peers |
| `AWS tunnel is sending AUTHENTICATION_FAILED as the response` | AWS cannot authenticate the peer from the IKE_AUTH message | Check PSK or certificate |
| `Traffic Selector: TS_UNACCEPTABLE` | The peer proposed incorrect traffic selectors | Configure identical, correct CIDRs; use a route-based device |
| `Timeout: deleting un-established Phase 1 IKE_SA` | Half-open IKE_SA, the peer did not proceed | Check reachability of UDP 500/4500 |
| `AWS-side peer detected a bad OPEN message ... remote AS is X, expected Y` | BGP ASN mismatch | Fix the ASN on the device |
| `AWS-side peer sent a Hold Timer Expired notification` | BGP hold timer expired | Check path loss and keepalives |
| BGP stuck in Connect | | Check TCP port 179 availability on the CGW |

## 4. Tunnel UP, no traffic
1. **BGP**: the device must show the AWS neighbor Established with prefixes received. Common issues: ASN
   mismatch and hold-timer expiry (see above), and the CGW advertising more routes than the quota (dynamic
   routes from the CGW: 100 per VPN connection on a virtual private gateway, 1,000 on a transit gateway;
   not adjustable; summarise).
2. **Static VPN**: static routes added on the VPN connection (`create-vpn-connection-route`; limit 100 on a VGW).
3. **VPC routing**: route tables have propagation from the VGW enabled (`enable-vgw-route-propagation`) or
   static routes to the VGW; on a transit gateway, check the VPN attachment association and propagation in the TGW route table.
4. **SGs/NACLs** allow the on-prem CIDRs.
5. **MTU/MSS**: Site-to-Site VPN supports at most MTU 1446 and MSS 1406 (less with some algorithms); no Path MTU
   Discovery and no jumbo frames. Symptoms of a mismatch: small pings work, large transfers hang.
6. **Idle tunnel**: without AWS-side IKE initiation a tunnel can go down after idle time (usually about 10 seconds,
   depending on configuration); use keepalive pings or the `start` startup action.

## 5. Monitoring to set up
- Alarm `TunnelState` below 1 (one tunnel down is a warning, both is critical).
- Subscribe to AWS Health events for Site-to-Site VPN (look up the event type codes in the AWS Health docs).
- On the device: BGP session alarms, interface errors.

## Verify
- [ ] Both tunnels UP with BGP established and expected accepted routes.
- [ ] Large-packet `ping` with the do-not-fragment flag set at your computed MTU succeeds end to end.
- [ ] Tunnel logs enabled and alarms tested by disabling one tunnel on the device.

## Checked
2026-10-28. Confirmed on monitoring-logs, monitoring-cloudwatch-vpn and vpn-limits pages: log field names and states, the 5120-character policy limit and `/aws/vendedlogs/` prefix, log messages in the table, TunnelState semantics and dimensions, route quotas, MTU/MSS, idle behaviour. Fixed: the 0.5 average claim (any fractional value), `NO_PROPOSAL_CHOSEN` replaced by the real log text, TS_UNACCEPTABLE cause. Removed as unconfirmed: ESP protocol 50 and NAT-T cause list, "keep CGW lifetimes at or below AWS", AS-path prepend/MED advice, MSS 1379, `AWS_VPN_REDUNDANCY_LOSS`, hold-timer mismatch as a cause beyond the documented message.
Method: documentation only; no commands were run.
