---
id: computing-software.cloud-infrastructure-engineering.aws.auto-remediating-open-security-groups
name: auto-remediating-open-security-groups
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, security-groups, open-sg-remediation, restricted-ssh, aws-config, auto-remediation]
level: practitioner
status: docs-checked
description: "Detect world-open security group ingress with AWS Config rules and attach the SSM Automation runbook AWS-DisablePublicAccessForSecurityGroup as an automatic remediation."
sources:
  - https://docs.aws.amazon.com/config/latest/developerguide/restricted-ssh.html
  - https://docs.aws.amazon.com/config/latest/developerguide/restricted-common-ports.html
  - https://docs.aws.amazon.com/config/latest/developerguide/vpc-sg-open-only-to-authorized-ports.html
  - https://docs.aws.amazon.com/config/latest/developerguide/setup-autoremediation.html
  - https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-aws-disablepublicaccessforsecuritygroup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-remediating open security groups

## Detect
| Rule | Flags |
|---|---|
| `restricted-ssh` (identifier `INCOMING_SSH_DISABLED`) | SSH ingress from `0.0.0.0/0` or `::/0` |
| `restricted-common-ports` | world-open ingress on the TCP ports you list as blocked (default 3389, RDP) |
| `vpc-sg-open-only-to-authorized-ports` | world-open ingress on ports outside your authorized list |

## Remediate with Config + SSM
1. Attach a remediation action to the Config rule (console, or `aws configservice put-remediation-configurations`); see "Setting Up Auto Remediation".
2. Choose the SSM Automation runbook `AWS-DisablePublicAccessForSecurityGroup`; read its runbook page for its input parameters and exactly which rules it revokes before enabling automatic mode.
3. Give the runbook an Automation assume role (`<ACCOUNT_ID>` role with permission to revoke security group ingress) and pass the noncompliant security group as the resource parameter.
4. Start with manual remediation, then switch to automatic once you have seen what it removes. Automatic remediation can break legitimate public rules (load balancer groups on 80/443), so scope the Config rule or tag exceptions.
- Config evaluation takes minutes. For faster response, trigger your own automation from an EventBridge rule on the CloudTrail security-group API call (design and test it yourself; event field names are in the CloudTrail event, not covered by these sources).

## Prevent
- Remove the need: use Session Manager instead of SSH from the internet.

## Verify
- [ ] Adding a `0.0.0.0/0` rule on port 22 in a sandbox is revoked (or flagged) and the owner notified.
- [ ] Load balancer security groups on 443 are untouched.

## Checked
2026-10-28. Confirmed on the AWS Config pages `restricted-ssh`, `restricted-common-ports`, `setup-autoremediation` and on the SSM runbook page for `AWS-DisablePublicAccessForSecurityGroup`: rule identifier `INCOMING_SSH_DISABLED`, `0.0.0.0/0` and `::/0` checks, default blocked port 3389, remediation setup flow; `check_commands.py` accepted the `put-remediation-configurations` operation.
Removed as unconfirmed: Security Hub control numbers, the `AWSConfigRemediation-RemoveUnrestrictedSourceIngressRules` runbook claim, the claim that the runbook revokes only 22 and 3389, the Lambda/boto3 example and CloudTrail field paths, the Firewall Manager section, VPC Block Public Access, and the remediation JSON parameter names.
Method: documentation only; no commands were run.
