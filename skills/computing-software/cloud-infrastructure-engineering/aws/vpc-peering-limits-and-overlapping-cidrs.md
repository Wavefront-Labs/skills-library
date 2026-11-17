---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-peering-limits-and-overlapping-cidrs
name: vpc-peering-limits-and-overlapping-cidrs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-peering, peering-non-transitive, overlapping-cidr, peering-routes, transit-gateway, network-design]
level: practitioner
status: docs-checked
description: "Set up VPC peering correctly and know its limits: non-transitive routing, no overlapping CIDRs, routes on both sides, DNS resolution options and when to move to TGW."
sources: ["https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-connection-quotas.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-routing.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC peering: limits and overlapping CIDRs

## 1. Set up
```bash
PCX=$(aws ec2 create-vpc-peering-connection --vpc-id vpc-a --peer-vpc-id vpc-b \
  --peer-owner-id <ACCOUNT_B> --peer-region eu-west-1 --query VpcPeeringConnection.VpcPeeringConnectionId --output text)
aws ec2 accept-vpc-peering-connection --region eu-west-1 --vpc-peering-connection-id $PCX   # in account B
aws ec2 create-route --route-table-id rtb-a --destination-cidr-block 10.2.0.0/16 --vpc-peering-connection-id $PCX
aws ec2 create-route --region eu-west-1 --route-table-id rtb-b --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id $PCX
aws ec2 modify-vpc-peering-connection-options --vpc-peering-connection-id $PCX \
  --requester-peering-connection-options AllowDnsResolutionFromRemoteVpc=true   # optional, see section 5
```
Routes are needed in **every** route table (both sides) whose subnets should talk.
Security groups can reference peer SGs (same region).

## 2. What peering cannot do
- **Not transitive**: A↔B and B↔C does not give A↔C. Each pair needs its own peering.
- **No edge-to-edge routing**: A cannot use B's IGW, NAT gateway, VPN, Direct Connect or
  gateway endpoints through the peering.
- **No overlapping CIDRs**: matching or overlapping IPv4 or IPv6 blocks block creation, and if any one of several IPv4 blocks overlaps you cannot peer even if you only intend to use the others.
- One peering per VPC pair at a time; 50 active peerings per VPC by default (adjustable up to 125) and 25 outstanding requests; an unaccepted request expires after 7 days.

## 3. Overlap options
1. Re-IP one side (best long-term; use IPAM to stop it recurring).
2. Expose only the needed service via **PrivateLink** or **VPC Lattice** — overlap irrelevant.
3. **Private NAT gateway** + TGW with a routable intermediate range.
4. Peering to only non-overlapping *subsets*: impossible — the whole VPC CIDR is checked.

## 4. When to move to Transit Gateway
Many VPCs needing any-to-any, need for central egress/inspection, on-prem
connectivity shared by all VPCs, or route table limits (each peering needs a route entry in every table).
Peering stays simple for a few high-volume pairs. Check current pricing for both options; this skill states none.

## Gotchas
- MTU is 9001 bytes between peered VPCs in the same Region and 8500 bytes for inter-Region peering.
- A route to a peering that is still `pending-acceptance` shows state `blackhole` and has no effect until the peering is active.
- Security group references to a peer SG work only when both VPCs are in the same Region.
- You cannot query the Amazon DNS server in a peer VPC.
- Unicast reverse path forwarding is not supported across peering; with overlapping peers, check route tables so replies do not go to the wrong VPC.
- Only VPC owners can manage peering connections; participants in a shared VPC cannot.

## 5. DNS resolution option
By default a peer instance's public DNS hostname resolves to its public IP. With DNS resolution enabled for the
peering it resolves to the private IP. Both VPCs need DNS hostnames and DNS resolution enabled, the peering must
be `active` (it cannot be set at creation), and each VPC owner sets their own side (requester options by the
requester, accepter options by the accepter). If a peer VPC's IPv4 range is outside RFC 1918, private DNS
hostnames resolve to private IPs only with this option on.

## Verify
- [ ] Peering state `active`; both route tables list the remote CIDR via `pcx-`.
- [ ] Reachability Analyzer A → B instance: reachable; A → C (via B): not reachable (as designed).
- [ ] The public DNS hostname of B's instance resolves to its private IP from A when the DNS option is enabled on both sides.

## Checked

Date: 2026-10-27. Sources: Amazon VPC Peering Guide pages "How VPC peering connections work" (limitations, MTU, edge-to-edge rules), "VPC peering connection quotas for an account", "Update your route tables", "Enable DNS resolution"; botocore EC2 model (CreateVpcPeeringConnection PeerRegion/PeerOwnerId, ModifyVpcPeeringConnectionOptions AllowDnsResolutionFromRemoteVpc).
Corrected: inter-Region peering MTU is 8500 bytes (jumbo frames supported), not 1500; the "blackhole after delete" claim was replaced by the documented pending-acceptance blackhole; the DNS option description now matches the documented requester/accepter model.
Removed: the "about 10 VPCs" threshold and the data-transfer price statements (pricing is not checkable from documentation).

Method: documentation only; no commands were run.
