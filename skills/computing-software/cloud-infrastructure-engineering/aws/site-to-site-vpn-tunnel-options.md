---
id: computing-software.cloud-infrastructure-engineering.aws.site-to-site-vpn-tunnel-options
name: site-to-site-vpn-tunnel-options
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, site-to-site-vpn, tunnel-options, ike-version, dead-peer-detection, ipsec, phase1-phase2]
level: advanced
status: docs-checked
description: "Tune Site-to-Site VPN tunnel options to match the customer gateway: IKE versions, phase 1/2 algorithms and lifetimes, DPD action, startup action, inside CIDRs and PSKs."
sources: ["https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/tunnel-configure.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/initiate-vpn-tunnels.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/modify-vpn-tunnel-options.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/vpn-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site-to-Site VPN tunnel options

Each VPN connection has two tunnels, each with independent options. Defaults are permissive
(many algorithms allowed) so most devices negotiate; tighten them to what your device
uses to avoid weak-suite fallback and flapping.

## 1. Options, defaults and limits (from the tunnel options page)
| Option | Default | Allowed / note |
|---|---|---|
| IKE versions | ikev1, ikev2 | one or more of the defaults; suggest `ikev2` only if the device supports it |
| Phase 1 encryption | AES128, AES256, AES128-GCM-16, AES256-GCM-16 | one or more of the defaults |
| Phase 2 encryption | same four | one or more of the defaults |
| Phase 1 / Phase 2 integrity | SHA1, SHA2-256, SHA2-384, SHA2-512 | one or more of the defaults |
| Phase 1 DH groups | 2, 14-24 | one or more of the defaults |
| Phase 2 DH groups | 2, 5, 14-24 | one or more of the defaults |
| Phase 1 lifetime | 28,800 s | 900-28,800 |
| Phase 2 lifetime | 3,600 s | 900-3,600, must be less than the phase 1 lifetime |
| Rekey margin time | 270 s | 60 up to half the phase 2 lifetime |
| Rekey fuzz | 100 % | 0-100 |
| Replay window size | 1,024 packets | 64-2048 |
| DPD timeout | 40 s | 30 or higher |
| DPD timeout action | `clear` (end IKE session, drop tunnel and routes) | `none`, `restart` (AWS restarts the IKE session) |
| Startup action | `add` (the CGW must initiate) | `start` (AWS initiates; IKEv2 only; needs a CGW with an IP address) |
| Inside IPv4 CIDR | a /30 from 169.254.0.0/16 | must be unique across connections on the same virtual private gateway; on a transit gateway it need not be unique, but reuse can conflict on the CGW |
| Pre-shared key | 32-character alphanumeric | 8-64 chars, alphanumeric, `.` and `_`, cannot start with 0 |
| Local / remote IPv4 network CIDR | 0.0.0.0/0 | proposed in phase 2; AWS is route-based only |
| Tunnel bandwidth | Standard (up to 1.25 Gbps) | Large (up to 5 Gbps) only on transit gateway or Cloud WAN attachments |
| Log formats | | `json` or `text` |
Reserved inside CIDRs: 169.254.0.0/30, 169.254.1.0/30, 169.254.2.0/30, 169.254.3.0/30, 169.254.4.0/30,
169.254.5.0/30, 169.254.169.252/30. Lifecycle control default is off.
AWS initiates rekeys using the phase 1 and phase 2 lifetimes; if the device uses different values the
tunnel connectivity may be interrupted.

Check the current values in the downloaded device configuration or:
```bash
aws ec2 describe-vpn-connections --vpn-connection-ids vpn-0abc \
  --query 'VpnConnections[0].Options.TunnelOptions'
```

## 2. Modify one tunnel at a time
```bash
aws ec2 modify-vpn-tunnel-options --vpn-connection-id vpn-0abc \
  --vpn-tunnel-outside-ip-address 203.0.113.11 \
  --tunnel-options '{"IKEVersions":[{"Value":"ikev2"}],
    "Phase1EncryptionAlgorithms":[{"Value":"AES256-GCM-16"}],
    "Phase2EncryptionAlgorithms":[{"Value":"AES256-GCM-16"}],
    "Phase1DHGroupNumbers":[{"Value":20}],"Phase2DHGroupNumbers":[{"Value":20}],
    "DPDTimeoutAction":"restart","StartupAction":"start",
    "LogOptions":{"CloudWatchLogOptions":{"LogEnabled":true,
      "LogGroupArn":"arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/vpn/tunnels","LogOutputFormat":"json"}}}'
```
Do tunnel 1, wait for it to come back UP (and BGP established), then tunnel 2, and change the
device side to match during the same window. `modify-vpn-tunnel-options` also accepts
`--skip-tunnel-replacement`; see the tunnel endpoint lifecycle page for scheduling AWS-side replacements.

## 3. Matching the device
- Download a device-specific config: `aws ec2 get-vpn-connection-device-sample-configuration
  --vpn-connection-id vpn-0abc --vpn-connection-device-type-id <id> --internet-key-exchange-version ikev2`
  (`get-vpn-connection-device-types` lists ids).
- Policy-based devices are not supported: AWS uses route-based VPNs exclusively and the local/remote
  network CIDRs default to 0.0.0.0/0. Use a route-based (VTI) configuration on the device.
- NAT-T: if the CGW is behind NAT, use the NAT's public IP as the CGW IP, allow UDP 500 and 4500, and
  configure an identity (IDr) on the device if you use AWS-side initiation.
- MTU: Site-to-Site VPN supports MTU 1446 and MSS 1406 at most; some algorithms lower that. No Path MTU Discovery, no jumbo frames.
- Without AWS-side initiation an idle tunnel (usually 10 seconds of idle, depending on configuration)
  might go down; generate keepalive pings with a monitoring tool or set `StartupAction` to `start`.

## Gotchas
- Narrowing algorithms to something the device does not offer leaves the tunnel DOWN; the tunnel logs
  show "No proposal chosen" / "No Proposal Match Found by AWS".
- When one tunnel is unavailable (for example in maintenance) traffic uses the other tunnel, so
  configure both.

## Verify
- [ ] Both tunnels `UP` and BGP `ESTABLISHED` after the change (`VgwTelemetry`).
- [ ] Tunnel logs show the negotiated suite matches the intended one.
- [ ] CloudWatch alarm on `TunnelState` exists (per connection with `VpnId`, per tunnel with `TunnelIpAddress`; 1 = up/established, fractional values mean at least one tunnel is not up).

## Checked
2026-10-28. Confirmed against the tunnel-configure, initiate-vpn-tunnels, VPNTunnels, vpn-limits and monitoring-cloudwatch-vpn pages, and the ec2 botocore model (`StartupAction`, `SkipTunnelReplacement`, `LogOptions` members). Fixed: DPD timeout default is 40 s (was 30), phase 2 DH defaults include 5, reserved CIDR 169.254.169.252/30 (was mangled), inside CIDR uniqueness differs for VGW and transit gateway, policy-based devices are not supported (the old one-SA-pair advice was wrong). Removed as unconfirmed: "modifying" state and several-minute outage, tunnel logging default off, PFS group recommendation, MSS 1379 (replaced by the documented MTU 1446/MSS 1406), the NO_PROPOSAL_CHOSEN literal.
Method: documentation only; no commands were run.
