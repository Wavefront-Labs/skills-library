---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-peering-dns-resolution-and-sg-references
name: vpc-peering-dns-resolution-and-sg-references
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-peering, peering-dns-resolution, peering-sg-reference, private-ip-resolution, security-groups, cross-account]
level: practitioner
status: docs-checked
description: "Make peered VPCs resolve each other's public DNS names to private IPs, reference peer security groups in rules, and know the cross-region and cross-account limits."
sources: ["https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-connection-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC peering: DNS resolution and security group references

## 1. Public DNS hostnames to private IPs
By default, an instance in VPC A resolving `ec2-203-0-113-10.eu-west-1.compute.amazonaws.com`
(the public DNS name of an instance in peered VPC B) gets the **public** IP, so traffic
leaves via the internet (or fails if B's instance has no public path). Enable resolution
on the peering:
```bash
aws ec2 modify-vpc-peering-connection-options --vpc-peering-connection-id pcx-0abc \
  --requester-peering-connection-options AllowDnsResolutionFromRemoteVpc=true \
  --accepter-peering-connection-options AllowDnsResolutionFromRemoteVpc=true
```
- The requester VPC owner modifies the requester options and the accepter VPC owner the accepter options;
  in one account you can set both at once. This works for same-Region and cross-Region peering.
- Both VPCs must be enabled for DNS hostnames and DNS resolution.
- Peering must be `active`; you cannot enable DNS resolution when you create the connection.
This affects only AWS-provided public DNS hostnames of instances. It does not share
**private hosted zones**; for that, associate the PHZ with the other VPC
(`create-vpc-association-authorization` in the zone owner account, then
`associate-vpc-with-hosted-zone` from the VPC owner account).

## 2. Referencing peer security groups
Within the **same region**, a rule can reference a security group in the peer VPC:
```bash
aws ec2 authorize-security-group-ingress --group-id sg-0dbB \
  --ip-permissions 'IpProtocol=tcp,FromPort=5432,ToPort=5432,UserIdGroupPairs=[{GroupId=sg-0appA,UserId=111122223333,VpcPeeringConnectionId=pcx-0abc}]'
```
- Cross-account (same Region): include the peer account ID with the group ID in the rule (`123456789012/sg-1a2b3c4d` in the console, `UserId` in the API group pair).
- Cross-region peering: you can't reference the peer's security group; use the peer VPC CIDR block.
- The peering connection must be `active`.
- Stale rules: if the peering is deleted or the peer SG is deleted, the rule becomes
  stale. Find them:
  `aws ec2 describe-stale-security-groups --vpc-id vpc-0B` and clean up.
- Referencing works in both inbound and outbound rules.

## 3. Other peering rules worth remembering
- No transitive routing: A-B and B-C does not give A-C; no edge-to-edge routing through a
  peer's internet gateway, NAT device, VPN, Direct Connect connection or gateway endpoint.
- Matching or overlapping IPv4 or IPv6 CIDR blocks cannot be peered, even if you intend to use only the non-overlapping ranges.
- Quotas (VPC peering quotas page, read 2026-10-27): 50 active peering connections per VPC by default (adjustable up to 125), 25 outstanding requests,
  and an unaccepted request expires after 1 week (168 hours).
- MTU: 9001 bytes between peered VPCs in the same Region, 8500 bytes for inter-Region peering.

## 4. Troubleshooting checklist
1. Routes in **both** VPCs' relevant route tables point the peer CIDR at `pcx-`.
2. SGs allow the traffic (by CIDR or peer SG reference).
3. NACLs allow it plus ephemeral returns.
4. DNS returns the private IP (`dig <peer-hostname>`).
5. Reachability Analyzer path between ENIs across the peering.

## Verify
- [ ] `dig` of a peer instance's public DNS name from VPC A returns its private IP.
- [ ] A connection using a peer-SG-referencing rule succeeds; `describe-stale-security-groups` returns empty.
- [ ] Route tables on both sides contain the peer CIDR routes.

## Checked

Checked 2026-10-27 against the Amazon VPC Peering guide (peering basics, DNS resolution, reference peer security groups, quotas) and the botocore EC2 model.
- DNS resolution behaviour, requirements (active, both VPCs with DNS hostnames and resolution, each owner sets its own side) and `modify-vpc-peering-connection-options` (`AllowDnsResolutionFromRemoteVpc`) confirmed.
- Security group references: same Region only, account-ID prefix for cross-account, stale rules and `describe-stale-security-groups` confirmed.
- No transitive peering, no edge-to-edge routing through gateways, overlapping CIDR rule, quotas (50 default, up to 125) and MTU (9001 same Region, 8500 inter-Region) confirmed.
- Removed the claims that inter-Region traffic is encrypted, that interface endpoints in a peer VPC are reachable by IP, and that peering routes count against a 50-route default, none of which a page read confirms; the earlier "no jumbo frames" statement was wrong.

Method: documentation only; no commands were run.
