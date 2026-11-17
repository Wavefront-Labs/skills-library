---
id: computing-software.cloud-infrastructure-engineering.aws.site-to-site-vpn-and-direct-connect
name: site-to-site-vpn-and-direct-connect
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, hybrid-connectivity, site-to-site-vpn, vpn, direct-connect, dx, virtual-private-gateway, customer-gateway, transit-gateway-vpn, bgp, ipsec, ikev2, ecmp, accelerated-vpn, direct-connect-gateway, virtual-interface, private-vif, transit-vif, public-vif, lag, macsec, sitelink, hosted-connection, loa-cfa, bgp-communities, mtu, dx-failover, hybrid-network]
level: advanced
status: docs-checked
description: "Connect on-prem to AWS: Site-to-Site VPN (tunnels, BGP, ECMP on Transit Gateway) and Direct Connect (VIFs, DX Gateway, LAG, resiliency, VPN failover) with the limits that bite."
sources: ["https://docs.aws.amazon.com/vpn/latest/s2svpn/vpn-limits.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/limits.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/routing-and-bgp.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/start_failover_test.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/MACsec.html", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/interface-set-mtu.html", "https://github.com/boto/botocore/tree/develop/botocore/data/ec2"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Site-to-Site VPN and Direct Connect — hybrid connectivity that fails over cleanly

**Goal:** on-prem reaches every VPC through one hub, bandwidth matches the need, the
link survives a device or location loss, and failover from Direct Connect to VPN is
automatic and tested. VPC-side routing (Transit Gateway, route tables) is in
`...aws.vpc-network-design`; the VPC-to-VPC hub is in the transit-gateway skill there.

## 1. Pick the primitive
| Need | Use |
|---|---|
| Get connected this week, < 1.25 Gbps per tunnel, internet is acceptable | **Site-to-Site VPN** on Transit Gateway |
| Consistent latency, > 1 Gbps, private path, lower egress cost | **Direct Connect** (dedicated or hosted) |
| DX plus a backup that does not need a second circuit | DX primary + VPN over the internet as BGP backup |
| Encryption over DX | Private IP VPN over a transit VIF, or MACsec on dedicated 10/100/400 Gbps |
Terminate both on **Transit Gateway** (not a Virtual Private Gateway per VPC) unless you
have one VPC and no plans: TGW gives ECMP across VPN tunnels, one BGP session set for
all VPCs, and a single place for route tables.

## 2. Site-to-Site VPN
- Create a **customer gateway** (your device's public IP + BGP ASN, e.g. 65000) and a
  VPN connection on the TGW: `aws ec2 create-vpn-connection --type ipsec.1
  --customer-gateway-id cgw-… --transit-gateway-id tgw-… --options
  'TunnelOptions=[{TunnelInsideCidr=169.254.10.0/30,PreSharedKey=<PSK>},{TunnelInsideCidr=169.254.11.0/30,PreSharedKey=<PSK>}]'`.
  Download the vendor config (`--vpn-connection-device-type-id` from
  `get-vpn-connection-device-types`) and paste it, then adjust.
- Every connection has **two tunnels** to two AWS endpoints; keep both up. With **BGP**
  use AS-path prepend or MED on your side to prefer one tunnel, or enable **ECMP** on the TGW
  attachment and let both carry traffic (and add more VPN connections to scale beyond
  1.25 Gbps per tunnel; ECMP needs dynamic routing, not static).
- Tunnel options worth setting: IKEv2 only (`IKEVersions`); `DPDTimeoutAction`; `StartupAction`
  (AWS initiates, needed when your side only responds); `Phase1LifetimeSeconds` and
  `Phase2LifetimeSeconds` set so rekeys are never simultaneous; a tunnel inside CIDR
  that avoids the reserved ranges in the tunnel options page; `--local-ipv4-network-cidr`
  and `--remote-ipv4-network-cidr` to narrow the policy-based SA when the device is
  policy-based (otherwise AWS expects route-based 0.0.0.0/0 ↔ 0.0.0.0/0 and a
  policy-based device will keep flapping between SAs).
- **Accelerated VPN** is the `EnableAcceleration` option of `create-vpn-connection`
  (set at creation).
- MTU: Site-to-Site VPN supports an MTU of 1446 bytes and an MSS of 1406 (less with
  algorithms that use larger TCP headers); jumbo frames and Path MTU Discovery are not
  supported. Clamp the MSS on the device (see the AWS best-practices page for the exact
  value per algorithm), or fragmentation will show up as "small files work, big files hang".
- Routes your device may advertise per VPN connection: 100 on a virtual private gateway,
  1,000 on a transit gateway (not adjustable). Summarise.
- Monitoring: alarm on *either* tunnel's CloudWatch state metric, not the connection,
  and on
  `aws ec2 describe-vpn-connections --query 'VpnConnections[].VgwTelemetry'`.
  VPN logs to CloudWatch (`LogOptions`) show IKE negotiation failures in plain text.

## 3. Direct Connect
- **Dedicated connection** (1, 10, 100, 400 Gbps port in a DX location; AWS issues a
  **LOA-CFA** you hand to the colo for cross-connect) or **hosted connection** via a DX
  partner (partner provisions the port and sets the speed; faster to get). Hosted
  connections carry one VIF each; dedicated ports carry up to 50 private/public VIFs
  and 4 transit VIFs (51 VIFs in total).
- Then create a **virtual interface** on it (802.1Q VLAN id, your BGP ASN, optional
  BGP auth key, /30 peer IPs):
  - **Private VIF** → a VGW (one VPC) or a **Direct Connect gateway** (up to 20 VGWs
    across accounts/regions, non-overlapping CIDRs);
  - **Transit VIF** → a DX gateway associated with up to 6 Transit Gateways — the
    normal enterprise design;
  - **Public VIF** → AWS public endpoints (S3, DynamoDB, public IPs) over the private
    link; you receive all AWS public prefixes for the chosen scope.
- **Allowed prefixes** on a DX gateway–TGW association are what AWS advertises *to
  you* for that TGW: the Direct Connect quota is 200 prefixes (IPv4 and IPv6 combined)
  per transit gateway — summarise your VPC space.
  Routes you advertise per BGP session: default 100 each for IPv4 and IPv6 on a private
  or transit VIF (raisable to 1,000 with prefix controls); 1,000 on a public VIF. Beyond
  the limit the session goes idle and reports DOWN.
- **LAG** bundles up to 4 same-speed ports (2 when the port speed is 100G) on the same device for bandwidth, not
  resilience (one LAG = one device). `--minimum-links` decides when the LAG is down.
- **Resiliency** per AWS's own models: use two connections at **two locations** at least, ideally two devices at each. Use the
  Resiliency Toolkit in the console to order it that way, then **Failover Test** (`start-bgp-failover-test`; the console default is 180 minutes, maximum 4,320)
  to prove the backup carries production.
- Jumbo frames: a private VIF can be set to jumbo MTU 8500 (`update-virtual-interface-attributes`; the VIF goes
  down briefly); it must be supported end to end, else PMTU black holes. Check the
  MTU page of the Direct Connect guide for transit VIFs.
- **MACsec** needs a dedicated 10/100/400 Gbps port at a MACsec-capable location and
  CKN/CAK pairs on both sides; **SiteLink** lets two on-prem sites talk via the AWS
  backbone through their DX VIFs.
- Costs: see the Direct Connect pricing page.

## 4. DX with VPN failover
- Terminate DX (transit VIF) and VPN on the same TGW. Keep the advertised prefix
  lengths equal on both paths (do not advertise a more specific over VPN by accident).
- From your side, prefer DX with higher **local preference** on routes learned from DX;
  AWS honours BGP communities on its side: `7224:7100` (low), `7224:7200` (medium),
  `7224:7300` (high) for local preference on private and transit VIFs; `7224:9100/9200/9300` on public VIFs
  control how far AWS re-advertises your prefixes (local Region/continent/global).
- Test by shutting the DX BGP session (failover test) and watching
  `TransitGateway BytesIn` move to the VPN attachment within the BGP hold time (set short
  hold and keepalive timers on both sides). Enable **Bidirectional Forwarding Detection**
  (BFD) on your router for faster failure detection (check the Direct Connect guide for defaults).

## Gotchas
- VPN over DX public VIF, or DX + VPN, counts as two *paths*; asymmetric routing (out
  via DX, back via VPN) breaks stateful on-prem firewalls. Keep prefixes symmetric.
- A DX connection "available" with the VIF "down" is almost always VLAN tagging or the
  BGP peer IP on the wrong side of the /30.
- Compare VPN and DX costs on the vendor's pricing pages before choosing.
- DX is not encrypted; many compliance regimes treat it as untrusted — plan private IP
  VPN or MACsec from the start.
- The TGW attachment for VPN is per connection; an ECMP set needs the connections on
  the same TGW route table with the **same** advertised prefixes and ECMP support enabled on the TGW (VPN connections must use dynamic routing).
- Customer gateway IP changes (ISP swap) mean a new CGW object and new VPN connection:
  PSKs, inside CIDRs and device config all change; script it.

## Verify
- [ ] Both VPN tunnels `UP` with BGP routes received and advertised; alarms per tunnel exist.
- [ ] Iperf through the VPN sustains the expected rate with MSS clamped; large file transfers do not stall.
- [ ] DX VIF BGP `up`, BFD active, advertised prefixes ≤ allowed-prefix limits; jumbo MTU verified with `ping -M do -s 8472` (8500 minus 28 bytes of headers).
- [ ] `start-bgp-failover-test` on the primary DX moves traffic to backup within hold-time and nothing on-prem notices beyond a latency bump.
- [ ] Monthly egress bill shows DX data-transfer rates, not internet rates, for the on-prem-bound traffic.

## Checked
2026-10-31. Confirmed in the VPN quotas page, the Direct Connect quotas, routing-and-bgp, failover-test, MACsec and jumbo-MTU pages: 1.25 Gbps per tunnel; MTU 1446 / MSS 1406; 100 dynamic routes on a VGW and 1,000 on a transit gateway; ECMP needs dynamic routing; 50 private/public + 4 transit VIFs (51 total) per dedicated connection and 1 per hosted; 20 VGWs and 6 transit gateways per DX gateway; 200 prefixes per transit gateway; 100 default / 1,000 maximum routes per BGP session on private and transit VIFs and 1,000 on public; LAG of 4 ports (2 at 100G); failover test default 180 and maximum 4,320 minutes; jumbo MTU 8500; BGP communities 7224:7100/7200/7300 and 7224:9100/9200/9300; MACsec port speeds. CLI flags and option names (EnableAcceleration, tunnel options, LogOptions) were confirmed against the botocore EC2 model. Removed as unconfirmed: the ECMP aggregate figure, static-routing tunnel preference, DPD/startup values, reserved tunnel CIDR detail, Global Accelerator wording, TGW DX-over-VPN default, resiliency model names, CloudWatch metric names, pricing statements.
Method: documentation only; no commands were run.
