---
id: computing-software.systems-network-administration.network-design.cloud-security-groups-vs-network-acls
name: cloud-security-groups-vs-network-acls
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, security-group, network-acl, aws-vpc, azure-nsg, stateful-firewall, micro-segmentation]
level: practitioner
status: docs-checked
description: "Design cloud traffic filtering with stateful security groups and stateless network ACLs (AWS) or NSGs (Azure): referencing groups, ephemeral ports and rule limits."
sources:
  - https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html
  - https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html
  - https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security groups vs network ACLs

| | AWS Security Group | AWS Network ACL | Azure NSG |
|---|---|---|---|
| Rule types | allow rules only | allow and deny rules | allow and deny, by priority |
| State | stateful (return traffic automatic) | **stateless** (return traffic must be explicitly allowed) | stateful (flow records) |
| Ordering | all rules evaluated | numbered rules, lowest number first (1 to 32766) | priority 100 to 4096, lower number first |
| Scope | instance network interfaces | subnet level | subnets (see the Azure page for NIC association) |
| Sources | CIDR, **other security groups** | CIDR | IP, CIDR, service tags, application security groups |

## Design pattern
- AWS guidance: use **security groups as the primary mechanism** for controlling network access, and network ACLs as a
  secondary, coarse layer. Security groups can reference other security groups, so one group per tier (web, app, db)
  needs no edits when IPs change.
- Keep NACLs coarse (a few deny guard rails): they are stateless, so fine-grained rules cause outages.
- Azure: an NSG on the subnet as baseline, and application security groups to group VMs by role; add a firewall or NVA
  where you need east-west inspection or egress control.

## Stateless pitfall (NACL)
Because return traffic is not automatically allowed, a NACL that admits inbound 443 also needs an outbound rule for the
clients' ephemeral ports, and the reverse for outbound calls made from the subnet. Check the ephemeral range used by
your clients' operating systems; do not assume one range.

## Limits and hygiene
- Rule counts and groups per interface are quota-limited (see the service quotas pages for current values); prefer
  managed prefix lists over many CIDR rules.
- Avoid `0.0.0.0/0` inbound except on internet-facing load balancers; never expose SSH/RDP to the internet.
- Define all rules as code and alert on drift.
- Use VPC Flow Logs (AWS) and NSG flow logs (Azure) to see what is actually allowed or rejected.

## Verify
- [ ] Intended paths verified with the cloud's reachability tooling; flow logs show no unexpected rejects.

## Checked
2026-10-28. Confirmed in the AWS VPC "Control subnet traffic with network ACLs" and "Infrastructure security" pages and
the Azure NSG overview: allow-only versus allow/deny, stateful versus stateless, NACL rule numbers 1 to 32766 lowest
first, security groups as primary mechanism and referencing other groups, flow logs, Azure priority range 100 to 4096,
service tags and application security groups. Removed as unconfirmed: the 1024-65535 ephemeral range, default quota
figures (60 and 5), NSG-on-NIC statement, SSM Session Manager, AWS Config and Azure Policy advice, named reachability
tools.
Method: documentation only; no commands were run.
