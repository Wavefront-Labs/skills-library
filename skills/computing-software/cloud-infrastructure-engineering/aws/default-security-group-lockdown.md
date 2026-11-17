---
id: computing-software.cloud-infrastructure-engineering.aws.default-security-group-lockdown
name: default-security-group-lockdown
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, default-security-group, sg-default-lockdown, cis-benchmark, aws-config]
level: practitioner
status: docs-checked
description: "Lock down every VPC's default security group by removing its rules, keeping workloads off it, and enforcing with Config and Security Hub controls."
sources: ["https://docs.aws.amazon.com/vpc/latest/userguide/default-security-group.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/ec2-controls.html#ec2-2", "https://docs.aws.amazon.com/config/latest/developerguide/vpc-default-security-group-closed.html", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/default_security_group.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default security group lockdown

Each VPC's default SG allows all inbound from members of itself and all outbound. It cannot be deleted,
and anything launched without an explicit SG lands in it.

## 1. Strip the rules (every VPC, every Region)
```bash
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  for sg in $(aws ec2 describe-security-groups --region $r --filters Name=group-name,Values=default --query 'SecurityGroups[].GroupId' --output text); do
    in=$(aws ec2 describe-security-group-rules --region $r --filters Name=group-id,Values=$sg --query 'SecurityGroupRules[?!IsEgress].SecurityGroupRuleId' --output text)
    out=$(aws ec2 describe-security-group-rules --region $r --filters Name=group-id,Values=$sg --query 'SecurityGroupRules[?IsEgress].SecurityGroupRuleId' --output text)
    [ -n "$in" ] && aws ec2 revoke-security-group-ingress --region $r --group-id $sg --security-group-rule-ids $in
    [ -n "$out" ] && aws ec2 revoke-security-group-egress --region $r --group-id $sg --security-group-rule-ids $out
  done
done
```

## 2. Before you strip: find users
```bash
aws ec2 describe-network-interfaces --filters Name=group-id,Values=<DEFAULT_SG> \
  --query 'NetworkInterfaces[].{eni:NetworkInterfaceId,desc:Description,type:InterfaceType}'
```
Move those ENIs to purpose-built SGs first; resources created without an explicit SG are associated with the default one.

## 3. Enforce
- Config managed rule `vpc-default-security-group-closed`; Security Hub control EC2.2.
- IaC: Terraform `aws_default_security_group` adopts the default SG and immediately removes all its
  ingress and egress rules, then creates only the rules in the configuration (none = empty). For other
  IaC tools, use the script above.
- New accounts: run the cleanup from the account vending pipeline.

## Verify
- [ ] `describe-security-group-rules` for every default SG returns nothing.
- [ ] Config rule compliant in all Regions.

## Checked

Checked 2026-10-28 against the VPC User Guide (default security groups), the AWS Config rule page, Security Hub control EC2.2, the Terraform AWS provider docs and the EC2 API model.
- Confirmed: default SG allows inbound from itself and all outbound, cannot be deleted, resources without an SG land in it, `vpc-default-security-group-closed` (NON_COMPLIANT if any inbound or outbound rule), Security Hub EC2.2, Terraform adopt-and-empty behaviour, `SecurityGroupRuleId` and `IsEgress` fields of DescribeSecurityGroupRules.
- Removed: the claim that CloudFormation cannot manage default SG rules, and the list of services that often use the default SG.

Method: documentation only; no commands were run.
