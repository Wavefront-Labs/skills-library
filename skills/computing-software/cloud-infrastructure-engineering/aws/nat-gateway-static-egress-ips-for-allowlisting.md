---
id: computing-software.cloud-infrastructure-engineering.aws.nat-gateway-static-egress-ips-for-allowlisting
name: nat-gateway-static-egress-ips-for-allowlisting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, nat-gateway, static-egress-ip, nat-eip, ip-allowlisting, centralized-egress]
level: practitioner
status: docs-checked
description: "Give partners a small, stable set of egress IPs to allowlist using NAT gateway Elastic IPs, secondary EIPs, centralized egress and BYOIP."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-working-with.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-byoip.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static egress IPs via NAT gateway EIPs

## 1. List what partners must allow
```bash
aws ec2 describe-nat-gateways --filter Name=vpc-id,Values=vpc-0abc Name=state,Values=available \
  --query 'NatGateways[].{az:SubnetId,ips:NatGatewayAddresses[].PublicIp}'
```
One NAT per AZ means one IP per AZ; give the partner all of them, or traffic from one AZ fails intermittently.

## 2. Keep IPs stable
- Allocate EIPs separately (tagged, protected by IAM) and pass `--allocation-id` to `create-nat-gateway`;
  recreating the NAT with the same allocation keeps the IP.
- Never let IaC allocate the EIP inside the same resource that might be replaced.

## 3. Need more IPs (port exhaustion) without new allowlist entries?
```bash
aws ec2 associate-nat-gateway-address --nat-gateway-id nat-0abc --allocation-ids eipalloc-0new
```
A public NAT gateway can have up to 8 IPv4 addresses (1 primary and 7 secondary) and is limited to 2 Elastic IPs by default
(adjustable); each secondary EIP needs a private IPv4 address and its network border group must match the gateway's. Each added EIP
must be allowlisted too, so pre-register a block.

## 4. Fewer IPs across many VPCs
Centralized egress VPC behind Transit Gateway: all spokes leave through the NAT gateways of one VPC, so the partner list stays
short no matter how many accounts you add. A public NAT gateway uses its Elastic IP as the source only when traffic goes via the
VPC's internet gateway; toward a transit gateway or virtual private gateway the source is the NAT gateway's private IP.

## 5. Your own range
Bring your own IPv4 range (the most specific range you can bring is a /24) and allocate EIPs from it
(`allocate-address --public-ipv4-pool ipv4pool-ec2-...`) when the partner allowlists by CIDR.

## 6. Regional NAT gateways
A regional NAT gateway spans Availability Zones with one NAT ID and supports up to 32 IP addresses per AZ. In automatic mode AWS
manages the IP addresses and AZ expansion, so for a fixed allowlist use manual mode and associate your own Elastic IPs per AZ
(`associate-nat-gateway-address --availability-zone ... --allocation-ids ...`). Regional NAT gateways do not support private NAT, and
migrating from zonal gateways while keeping the same IPs requires deleting the zonal gateways first, with a traffic interruption.

## Verify
- [ ] From instances in each AZ, an external IP-echo service you trust returns one of the listed IPs.
- [ ] EIPs tagged and covered by an SCP/IAM deny on `ec2:ReleaseAddress`.

## Checked

Date: 2026-10-27. Sources: Amazon VPC User Guide pages "NAT gateways", "Work with NAT gateways", "Regional NAT gateways for automatic multi-AZ expansion", "NAT gateway basics" and "Amazon VPC quotas"; EC2 User Guide "Bring your own IP addresses (BYOIP)"; botocore EC2 model (AssociateNatGatewayAddress AllocationIds and AvailabilityZone, AllocateAddress, NatGateway).
Confirmed: 8 addresses per zonal gateway (1 primary, 7 secondary), default 2 Elastic IPs, secondary EIP needs a private address and matching network border group; /24 is the most specific BYOIP IPv4 range; regional gateway limits and manual mode; source-IP behaviour toward transit and virtual private gateways.
Removed: the claim that BYOIP gives IPs that survive account changes (not documented).

Method: documentation only; no commands were run.
