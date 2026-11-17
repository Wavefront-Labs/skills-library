---
id: computing-software.cybersecurity-defensive.cloud-security.iam-permission-boundaries
name: iam-permission-boundaries
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, permission-boundaries, delegated-administration, iam-passrole, privilege-escalation-prevention, aws-iam]
level: advanced
status: docs-checked
description: "Use AWS IAM permission boundaries to let teams create roles safely: design the boundary, require it via conditions on iam:CreateRole, and block privilege escalation paths."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM permission boundaries

**Goal:** developers can create IAM roles for their workloads, but those roles can never exceed a maximum permission set you define.

## How it works
Effective permissions are the intersection of the identity policy and the permission boundary; an explicit deny in either overrides an allow. A boundary grants nothing on its own.

## Design the boundary (`DevBoundary`)
- Allow the services teams use (scoped by Region/resource tags as needed).
- Deny IAM actions that could escape: modifying or deleting the boundary policy, removing boundaries from roles, creating users/access keys, changing other teams' roles.
- Deny access to security tooling (CloudTrail, GuardDuty, Config changes).

## Enforce the boundary on delegated admins
Developer role policy:
```json
{"Effect":"Allow","Action":["iam:CreateRole","iam:PutRolePermissionsBoundary","iam:AttachRolePolicy","iam:PutRolePolicy","iam:DetachRolePolicy","iam:DeleteRolePolicy"],
 "Resource":"arn:aws:iam::111122223333:role/app/*",
 "Condition":{"StringEquals":{"iam:PermissionsBoundary":"arn:aws:iam::111122223333:policy/DevBoundary"}}},
{"Effect":"Deny","Action":["iam:DeleteRolePermissionsBoundary","iam:CreatePolicyVersion","iam:DeletePolicy","iam:SetDefaultPolicyVersion"],
 "Resource":["arn:aws:iam::111122223333:policy/DevBoundary","arn:aws:iam::111122223333:role/*"]},
{"Effect":"Allow","Action":"iam:PassRole","Resource":"arn:aws:iam::111122223333:role/app/*"}
```
- Path-scope (`/app/`) delegated roles so they cannot touch admin roles.
- Restrict `iam:PassRole` to the delegated path so developers cannot pass admin roles to EC2/Lambda.

## Escalation paths to close
Creating roles without a boundary, editing the boundary policy itself (new version), `iam:UpdateAssumeRolePolicy` on privileged roles, passing privileged roles, attaching `AdministratorAccess` (allowed by identity policy but capped by boundary - fine), creating access keys for other users. Test with tools like PMapper or Cloudsplaining.

## Checked

2026-10-28: confirmed against the IAM "Permissions boundaries for IAM entities" page: the intersection rule, explicit deny precedence, the `iam:PermissionsBoundary` condition key on role-creation actions, and the example where a boundary without iam:CreateUser blocks that action. Removed: the claim that SCPs and session policies are part of the same intersection (not on that page).

Method: documentation only; no commands were run.

## Verify
- [ ] Developer attempt to create a role without the boundary is denied.
- [ ] Role created with boundary cannot perform `iam:CreateUser` even with AdministratorAccess attached.
