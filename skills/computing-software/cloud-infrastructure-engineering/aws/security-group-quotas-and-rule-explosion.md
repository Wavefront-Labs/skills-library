---
id: computing-software.cloud-infrastructure-engineering.aws.security-group-quotas-and-rule-explosion
name: security-group-quotas-and-rule-explosion
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, security-group-quotas, rules-per-group, sg-limits, service-quotas, prefix-lists, eni]
level: practitioner
status: docs-checked
description: "Stay inside security group quotas: rules per group times groups per ENI, how prefix lists count, consolidating CIDR rules, and raising limits without hurting performance."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html", "https://docs.aws.amazon.com/vpc/latest/userguide/managed-prefix-lists.html", "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/errors-overview.html", "https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security group quotas and rule explosion

**Symptom:** `RulesPerSecurityGroupLimitExceeded` or `SecurityGroupsPerInterfaceLimitExceeded`
during a deploy, usually after someone added "just one more IP".

## 1. The quotas that interact
| Quota (per region) | Default |
|---|---|
| Inbound rules per SG | 60 |
| Outbound rules per SG | 60 (counted separately; IPv4 and IPv6 also counted separately) |
| Security groups per network interface | 5 (adjustable up to 16) |
| Security groups per Region | 2,500 |
**Constraint:** rules-per-SG × SGs-per-ENI must not exceed **1,000**. Raising one may
require lowering the other.
A quota change applies to both inbound and outbound rules. Find the codes from the list output
(`aws service-quotas list-service-quotas --service-code <VPC_SERVICE_CODE>`) and read one with
`aws service-quotas get-service-quota --service-code <VPC_SERVICE_CODE> --quota-code <QUOTA_CODE>`.

## 2. Count what you have
```bash
aws ec2 describe-security-group-rules --filters Name=group-id,Values=sg-123 \
  --query 'length(SecurityGroupRules[?IsEgress==`false`])'
```
Prefix list references count as the list's **max entries**: a list with 20 maximum entries referenced in one
rule counts as 20 rules. The query above counts IPv4 and IPv6 rules together; the quota is enforced separately for each.

## 3. Reduce instead of raise
- Replace per-IP rules with **SG references** (instances behind ALB → reference ALB SG).
- Aggregate CIDRs (a /22 instead of four /24s) where policy allows.
- Move partner/office ranges into a **customer-managed prefix list** with tight `max-entries`.
- Use port ranges instead of one rule per port where ports are contiguous.
- Split responsibilities: a shared "monitoring" SG + a per-app SG rather than one giant SG.
- Internet allow-lists of hundreds of IPs belong in **WAF IP sets** (ALB/CloudFront) or
  Network Firewall, not SGs.

## 4. Raising
```bash
aws service-quotas request-service-quota-increase --service-code <VPC_SERVICE_CODE> --quota-code <QUOTA_CODE> --desired-value <VALUE>
```
If you raise the rules-per-group quota, the quota for security groups per network interface may have to
come down so the product stays at or under 1,000; reducing rules is usually the better route.

## Gotchas
- A managed prefix list with a large max-entries value (for example an AWS-managed list) can use most of a 60-rule SG on its own; check its maximum entries before referencing it.
- IaC drift: rules added by hand in the console make the next deploy exceed limits; enforce
  via SCP on `ec2:AuthorizeSecurityGroupIngress` outside pipelines if this keeps happening.

## Verify
- [ ] Every SG's inbound/outbound count (including prefix-list weights) has headroom ≥ 10%.
- [ ] rules × SGs-per-ENI ≤ 1,000 for current quotas.
- [ ] After consolidation, Reachability Analyzer confirms previously allowed paths still allowed.

## Checked

Date: 2026-10-27. Sources: Amazon VPC quotas page (security groups table and prefix-list rows), EC2 API error codes page, AWS CLI describe-security-group-rules reference, Service Quotas documentation.
Confirmed: 60 rules default, enforced separately for inbound, outbound, IPv4 and IPv6; 5 groups per interface, adjustable up to 16; product of the two cannot exceed 1,000; 2,500 groups per Region; prefix list maximum entries count against rules; error codes RulesPerSecurityGroupLimitExceeded and SecurityGroupsPerInterfaceLimitExceeded exist; group-id filter and IsEgress field.
Removed: hard-coded quota codes, the "~55 weight" figure for the CloudFront prefix list, and the unsupported performance statement about large rule sets.

Method: documentation only; no commands were run.
