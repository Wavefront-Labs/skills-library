---
id: computing-software.cybersecurity-defensive.cloud-security.iam-privilege-escalation-review
name: iam-privilege-escalation-review
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, iam-privilege-escalation, iam-passrole, pmapper, cloudsplaining, policy-review, aws-iam]
level: advanced
status: draft
description: "Review AWS IAM for privilege escalation paths: dangerous permission combinations (PassRole, CreatePolicyVersion, UpdateAssumeRolePolicy), graph tools like PMapper, and fixes."
sources: ["https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/", "https://github.com/nccgroup/PMapper", "https://github.com/salesforce/cloudsplaining"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IAM privilege escalation review

A principal that is "not admin" can often make itself admin through one or two permissions.

## Dangerous permissions (on `Resource: *` or broad resources)
- **Policy manipulation**: `iam:CreatePolicyVersion` (+ set default), `iam:SetDefaultPolicyVersion`,
  `iam:AttachUserPolicy`/`AttachRolePolicy`/`AttachGroupPolicy`, `iam:PutUserPolicy`/`PutRolePolicy`/`PutGroupPolicy`.
- **Credentials for others**: `iam:CreateAccessKey`, `iam:CreateLoginProfile`, `iam:UpdateLoginProfile` on other users.
- **Group membership**: `iam:AddUserToGroup`.
- **Role trust**: `iam:UpdateAssumeRolePolicy` (make a powerful role assumable by yourself).
- **PassRole combos**: `iam:PassRole` on a privileged role + `ec2:RunInstances`, `lambda:CreateFunction` +
  `lambda:InvokeFunction`, `glue:CreateDevEndpoint`, `cloudformation:CreateStack`, `datapipeline:*`,
  `ecs:RunTask`, `sagemaker:CreateNotebookInstance`: run code as the passed role.
- **Code update of existing privileged compute**: `lambda:UpdateFunctionCode` on a function with an
  admin role; `ssm:SendCommand`/`ssm:StartSession` on instances with powerful instance profiles.
- **Permission boundary removal**: `iam:DeleteUserPermissionsBoundary`/`DeleteRolePermissionsBoundary`.

## Tools
- **PMapper** (NCC Group): builds a graph of who can become whom; `pmapper graph create`,
  `pmapper query 'preset privesc *'`, `pmapper query "who can do iam:CreateAccessKey with *"`.
- **Cloudsplaining**: flags policies allowing privilege escalation, data exfiltration, resource exposure.
- IAM Access Analyzer policy validation and custom policy checks (`check-no-new-access`, `check-access-not-granted`)
  in CI to block dangerous actions in new policies.
- CSPM/CIEM products compute effective permissions across accounts.

## Fixes
- Scope `iam:PassRole` to specific role ARNs and add `iam:PassedToService` condition.
- Remove IAM write permissions from non-admin roles; delegate role creation with permission boundaries
  (`iam:PermissionsBoundary` condition required on CreateRole).
- SCPs denying IAM changes outside a platform role; protect security roles and boundaries from modification.
- Separate deploy roles from runtime roles.

## Detect
CloudTrail alerts on `CreatePolicyVersion` with `setAsDefault`, `AttachUserPolicy` of
`AdministratorAccess`, `UpdateAssumeRolePolicy`, `CreateAccessKey` for another user, especially by
non-admin principals.

## Gotchas
- Resource `*` hides escalation; check what roles exist that could be passed.
- Cross-account paths: a role in account A trusted by account B's role chain.

## Verify
PMapper reports no path from non-admin principals to admin (except documented platform roles), and CI
policy checks fail on a test policy containing `iam:PassRole` with `Resource: *`.
