---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-attachments-and-appliance-mode
name: transit-gateway-attachments-and-appliance-mode
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-attachment, appliance-mode, tgw-peering, vpn-attachment, direct-connect-gateway, inter-region]
level: practitioner
status: docs-checked
description: "Attach VPCs, VPNs, Direct Connect gateways and peer TGWs: attachment subnets per AZ, appliance mode for stateful inspection, and inter-region TGW peering with static routes."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-vpc-attachments.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html", "https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html", "https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit Gateway attachments, appliance mode and peering

## 1. VPC attachments
```bash
aws ec2 create-transit-gateway-vpc-attachment --transit-gateway-id tgw-123 --vpc-id vpc-abc \
  --subnet-ids subnet-tgw-a subnet-tgw-b subnet-tgw-c \
  --options DnsSupport=enable,Ipv6Support=disable,SecurityGroupReferencingSupport=enable
```
- Enable each AZ by specifying exactly one subnet; the TGW places an ENI (one IP address) there and can then reach
  every subnet in that AZ. A small dedicated subnet per AZ for the attachment is the usual design.
- Only resources in AZs where the VPC attachment has a subnet can reach the TGW; traffic sourced from an AZ where
  the destination attachment is absent is routed internally to a random AZ where it is present (no extra TGW charge for that cross-AZ hop). Enable several AZs for availability.
- Bandwidth per VPC attachment per AZ: up to 100 Gbps each direction, up to 7,500,000 packets per second (quotas page, read 2026-10-27).
- VPC route tables still need a route to the TGW; attachments do not enable communication between subnets of the same VPC.

## 2. Appliance mode
For VPCs hosting stateful appliances (firewalls, inspection VPC):
```bash
aws ec2 modify-transit-gateway-vpc-attachment --transit-gateway-attachment-id att-inspect \
  --options ApplianceModeSupport=enable
```
With appliance mode the TGW keeps the same appliance-VPC AZ for the lifetime of a flow (both directions), so stateful
inspection sees a symmetric flow. It is supported on VPC attachments only. With route propagation enabled on the route
table associated with the appliance attachment, same-AZ flows use that AZ and cross-AZ flows use a flow hash; without
propagation everything falls back to flow-hash selection. Enabling it later on an existing attachment can rebalance
flows across AZs.

## 3. VPN and Direct Connect
- VPN attachment: `create-vpn-connection --transit-gateway-id ...`; ECMP across tunnels needs `VpnEcmpSupport=enable`
  on the TGW and a VPN connection with dynamic routing (static routing does not support ECMP).
- DX: associate a **Direct Connect gateway** with the TGW (transit VIF), listing allowed
  prefixes to advertise to on-prem.

## 4. Inter-region peering
```bash
aws ec2 create-transit-gateway-peering-attachment --transit-gateway-id tgw-use1 \
  --peer-transit-gateway-id tgw-euw1 --peer-account-id <ACCOUNT_ID> --peer-region eu-west-1
aws ec2 accept-transit-gateway-peering-attachment --region eu-west-1 --transit-gateway-attachment-id tgw-attach-peer
```
- Peering attachments support static routes only: add static routes in both TGWs' route tables for the remote CIDRs.
- The docs recommend a unique ASN per peered TGW. Inter-Region traffic is encrypted at the network layer; the accepter TGW's owner must accept the request.
- Intra-Region peering between TGWs is supported too.

## Gotchas
- A TGW cannot have more than one VPC attachment to the same VPC.
- Security group referencing across attachments works only if enabled on both the TGW and its VPC attachments (inbound rules only).
- Peering attachment acceptance is manual by the accepter side.

## Verify
- [ ] `describe-transit-gateway-vpc-attachments` shows subnets in every AZ used by workloads and `ApplianceModeSupport=enable` where inspection lives.
- [ ] Cross-AZ flow through the firewall passes both directions (firewall flow logs show same AZ).
- [ ] Cross-region ping/curl between VPCs works after static routes are added in both TGWs.

## Checked

Checked 2026-10-27 against the AWS Transit Gateway documentation (how transit gateways work, VPC attachments, peering, quotas) and the botocore ec2 2016-11-15 model.
- Corrected: appliance mode is AZ-aware (same-AZ flows stay in the AZ when propagation is on, cross-AZ flows use a flow hash, no propagation falls back to flow hash); traffic from an AZ without the destination attachment is routed to a random AZ that has it; VPN ECMP needs dynamic routing; security group referencing must be enabled on both the TGW and the attachment.
- Confirmed: one subnet per enabled AZ, up to 100 Gbps and 7,500,000 packets per second per VPC attachment per AZ, peering supports static routes only, accepter must accept, unique ASNs recommended, `ApplianceModeSupport` and `SecurityGroupReferencingSupport` option names.
- Removed: /28 sizing, "blackhole routes left behind on deletion", inter-Region price statement and hash-of-5-tuple wording that no page confirmed.

Method: documentation only; no commands were run.
