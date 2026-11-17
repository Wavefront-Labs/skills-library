---
id: computing-software.cloud-infrastructure-engineering.aws.detective-behavior-graph-investigations
name: detective-behavior-graph-investigations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, amazon-detective, detective, behavior-graph, investigation, finding-groups, guardduty, security-investigation, incident-response, iam-investigation, entity-profile, threat-hunting]
level: advanced
status: docs-checked
description: "Investigate GuardDuty and Security Hub findings with Amazon Detective: enable the behavior graph org-wide, use finding groups, entity profiles and automated IAM investigations."
sources: ["https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html", "https://docs.aws.amazon.com/detective/latest/userguide/groups-about.html", "https://docs.aws.amazon.com/detective/latest/userguide/detective-enabling.html", "https://docs.aws.amazon.com/detective/latest/userguide/detective-source-data-about.html", "https://docs.aws.amazon.com/detective/latest/userguide/investigations-about.html", "https://docs.aws.amazon.com/detective/latest/userguide/run-investigations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon Detective — behavior graphs and investigations

**Goal:** when GuardDuty says "credentials exfiltrated", the analyst answers *what else did
this principal do, from where, and which resources are involved* in minutes, from a graph
that already holds up to a year of CloudTrail, VPC Flow Logs and finding history.

## 1. Enable org-wide
Detective docs recommend aligning the Detective administrator account with the GuardDuty and Security Hub administrator.
You can enable Detective only once per Region.
```bash
# management account
aws detective enable-organization-admin-account --account-id <SECURITY_ACCOUNT_ID>
# security (admin) account, every Region you use
aws detective list-graphs                                   # graph ARN
aws detective update-organization-configuration --graph-arn <GRAPH> --auto-enable
aws detective create-members --graph-arn <GRAPH> --accounts AccountId=<ID>,EmailAddress=<EMAIL>   # pre-existing accounts
aws detective list-datasource-packages --graph-arn <GRAPH>
aws detective update-datasource-packages --graph-arn <GRAPH> --datasource-packages EKS_AUDIT ASFF_SECURITYHUB_FINDING
```
Detective pulls its core sources (such as CloudTrail management events and VPC Flow Logs)
itself. Optional packages (`EKS_AUDIT`, `ASFF_SECURITYHUB_FINDING`) add EKS audit logs and
Security Hub findings. Repeat per Region.

## 2. Triage workflow
1. Start from the finding (GuardDuty/Security Hub console → *Investigate in Detective*).
2. **Finding groups**: Detective clusters related findings, entities and tactics (MITRE
   ATT&CK mapping) into one group per probable incident. Work the group, not 40 findings.
3. **Entity profiles**: Detective visualizations show changes in the type and volume of
   activity over a selected time window, linked to GuardDuty findings. Entities include
   resources outside AWS such as IP addresses or user agents.
4. Pivot: role, role sessions, source IPs, then other principals from those IPs.

## 3. Automated investigations for IAM
```bash
aws detective start-investigation --graph-arn <GRAPH> \
  --entity-arn arn:aws:iam::<ACCOUNT_ID>:role/app-deployer \
  --scope-start-time 2026-10-14T00:00:00Z --scope-end-time 2026-10-16T00:00:00Z
aws detective get-investigation --graph-arn <GRAPH> --investigation-id <ID>
aws detective list-indicators --graph-arn <GRAPH> --investigation-id <ID>
```
Detective Investigation examines IAM users and roles using indicators of compromise
(attack tactics, impossible travel, flagged IP addresses, finding groups). Use it as the
first pass for any IAM principal named in a finding.

## Gotchas
- Detective retains data from each data source package for up to 1 year, so enabling it
  after an incident gives no history. Enable before you need it.
- Pricing is per GB ingested (see the vendor pricing page); watch usage per member account.
- Detective is for investigation; pair it with GuardDuty/Security Hub and an IR runbook.

## Verify
- [ ] `list-members` shows every org account `ENABLED` in each used Region.
- [ ] `start-investigation` on a test role completes and returns indicators.
- [ ] IR runbook step "pivot in Detective" has a named owner and was exercised in the last game day.

## Checked

2026-10-28. Confirmed against AWS documentation: 1-year retention per data source package, once-per-Region enablement, optional EKS audit and Security Hub packages, finding groups with MITRE ATT&CK-style grouping, Detective Investigation for IAM users/roles with indicators; DatasourcePackage enum via the botocore detective model.
Removed: 48-hour GuardDuty prerequisite, entity-profile metric list, scope/baseline walkthrough, generative summaries, specific indicator list items, usage-page and invitation gotchas; replaced stub source URLs.
Method: documentation only; no commands were run.
