---
id: computing-software.cloud-infrastructure-engineering.aws.scp-size-limits-and-consolidation
name: scp-size-limits-and-consolidation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, scp, scp-size-limit, scp-quota, service-control-policies, organizations]
level: advanced
status: docs-checked
description: "Stay inside SCP limits (10,240 characters per policy, ten SCPs per target) by minifying, merging statements and using wildcards without weakening guardrails."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_syntax.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCP size limits and consolidation

## 1. The limits that bite
| Limit | Value |
|---|---|
| Max SCP document size | 10,240 characters (console removes extra whitespace; CLI and SDK do not) |
| SCPs attached directly to one root, OU or account | 10, minimum 1 (FullAWSAccess counts) |
| OU nesting depth | 5 levels under root |
Check usage:
```bash
aws organizations list-policies-for-target --target-id ou-abcd-1234 --filter SERVICE_CONTROL_POLICY
aws organizations describe-policy --policy-id p-xxxx --query 'Policy.Content' --output text | wc -c
```
On overflow the Organizations API returns `ConstraintViolationException` with a reason such as `POLICY_CONTENT_LIMIT_EXCEEDED` (size) or `MAX_POLICY_TYPE_ATTACHMENT_LIMIT_EXCEEDED` (attachments).

## 2. Shrink before you split
1. **Minify.** Whitespace counts when you submit via CLI/IaC. `jq -c . scp.json > scp.min.json`.
2. **Drop `Sid`** values or make them short.
3. **Merge statements** that share Effect, Resource and Condition into one Action list.
4. **Wildcards with care:** `"ec2:*VpcPeering*"`, `"iam:*Role*"` cover families. Check what a wildcard
   expands to (the IAM service authorization reference) so you do not deny an action you need.
5. **NotAction for exemption lists** (region deny): one `Deny` + `NotAction` of global services
   replaces many per-service statements.
6. **Move exemptions into conditions**: one `ArnNotLike aws:PrincipalArn` list per statement instead
   of duplicated statements per role.

## 3. Then restructure
- Put org-wide guardrails at root, environment-specific ones at OU level: spreads policies across
  the per-target attachment limit while inheritance still applies them all.
- Replace FullAWSAccess at an OU with an allow-list SCP only when you mean to.
- Use declarative policies, RCPs or tag policies for controls that are not about actions.

## Gotchas
- A policy that minifies under the limit can still be unreadable; keep the pretty source in Git and generate the minified form in CI.
- Changing a shared SCP affects every target at once; stage on a test OU first.

## Verify
- [ ] CI check fails if `jq -c` output exceeds about 9,500 characters (headroom).
- [ ] A test account confirms denied and exempted actions behave as before the merge.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide pages on quotas and service limits, SCP syntax and Service control policies, and the botocore organizations model:
- SCP size 10,240 characters; the console strips extra whitespace and the CLI and SDK keep it; 10 SCPs directly attached per root, OU or account with a minimum of 1; 5 OU levels. The earlier values (5,120 characters, 5 SCPs) were wrong.
- `ConstraintViolationException` reasons `POLICY_CONTENT_LIMIT_EXCEEDED` and `MAX_POLICY_TYPE_ATTACHMENT_LIMIT_EXCEEDED` exist in the model; the exception names used before are not Organizations error names.
- `Action` and `NotAction` support `*` and `?` wildcards; NotAction and NotResource are available with Allow and Deny.
The commands were not run.

Method: documentation only; no commands were run.
