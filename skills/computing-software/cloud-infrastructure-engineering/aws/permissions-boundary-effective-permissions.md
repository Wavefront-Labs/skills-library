---
id: computing-software.cloud-infrastructure-engineering.aws.permissions-boundary-effective-permissions
name: permissions-boundary-effective-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, permissions-boundary, boundary-policy-design, effective-permissions, iam, policy-evaluation]
level: advanced
status: docs-checked
description: "Write a permissions boundary and reason about effective permissions as the intersection of identity policy, boundary, SCP and session policies."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissions boundary design and effective permissions

## 1. The intersection
Effective allow = identity-based policy ∩ permissions boundary ∩ SCPs/RCPs ∩ session policy.
Any explicit `Deny` anywhere wins. A boundary never grants anything by itself.

Resource-based policies are the exception within one account: if the resource policy names the
**IAM user ARN or the role session ARN** directly, an implicit deny in the boundary does not limit it.
If it names the **role ARN**, the boundary does limit the session. Explicit denies in the boundary
always apply.

## 2. Boundary shape
```json
{"Version":"2012-10-17","Statement":[
 {"Sid":"Ceiling","Effect":"Allow","Action":["s3:*","dynamodb:*","logs:*","sqs:*","cloudwatch:*"],"Resource":"*"},
 {"Sid":"NoBoundaryEscape","Effect":"Deny","Action":["iam:DeleteRolePermissionsBoundary","iam:DeleteUserPermissionsBoundary",
   "iam:PutRolePermissionsBoundary","iam:PutUserPermissionsBoundary"],"Resource":"*"},
 {"Sid":"NoEditingBoundary","Effect":"Deny","Action":["iam:CreatePolicyVersion","iam:DeletePolicy","iam:SetDefaultPolicyVersion"],
   "Resource":"arn:aws:iam::<ACCOUNT_ID>:policy/AppBoundary"}]}
```
Keep the ceiling as an allow list of services, not `*` with denies: easier to reason about.

## 3. Working out "why denied"
1. Identity policy allows? (`simulate-principal-policy`)
2. Boundary allows? Simulate with the boundary supplied:
```bash
aws iam simulate-custom-policy --policy-input-list file://identity.json \
  --permissions-boundary-policy-input-list file://boundary.json \
  --action-names s3:PutObject --resource-arns arn:aws:s3:::bucket/key
```
3. SCP/RCP allows? (check OU chain)
4. Session policy passed at AssumeRole?
`EvalDecisionDetails`, `PermissionsBoundaryDecisionDetail` and `OrganizationsDecisionDetail` in the output show which layer said no.

## Gotchas
- The boundary attaches to an IAM user or role, not a group.

## Verify
- [ ] An action outside the ceiling is denied even when the identity policy is `*:*`.
- [ ] The role cannot remove or rewrite its own boundary.

## Checked

Checked 2026-10-27 against the IAM User Guide pages "Permissions boundaries for IAM entities" and "Policy evaluation logic", and the botocore iam model:
- Effective permissions are the intersection of the identity-based policy, boundary, SCP and session policy; an explicit deny anywhere overrides an allow.
- Resource-based policies naming an IAM user ARN or a role session ARN are not limited by an implicit deny in the boundary (same account); one naming the role ARN is limited. A federated user session behaves like a session ARN.
- The operations in the boundary example exist; `simulate-custom-policy` takes `--permissions-boundary-policy-input-list`; the decision-detail fields exist in the response model.
Removed: the statement about service-linked roles and service-created roles, which these pages do not cover. The commands were not run.

Method: documentation only; no commands were run.
