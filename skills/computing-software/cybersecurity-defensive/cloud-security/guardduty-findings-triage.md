---
id: computing-software.cybersecurity-defensive.cloud-security.guardduty-findings-triage
name: guardduty-findings-triage
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-detection, guardduty-findings-triage, amazon-guardduty, finding-types, suppression-rules, cloud-incident-triage]
level: practitioner
status: docs-checked
description: "Triage Amazon GuardDuty findings by type family: validate with CloudTrail and resource context, suppress known-benign patterns safely and route high-severity findings to response."
sources: ["https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings-severity.html", "https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-ec2.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GuardDuty findings triage

**Goal:** every GuardDuty finding gets a consistent, quick determination and the noisy-but-benign ones are suppressed narrowly.

## Setup
Delegated administrator account, auto-enable for all organisation accounts and Regions, the protection plans you need (see the GuardDuty User Guide for current plan names), findings to Security Hub and EventBridge, then SIEM/SOAR.

## Severity
Critical 9.0-10.0, High 7.0-8.9, Medium 4.0-6.9, Low below that (GuardDuty severity page). Suggested handling, your policy to set: Critical and High immediately, Medium same day, Low batch review.

## Triage by family
- **Instance credential exfiltration findings** (EC2 role credentials used from outside AWS): treat as likely compromise (often SSRF). Revoke role sessions (the IAM revoke-sessions page uses an `AWSRevokeOlderSessions` inline deny keyed on `aws:TokenIssueTime`), investigate the instance.
- **Recon, Discovery and PenTest IAMUser findings** - API calls enumerating resources from unusual sources; check whether the principal is a known scanner/pen test.
- **CryptoCurrency:EC2/BitcoinTool.B!DNS**, **Impact:EC2/...** - compromised compute; isolate and snapshot.
- **Backdoor:EC2/C&CActivity.B**, **Trojan:EC2/...** - instance contacting known malicious infrastructure.
- **Root credential usage findings** - root used; verify with the account owner.
- **CloudTrail logging disabled findings** - treat as an attack until proven otherwise.
- **S3 exfiltration and discovery findings** - unusual S3 access patterns by a principal.
- **Runtime/EKS** findings - container-level, pivot to the pod and node.

## Validate
1. Who/what: principal ARN, access key, instance id, role session name in `resource` and `service.action`.
2. CloudTrail around the time: `aws cloudtrail lookup-events --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=<key>` or Athena/Lake queries; source IPs, user agents, other API calls.
3. Expected? Change tickets, known scanners, CI/CD egress IPs, VPN egress.
4. Decide: true positive -> IR runbook; benign -> suppress or archive with reason.

## Suppression
Filter-based suppression rules (e.g. `PortProbeUnprotectedPort` on intentionally public web instances tagged `public-web`), or trusted IP lists for your scanners. Never suppress whole finding types organisation-wide without resource scoping.

## Checked

2026-10-28: confirmed on the GuardDuty severity page (Critical 9.0-10.0, High 7.0-8.9, Medium 4.0-6.9) and the EC2 finding types page (CryptoCurrency:EC2/BitcoinTool.B!DNS, Impact:EC2/..., Backdoor:EC2/C&CActivity.B, Trojan:EC2/..., Recon:EC2/PortProbeUnprotectedPort); `aws:TokenIssueTime` and `AWSRevokeOlderSessions` on the IAM revoke-sessions page. Fixed: finding name C&CActivity lacked the .B suffix. Removed: finding-type name format and exact IAM/S3 finding names, protection-plan list (not read this batch).

Method: documentation only; no commands were run.

## Verify
- [ ] Generate sample findings (`aws guardduty create-sample-findings`) and confirm routing to SOC queue.
- [ ] Suppression rules reviewed quarterly with documented rationale.
