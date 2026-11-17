---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-quotas-and-limits
name: vpc-quotas-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc, vpc-quotas, service-quotas, security-group-limits, route-table-limits]
level: practitioner
status: docs-checked
description: "Plan around VPC quotas such as routes per route table, security groups per ENI, rules per group, CIDRs per VPC and network address usage, and raise them safely."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html", "https://docs.aws.amazon.com/vpc/latest/userguide/network-address-usage.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-limits-endpoints.html", "https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-connection-quotas.html", "https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC quotas

## 1. The ones that shape designs (defaults, as listed on 2026-10-27)
| Quota | Default | Note |
|---|---|---|
| VPCs per Region | 5 | adjustable; raising it raises internet gateways per Region by the same amount |
| Subnets per VPC | 200 | adjustable |
| IPv4 CIDR blocks per VPC | 5 | adjustable up to 50; primary and secondary blocks both count |
| IPv6 CIDR blocks per VPC | 5 | adjustable up to 50 |
| Route tables per VPC | 200 | adjustable; the main route table counts |
| Routes per route table (non-propagated) | 500 | adjustable up to 1,000; network performance might be impacted; enforced separately for IPv4 and IPv6 |
| Propagated routes per route table | 100 | **not adjustable**; if you need more prefixes, advertise a default route |
| Security groups per network interface | 5 | adjustable up to 16 |
| Inbound or outbound rules per security group | 60 | counted separately for inbound, outbound, IPv4 and IPv6; rules per SG x SGs per ENI cannot exceed 1,000 |
| Security groups per Region | 2,500 | adjustable |
| Rules per network ACL | 20 | adjustable up to 40 inbound and 40 outbound; performance might be impacted |
| Interface and Gateway Load Balancer endpoints per VPC | 50 | combined quota, adjustable (PrivateLink quotas page) |
| Gateway VPC endpoints per Region | 20 | adjustable; up to 255 gateway endpoints per VPC |
| NAT gateways per Availability Zone | 5 | counts pending, active and deleting gateways |
| Elastic IP addresses per Region | 5 | adjustable |
| Elastic IP addresses per public NAT gateway | 2 | adjustable up to 8 |
| Active VPC peering connections per VPC | 50 | adjustable up to 125 (VPC peering quotas page) |
| Network Address Usage (NAU) per VPC | 64,000 | adjustable up to 256,000 |
| Peered NAU (VPC plus intra-Region peers) | 128,000 | adjustable up to 512,000; cross-Region peers do not count |
A customer-managed prefix list referenced in a security group rule counts as its **maximum entries**, not its
current size. Default prefix-list quotas are adjustable, but a support case is needed rather than the Service Quotas console.

## 2. Check and raise
Find the VPC service code first, then list quotas and copy the quota code from the output:
```bash
aws service-quotas list-services --query 'Services[].[ServiceCode,ServiceName]' --output text
aws service-quotas list-service-quotas --service-code <VPC_SERVICE_CODE> \
  --query 'Quotas[].{n:QuotaName,v:Value,code:QuotaCode}' --output table
aws service-quotas request-service-quota-increase --service-code <VPC_SERVICE_CODE> \
  --quota-code <QUOTA_CODE> --desired-value <VALUE>
aws service-quotas list-requested-service-quota-change-history --service-code <VPC_SERVICE_CODE>
```
Look up quota codes from the list output rather than memorising them. Some quotas (for example Region-level
VPC Block Public Access exclusions) are raised through an AWS Support request instead.

## 3. Design around them
- Hitting the propagated-routes cap: advertise a default route (or fewer, summarised prefixes) from the on-premises side.
- Rule explosion: consolidate with prefix lists and SG references instead of raising the per-SG cap.
- Large NAU with many intra-Region peered VPCs: remember the peered-NAU quota covers the VPC plus all its peers.
- Even when NAU headroom exists, launches fail if the individual resource quota (ENIs, rules, routes) is exhausted.

## Verify
- [ ] `list-service-quotas` values match this table for the Region, and usage of VPCs, EIPs, NAT gateways and routes is compared against them.
- [ ] A CloudWatch alarm exists for quotas that support one (Service Quotas console) on the quotas that matter to the design.

## Checked

Date: 2026-10-27. Sources: Amazon VPC quotas page (amazon-vpc-limits.html), AWS PrivateLink quotas page, VPC peering connection quotas page, Network Address Usage page, Service Quotas User Guide, botocore Service Quotas model (ListServiceQuotas, RequestServiceQuotaIncrease, ListRequestedServiceQuotaChangeHistory).
Corrected: routes per route table is 500 (adjustable to 1,000), not 50; propagated routes are not adjustable and the documented workaround is a default route; interface endpoints are a combined quota with Gateway Load Balancer endpoints; gateway endpoints are 20 per Region (255 per VPC); peered NAU is a separate quota (128,000).
Removed: hard-coded quota code L-29B6F2EB (not found in any page), Trusted Advisor and AWS/Usage alarm claims, and the Transit Gateway "own table limits" aside.

Method: documentation only; no commands were run.
