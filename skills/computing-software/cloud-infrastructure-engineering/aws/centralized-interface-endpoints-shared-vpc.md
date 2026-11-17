---
id: computing-software.cloud-infrastructure-engineering.aws.centralized-interface-endpoints-shared-vpc
name: centralized-interface-endpoints-shared-vpc
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-endpoints, centralized-endpoints, shared-endpoints, endpoint-phz, private-hosted-zone, transit-gateway, cost-optimization]
level: practitioner
status: docs-checked
description: "Share one set of interface endpoints across many VPCs: hub endpoints with private DNS off, a private hosted zone with alias records, cross-account association and the trade-offs."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/centralized-access-to-vpc-private-endpoints.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zone-private-associate-vpcs-different-accounts.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centralised interface endpoints

**Goal:** per the whitepaper, an interface endpoint is billed for every hour it runs plus data processing, and by default you
create one in every VPC that needs the service. In a landing zone that can be cost prohibitive and hard to manage, so host the
interface endpoints in a centralised VPC and let spoke VPCs use them over Transit Gateway.

## 1. Hub endpoints with private DNS **off**
With private DNS on, the managed private hosted zone (PHZ) only works inside the VPC that has the endpoint, so spokes cannot
resolve it. Disable the automatic private DNS option when creating the endpoint.
```bash
aws ec2 create-vpc-endpoint --vpc-id <HUB_VPC_ID> --vpc-endpoint-type Interface \
  --service-name com.amazonaws.<REGION>.<SERVICE> --subnet-ids <SUBNET_A> <SUBNET_B> \
  --security-group-ids <ENDPOINT_SG_ID> --no-private-dns-enabled
```
- One subnet per Availability Zone, never two in the same AZ. The security group must allow the traffic from the
  resources (HTTPS for the AWS CLI); also check network ACLs. Endpoint network interfaces take IPs from the subnets.
- Create the endpoints and the PHZ in a network-services account and share the PHZ with the spoke accounts (whitepaper).

## 2. One private hosted zone per service
Create a PHZ matching the service endpoint name (e.g. `<SERVICE>.<REGION>.amazonaws.com`) and add an `A` alias record with
the full service endpoint name pointing at the interface endpoint. Per the whitepaper, some services such as `dkr.ecr`
need a wildcard (`*`) alias record name; it also selects the routing policy and enables "Evaluate target health".
```bash
aws route53 create-hosted-zone --name <SERVICE>.<REGION>.amazonaws.com --caller-reference <UNIQUE_STRING> \
  --vpc VPCRegion=<REGION>,VPCId=<HUB_VPC_ID> --hosted-zone-config PrivateZone=true
```

## 3. Associate the PHZ with spoke VPCs (cross-account)
Per the Route 53 page: authorise from the account that owns the hosted zone, then associate from the account that owns the VPC.
```bash
# hosted-zone account (one authorisation per VPC)
aws route53 create-vpc-association-authorization --hosted-zone-id <ZONE_ID> --vpc VPCRegion=<REGION>,VPCId=<SPOKE_VPC_ID>
# VPC account
aws route53 associate-vpc-with-hosted-zone --hosted-zone-id <ZONE_ID> --vpc VPCRegion=<REGION>,VPCId=<SPOKE_VPC_ID>
```
- The hosted zone must already exist; the Route 53 console cannot authorise or make this association.
- Deleting the authorisation afterwards is recommended and does not remove the association.
- `ListHostedZonesByVPC` and `GetHostedZone` only reflect associations made by `AssociateVPCWithHostedZone` or at
  PHZ creation; also call `ListProfileResourceAssociations` for a complete list.
- Spoke hosts must use their VPC's Route 53 Resolver. On-premises clients reach the endpoints over VPN or Direct Connect
  through conditional forwarding to Route 53 Resolver inbound endpoints (whitepaper).

## Trade-offs (whitepaper)
- A distributed (endpoint per VPC) design allows least-privilege endpoint policies per VPC; a centralised endpoint has one
  policy for every spoke, which is harder to keep least-privilege, widens blast radius, and is limited to a 20,480-character
  policy document.
- Cross-Region access works by associating VPCs in each Region with the PHZ and peering the Transit Gateways (or VPC
  peering); inter-Region data transfer charges apply.
- Interface endpoints do not answer ping.

## Verify
- [ ] From a spoke VPC, the service hostname resolves to the hub endpoint's private IPs (use the FQDN from the PHZ).
- [ ] A request from the spoke to the service succeeds over Transit Gateway without a local endpoint.

## Checked
Date: 2026-11-07. Read in full: the whitepaper section "Centralized access to VPC private endpoints" (interface
endpoints, cross-Region access; the Verified Access part skimmed only as unrelated), the Route 53 cross-account
association page, and "Access an AWS service using an interface VPC endpoint" (prerequisites, console procedure, shared
subnets, ICMP). CLI flags checked with check_commands and the botocore EC2 model (`PrivateDnsEnabled`).
Removed because none of these pages state them: the "50 VPCs x 15 services x 3 AZs" arithmetic, the list of services
to centralise versus keep local, the claim that S3 gateway endpoints cannot cross Transit Gateway, the SSM hostname
trio, the Route 53 Profiles via RAM alternative, and the `dig`, SSM-agent and cost-dashboard verify steps.
Method: documentation only; no commands were run.
