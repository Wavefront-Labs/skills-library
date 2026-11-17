---
id: computing-software.cloud-infrastructure-engineering.aws.security-group-audit-open-and-unused
name: security-group-audit-open-and-unused
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, security-group-audit, unused-security-groups, open-ports-audit, aws-config, firewall-manager, security-hub]
level: practitioner
status: docs-checked
description: "Audit security groups for 0.0.0.0/0 exposure and dead groups: Config rules, Security Hub controls, Firewall Manager audit policies, CLI queries and safe cleanup."
sources: ["https://docs.aws.amazon.com/config/latest/developerguide/restricted-common-ports.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/ec2-controls.html", "https://docs.aws.amazon.com/waf/latest/developerguide/security-group-policies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing open and unused security groups

## 1. Find world-open ingress now
```bash
aws ec2 describe-security-group-rules \
  --filters Name=is-egress,Values=false \
  --query 'SecurityGroupRules[?CidrIpv4==`0.0.0.0/0` || CidrIpv6==`::/0`].[GroupId,IpProtocol,FromPort,ToPort]' --output table
```
Priority: 22, 3389, database ports and `-1` (all
traffic) open to the world. 443/80 on internet-facing load balancers is expected.

## 2. Continuous detection
- **Config managed rule** `restricted-common-ports` (identifier `RESTRICTED_INCOMING_TRAFFIC`;
  parameters `blockedPort1` to `blockedPort5`, optional `blockedPorts`).
- **Security Hub** controls: EC2.2 (default SGs allow no inbound or outbound traffic), EC2.13 and
  EC2.14 (no 0.0.0.0/0 or ::/0 to port 22 / 3389), EC2.18 (unrestricted incoming traffic only
  for authorized ports), EC2.19 (no unrestricted access to high-risk ports), EC2.22 (remove
  unused SGs).
- **Firewall Manager** security group policies: *content audit* policies locate and remediate
  noncompliant rules; *usage audit* policies clean up unused and redundant SGs; *common*
  policies apply shared SGs to accounts and resources. Start with automatic remediation
  disabled and review the policy details first.
- **Network Access Analyzer** scopes (`MatchPaths`, `ExcludePaths`) with an internet gateway as
  source and network interfaces as destination show what is reachable, not just configured.

## 3. Find unused groups
```bash
# SGs attached to any ENI
aws ec2 describe-network-interfaces --query 'NetworkInterfaces[].Groups[].GroupId' --output text | tr '\t' '\n' | sort -u > used.txt
aws ec2 describe-security-groups --query 'SecurityGroups[?GroupName!=`default`].GroupId' --output text | tr '\t' '\n' | sort -u > all.txt
comm -23 all.txt used.txt   # candidates
```
Before deleting, check the candidate is not referenced by other SGs' rules
(`ReferencedGroupInfo` in `describe-security-group-rules` output, or
`describe-security-group-references --group-id <SG_ID>`), launch templates, or IaC.

## 4. Fixing safely
- Look at VPC flow logs for the ENIs: which sources actually used the open port over a window you choose.
- Replace 0.0.0.0/0 SSH with SSM Session Manager (no inbound rule at all) or EC2 Instance Connect Endpoint.
- Change via IaC; tag SGs with owner so findings route to a team.

## Gotchas
- EC2.2 expects the default SG to have no inbound or outbound rules.
- The ENI query covers every service that attaches SGs to network interfaces, not only instances.
- If a Firewall Manager policy uses automatic remediation, tag SGs managed elsewhere and exclude them from the policy scope to avoid conflicting remediation cycles.

## Verify
- [ ] Config/Security Hub show zero failing resources for SSH/RDP and high-risk ports.
- [ ] Unused SG list reviewed with owners; deletions done via IaC, no deploy failures after.
- [ ] A Network Access Analyzer scope for internet-to-ENI paths returns no unexpected findings.

## Checked
2026-10-28. Confirmed against the Security Hub EC2 controls page (EC2.2, EC2.13, EC2.14, EC2.18, EC2.19, EC2.22 titles), the Config page for restricted-common-ports (identifier and parameters), the Firewall Manager security group policies page (audit, usage audit, common policies; remediation advice), the Network Access Analyzer overview (scopes, MatchPaths, ExcludePaths, internet gateway resource type) and botocore ec2 (DescribeSecurityGroupRules, SecurityGroupRule members, DescribeSecurityGroupReferences). Removed unconfirmed claims: the other Config rule names and identifiers, the filter name referenced-group-info.group-id, the 30-day window, "policies can remove SGs", the Access Analyzer reference, and the default-SG and launch-template gotchas.
Method: documentation only; no commands were run.
