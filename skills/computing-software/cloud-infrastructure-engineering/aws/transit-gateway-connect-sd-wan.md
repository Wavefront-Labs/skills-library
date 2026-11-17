---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-connect-sd-wan
name: transit-gateway-connect-sd-wan
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-connect, gre-attachment, sd-wan, bgp, virtual-appliance, hybrid-connectivity]
level: practitioner
status: docs-checked
description: "Integrate SD-WAN appliances with Transit Gateway Connect: transport attachment, GRE Connect peers, BGP inside addresses, ECMP across peers and bandwidth limits."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-connect.html", "https://aws.amazon.com/blogs/networking-and-content-delivery/simplify-sd-wan-connectivity-with-aws-transit-gateway-connect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit Gateway Connect for SD-WAN

**Goal:** third-party SD-WAN/virtual router appliances in a VPC (or on-prem over DX) exchange
routes with TGW dynamically over GRE + BGP, using an existing VPC or Direct Connect attachment as transport.

## 1. Build
```bash
# transport: an existing VPC (or DX gateway) attachment where the appliances live
CONNECT=$(aws ec2 create-transit-gateway-connect --transport-transit-gateway-attachment-id att-sdwan-vpc \
  --options Protocol=gre --query TransitGatewayConnect.TransitGatewayAttachmentId --output text)
aws ec2 create-transit-gateway-connect-peer --transit-gateway-attachment-id $CONNECT \
  --peer-address 10.50.1.10 --transit-gateway-address 192.0.2.10 \
  --bgp-options PeerAsn=65010 --inside-cidr-blocks 169.254.100.0/29
```
- `peer-address`: the appliance's IP (in the transport VPC or on-prem via DX).
- `transit-gateway-address`: from a transit gateway CIDR block (add one to the TGW first, e.g.
  192.0.2.0/24); it must be unique across the transit gateway, and if omitted the first available
  address is used. The subnet route table must send the TGW CIDR block to the TGW.
- Inside CIDR: a /29 from 169.254.0.0/16 (169.254.0.0/29 to 169.254.5.0/29 and 169.254.169.248/29
  are reserved); unique across all tunnels on the TGW. Configure the first address of the range on
  the appliance as its BGP IP.
- Each Connect peer has two BGP sessions for redundancy; configure both on the appliance.

## 2. Appliance side (pseudo)
```
interface Tunnel1  source 10.50.1.10  destination 192.0.2.10  mode gre  ip 169.254.100.1/29
router bgp 65010
  neighbor <TGW_BGP_ADDRESS_1> remote-as <TGW_ASN>  (ebgp-multihop 2)
  neighbor <TGW_BGP_ADDRESS_2> remote-as <TGW_ASN>
```

## 3. Scale
- Up to 4 Connect peers per Connect attachment; each GRE tunnel up to 5 Gbps and 300,000 packets per
  second; up to 20 Gbps per attachment if the transport supports it. ECMP needs the same prefixes
  with the same AS-PATH and ASN, and works across peers of one attachment or across Connect
  attachments on one TGW, not across the two BGP sessions of one peer.
- Routes from a Connect attachment are propagated to a TGW route table by default; static routes
  are not supported, nor are BFD, graceful restart or IPv6 BGP peering (IPv6 prefixes ride IPv4 BGP).
- Default BGP keepalive is 10 seconds and hold timer 30 seconds.

## Gotchas
- Packets with wrong GRE outer addresses are treated as transport-attachment traffic, not Connect traffic.
- Set the GRE tunnel MTU below the external interface MTU by 24 bytes (4 GRE + 20 outer IP), e.g. 1476 on a 1500 interface.
- Check BGP status (`up` or `down`) per session in `describe-transit-gateway-connect-peers`.

## Verify
- [ ] `describe-transit-gateway-connect-peers` shows both BGP sessions `up`.
- [ ] Branch prefixes appear as propagated routes in the TGW route table.
- [ ] ECMP: traffic counters on multiple Connect peers increase under load.

## Checked
2026-10-28. Confirmed against the Transit Gateway guide pages "Connect attachments and Connect peers" (GRE and BGP, transport attachments, inside CIDR /29 and reserved ranges, TGW address rules, two BGP sessions, ebgp-multihop TTL 2, ECMP rules, defaults, unsupported features, MTU arithmetic) and "Quotas" (4 peers, 5 Gbps and 300,000 pps per peer, 20 Gbps per attachment), plus botocore ec2 (CreateTransitGatewayConnectPeer members, protocol gre, BgpStatus up/down). Removed unconfirmed claims: the "higher bandwidth than VPN" comparison, TGW BGP neighbor addresses .2/.3, the GRE protocol 47 security group note and "routes withdrawn" behaviour; replaced the wrong 8500 GRE MTU gotcha. The blog source was not read.
Method: documentation only; no commands were run.
