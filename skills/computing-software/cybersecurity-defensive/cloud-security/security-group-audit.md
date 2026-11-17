---
id: computing-software.cybersecurity-defensive.cloud-security.security-group-audit
name: security-group-audit
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-network-security, security-group-audit, aws-security-groups, nsg, firewall-rules, open-to-internet, 0-0-0-0-0, unused-rules, vpc-reachability-analyzer]
level: practitioner
status: draft
description: "Audit cloud security groups and NSGs: find internet-exposed admin ports, overly broad rules and unused groups, verify reachability, and fix with IaC."
sources: ["CIS AWS Foundations Benchmark (security group controls)", "CIS Microsoft Azure Foundations Benchmark (NSG rules)", "AWS Docs - VPC Reachability Analyzer and Network Access Analyzer"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security group and NSG audit

**Goal:** no cloud workload is reachable from the internet or other networks except on the
ports and sources it needs.

## Find exposure
AWS CLI - rules open to the world:
```
aws ec2 describe-security-groups --query \
 "SecurityGroups[?IpPermissions[?IpRanges[?CidrIp=='0.0.0.0/0'] || Ipv6Ranges[?CidrIpv6=='::/0']]].[GroupId,GroupName]" --output table
```
Focus: 22, 3389, 3306, 5432, 1433, 6379, 9200, 27017, 2375/2376 (Docker), 6443 (Kubernetes API), any "all traffic" rule.
Azure: `az network nsg list` then rules with `sourceAddressPrefix` `*`/`Internet`/`0.0.0.0/0`;
Azure Policy / Defender for Cloud recommendation "Management ports should be closed".
GCP: firewall rules with `0.0.0.0/0` source (`gcloud compute firewall-rules list --filter="sourceRanges:0.0.0.0/0"`).
CSPM (Security Hub EC2.19 etc., Prowler) report the same continuously.

## Verify actual reachability
A security group may be open while no public IP or route exists, or closed while a load balancer
exposes the service. Use AWS **Network Access Analyzer** (paths from the internet gateway to
resources) and **Reachability Analyzer**; Azure Network Watcher "effective security rules";
external scans of your public IP ranges.

## Hygiene
- Reference security groups instead of CIDRs for internal tiers (`sg-web` -> `sg-app`).
- Unused groups (not attached to ENIs) and rules with no hits (VPC flow logs) - remove.
- Admin access via SSM Session Manager / Azure Bastion / IAP instead of open 22/3389.
- Manage all rules in IaC (Terraform), with policy-as-code checks blocking 0.0.0.0/0 on admin ports in PRs.

## Gotchas
- Default security group with permissive rules gets used by accident; strip its rules (CIS control).
- IPv6 rules (`::/0`) are often forgotten.
- Console hotfixes cause drift from IaC; detect drift.

## Verify
- [ ] Zero admin ports open to 0.0.0.0/0 or ::/0 across all accounts (CSPM report).
- [ ] External scan of public ranges matches the approved exposure list.
