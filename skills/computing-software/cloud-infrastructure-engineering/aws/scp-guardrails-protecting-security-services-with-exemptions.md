---
id: computing-software.cloud-infrastructure-engineering.aws.scp-guardrails-protecting-security-services-with-exemptions
name: scp-guardrails-protecting-security-services-with-exemptions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, scp, protect-security-services, guardrail-scp, break-glass-role, scp-exemption, organizations, cloudtrail, guardduty]
level: advanced
status: docs-checked
description: "Write SCPs that stop member accounts disabling CloudTrail, GuardDuty, Config and Security Hub, with exemptions for break-glass and pipeline roles via aws:PrincipalArn."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/controltower/latest/controlreference/mandatory-controls.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCP guardrails for security services, with exemptions

**Goal:** no one in a member account, including its local administrators, can turn off
the organization's detective controls; a small set of named automation and break-glass
roles can still manage them.

## 1. The guardrail SCP
```json
{"Version": "2012-10-17",
 "Statement": [
  {"Sid": "ProtectCloudTrail", "Effect": "Deny",
   "Action": ["cloudtrail:StopLogging", "cloudtrail:DeleteTrail", "cloudtrail:UpdateTrail",
              "cloudtrail:PutEventSelectors", "cloudtrail:PutInsightSelectors",
              "cloudtrail:DeleteEventDataStore"],
   "Resource": "*",
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": [
     "arn:aws:iam::*:role/OrgSecurityAutomation",
     "arn:aws:iam::*:role/AWSControlTowerExecution",
     "arn:aws:iam::*:role/BreakGlassAdmin"]}}},
  {"Sid": "ProtectGuardDuty", "Effect": "Deny",
   "Action": ["guardduty:DeleteDetector", "guardduty:DisassociateFromMasterAccount",
              "guardduty:DisassociateFromAdministratorAccount", "guardduty:UpdateDetector",
              "guardduty:DeleteMembers", "guardduty:StopMonitoringMembers",
              "guardduty:CreateFilter", "guardduty:UpdateFilter",
              "guardduty:DeleteIPSet", "guardduty:DeleteThreatIntelSet"],
   "Resource": "*",
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": ["arn:aws:iam::*:role/OrgSecurityAutomation", "arn:aws:iam::*:role/BreakGlassAdmin"]}}},
  {"Sid": "ProtectConfig", "Effect": "Deny",
   "Action": ["config:StopConfigurationRecorder", "config:DeleteConfigurationRecorder",
              "config:DeleteDeliveryChannel", "config:PutConfigurationRecorder",
              "config:DeleteConfigRule", "config:DeleteConformancePack",
              "config:DeleteRetentionConfiguration"],
   "Resource": "*",
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": ["arn:aws:iam::*:role/OrgSecurityAutomation", "arn:aws:iam::*:role/AWSControlTowerExecution", "arn:aws:iam::*:role/BreakGlassAdmin"]}}},
  {"Sid": "ProtectSecurityHubAccessAnalyzerMacie", "Effect": "Deny",
   "Action": ["securityhub:DisableSecurityHub", "securityhub:DisassociateFromAdministratorAccount",
              "securityhub:DeleteMembers", "securityhub:BatchDisableStandards",
              "access-analyzer:DeleteAnalyzer", "macie2:DisableMacie",
              "inspector2:Disable"],
   "Resource": "*",
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": ["arn:aws:iam::*:role/OrgSecurityAutomation", "arn:aws:iam::*:role/BreakGlassAdmin"]}}},
  {"Sid": "ProtectExemptRoles", "Effect": "Deny",
   "Action": ["iam:AttachRolePolicy", "iam:DetachRolePolicy", "iam:PutRolePolicy",
              "iam:DeleteRolePolicy", "iam:UpdateAssumeRolePolicy", "iam:DeleteRole",
              "iam:UpdateRole", "iam:TagRole", "iam:UntagRole"],
   "Resource": ["arn:aws:iam::*:role/OrgSecurityAutomation", "arn:aws:iam::*:role/BreakGlassAdmin"],
   "Condition": {"ArnNotLike": {"aws:PrincipalArn": ["arn:aws:iam::*:role/OrgSecurityAutomation", "arn:aws:iam::*:role/AWSControlTowerExecution"]}}}
 ]}
```

## 2. Why `aws:PrincipalArn` with `ArnNotLike`
- For IAM roles the request context holds the **role ARN**, not the session ARN, so one entry
  matches every session of the role; the IAM documentation says not to put the assumed-role
  session ARN in this key.
- AWS recommends ARN condition operators (`ArnLike`, `ArnNotLike`) rather than string operators
  when comparing ARNs.
- The last statement is essential: without it, a local admin can rewrite the exempt
  role's trust policy and assume it, bypassing the guardrail.
- Exempt roles should be deployed by StackSets from the management account and trust
  only principals in the security/tooling account.

## 3. Rollout
1. Check the size budget: SCPs are limited to 10,240 characters each and 10 attached per
   target. The console strips extra whitespace; if you save through the CLI or SDK, minify
   (`jq -c`) because whitespace counts.
2. Attach to a test OU first, run the security automation pipeline end to end
   (GuardDuty member enablement, Config conformance packs, trail updates) to confirm the
   exempt roles are complete.
3. Control Tower: its mandatory controls already protect CT-managed resources, and the SCP
   artifacts in the Control Tower controls reference exempt `AWSControlTowerExecution`; do not
   duplicate statements CT owns, and exempt that role in yours.
4. Attach at the root or top-level OUs (never affects the management account).

## 4. Diagnosing denials
An SCP denial message reads `... with an explicit deny in a service control policy` (the
documented example also names the policy ARN). Search CloudTrail for that message by role and
action, and test with a real session in a sandbox account.

## Gotchas
- `guardduty:UpdateDetector` is also used to enable features; your automation role must
  be exempt or plan features centrally from the delegated admin.
- New services (e.g. a new protection plan API) are not covered until you add their
  disable actions; review quarterly against the service authorization reference.
- Exempting by tag (`aws:PrincipalTag/role-type`) is weaker unless tagging roles is
  itself denied to non-admins.

## Verify
- [ ] From a member-account admin session, `aws cloudtrail stop-logging --name org-trail` and `aws guardduty delete-detector` fail with an SCP explicit deny.
- [ ] The same calls from `OrgSecurityAutomation` succeed in a sandbox account.
- [ ] A member admin cannot `iam:UpdateAssumeRolePolicy` on the exempt roles.
- [ ] Policy size within 10,240 characters; Control Tower landing zone update still succeeds.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide pages on SCP examples, quotas and Service control policies, the IAM User Guide page on global condition keys, the IAM troubleshooting page, the Control Tower mandatory controls reference and the botocore models for CloudTrail, GuardDuty, Config, Security Hub, Access Analyzer, Macie and Inspector:
- Every API operation named in the SCP exists in its service model (IAM action names are the operation names); `guardduty:UpdateDetector` accepts `Features`.
- `aws:PrincipalArn` returns the role ARN for role sessions and AWS recommends ARN operators.
- Control Tower SCP artifacts exempt `AWSControlTowerExecution`.
- SCP quotas: 10,240 characters and 10 attached SCPs per target (the old 5,120 and 5 were wrong).
Removed: the claim about the policy simulator. The commands were not run.

Method: documentation only; no commands were run.
