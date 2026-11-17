---
id: computing-software.cloud-infrastructure-engineering.aws.iam-permissions-boundary-delegated-admin
name: iam-permissions-boundary-delegated-admin
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, permissions-boundary, permission-boundaries, delegated-iam-admin, boundary-delegation, boundary-enforcement, privilege-escalation, iam-createrole, iam-permissionsboundary, passrole, least-privilege]
level: advanced
status: docs-checked
description: "Let teams create their own IAM roles safely: a permissions boundary plus a delegate policy that forces it on every role, blocks its removal and stops privilege escalation."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/aws-iam/lib/permissions-boundary.ts", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/iam_role.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissions boundaries for delegated IAM administration

**Goal:** application teams (or their pipelines) can create roles and policies for their own
Lambdas and tasks without a ticket, and nothing they create can ever exceed a ceiling the
platform team owns. The boundary is the ceiling; the *delegate policy* is what makes the
ceiling unavoidable.

## 1. How the boundary bites
A permissions boundary sets the maximum permissions an identity-based policy can grant to a user or role: the
effective permissions are the intersection of the identity-based policies and the boundary, and an explicit deny in
either overrides an allow. A boundary never grants anything. SCPs and session policies intersect in the same way.
How resource-based policies interact (same account):
- A resource policy granting to an **IAM role ARN** is limited by an implicit deny in the role's boundary or session policy.
- A resource policy granting to an **IAM user ARN**, or directly to an **assumed-role session ARN**, is not limited
  by an implicit deny in the boundary (the Secrets Manager example in the guide: a resource policy allow still works
  because the boundary has no explicit deny). An explicit deny in the boundary still wins.
So the boundary caps what a role can do through its own identity policies, which is the escalation path you care about.

## 2. The three policies
1. **Boundary** (`arn:aws:iam::<ACCOUNT_ID>:policy/boundary/app-boundary`): the ceiling for
   any role a team creates: their service actions on their resources, no IAM writes,
   no Organizations/account APIs, no touching the platform's roles.
2. **Delegate policy**: attached to the team's deployer role (CI) or SSO permission set.
3. **The deployer role itself** should also carry a boundary, so it cannot use its own
   power directly beyond the ceiling.
Delegate policy core (tighten resource ARNs to a path such as `/app/`); this follows the pattern in the IAM
guide's delegation example, applied to roles:
```json
{"Version":"2012-10-17","Statement":[
 {"Sid":"CreateOrChangeOnlyWithBoundary","Effect":"Allow",
  "Action":["iam:CreateRole","iam:PutRolePolicy","iam:AttachRolePolicy","iam:DetachRolePolicy",
            "iam:DeleteRolePolicy","iam:PutRolePermissionsBoundary"],
  "Resource":"arn:aws:iam::<ACCOUNT_ID>:role/app/*",
  "Condition":{"StringEquals":{"iam:PermissionsBoundary":"arn:aws:iam::<ACCOUNT_ID>:policy/boundary/app-boundary"}}},
 {"Sid":"ManageOwnPolicies","Effect":"Allow",
  "Action":["iam:CreatePolicy","iam:CreatePolicyVersion","iam:DeletePolicy","iam:DeletePolicyVersion","iam:SetDefaultPolicyVersion"],
  "Resource":"arn:aws:iam::<ACCOUNT_ID>:policy/app/*"},
 {"Sid":"ReadAndCleanup","Effect":"Allow",
  "Action":["iam:Get*","iam:List*","iam:DeleteRole","iam:TagRole","iam:UntagRole","iam:UpdateAssumeRolePolicy"],
  "Resource":"arn:aws:iam::<ACCOUNT_ID>:role/app/*"},
 {"Sid":"PassOnlyAppRoles","Effect":"Allow","Action":"iam:PassRole",
  "Resource":"arn:aws:iam::<ACCOUNT_ID>:role/app/*"},
 {"Sid":"NeverLoosenTheCeiling","Effect":"Deny",
  "Action":["iam:DeleteRolePermissionsBoundary","iam:DeleteUserPermissionsBoundary"],"Resource":"*"},
 {"Sid":"NeverEditTheBoundary","Effect":"Deny",
  "Action":["iam:CreatePolicyVersion","iam:DeletePolicy","iam:DeletePolicyVersion","iam:SetDefaultPolicyVersion"],
  "Resource":"arn:aws:iam::<ACCOUNT_ID>:policy/boundary/*"}
]}
```
Why each piece matters:
- `iam:PermissionsBoundary` condition on create **and** on every policy-changing action:
  otherwise a team creates a compliant role then attaches policies to an existing
  unbounded role.
- Path scoping (`role/app/*`) stops them editing platform roles, including the deployer.
- `PassRole` scoped to the same path: they can only hand roles of that path to services. The IAM guide
  warns that a user who can pass a more powerful role lets the service act with it, and that controlling
  `iam:PassRole` through role tags (`ResourceTag`) does not give reliable results, so scope by role ARN or path.
- Denies on deleting the boundary and on editing the boundary policy close the two obvious
  escalations.

## 3. Enforce it at the org too
Put the same rules in an SCP for workload OUs: deny `iam:CreateRole` unless the
`iam:PermissionsBoundary` condition key equals the boundary ARN, with an `ArnNotLike` condition on
`aws:PrincipalArn` as the exception for the platform's break-glass and pipeline roles (`NotPrincipal` is not
supported in SCPs). Because SCPs intersect with identity policies, the SCP still applies if someone later grants
a team `AdministratorAccess`.

## 4. IaC
- CDK: `iam.PermissionsBoundary.of(scope).apply(<managed policy>)` applies a boundary to the roles under that
  scope.
- CloudFormation: set the permissions boundary on every role resource in the template.
- Terraform: `permissions_boundary` on `aws_iam_role` is the ARN of the boundary policy.

## Gotchas
- Service-linked roles are created by services, not by the delegate; allow
  `iam:CreateServiceLinkedRole` separately, scoped with the `iam:AWSServiceName` condition key and the
  `role/aws-service-role/<service>.amazonaws.com/` resource path.
- A boundary that is too narrow causes `AccessDenied` that looks like a missing identity permission; check the
  boundary as well as the identity policy.
- Do not use resource-policy `NotPrincipal` + `Deny` for principals that have a boundary: it denies them
  regardless of what you list.
- Forgetting the deny on `CreatePolicyVersion` for the boundary itself = the team rewrites the ceiling.
- Instance profiles: `iam:AddRoleToInstanceProfile`/`CreateInstanceProfile` also need scoping
  to the path, or a team attaches a platform role to an EC2 instance it controls.

## Verify
- [ ] As the delegate: `aws iam create-role --path /app/ --role-name x ...` **without** the boundary is denied.
- [ ] With the boundary it succeeds; attaching `AdministratorAccess` to it succeeds but
      `iam:CreateUser` from that role is still denied (boundary wins).
- [ ] `aws iam delete-role-permissions-boundary --role-name x` is denied.
- [ ] `aws iam create-policy-version` on the boundary ARN is denied.
- [ ] IAM Access Analyzer policy validation on the delegate and boundary policies: no errors.

## Checked
Checked 2026-10-24 against the IAM User Guide pages "Permissions boundaries for IAM entities", "Policy
evaluation logic", "Create a service-linked role" and "Grant a user permissions to pass a role to an AWS
service", the AWS CDK `permissions-boundary.ts` source and the Terraform AWS provider `aws_iam_role`
documentation. Corrected: the old text said resource policies naming the role ARN are not limited by the
boundary; the guide says they are limited (only grants to a user ARN or a role session ARN escape the implicit
deny). Removed the user-related actions from the role-scoped statement (they did not match the role resource), the
quoted newer error message, the CDK context key and role `path` property, the cfn-guard/Hook suggestion and
the `PermissionsBoundary:` CloudFormation property name, none of which were confirmed. Confirmed the
`iam:PermissionsBoundary` and `iam:AWSServiceName` condition keys, the delegation statements pattern (create/attach/
put/delete policy actions with the boundary condition; deny boundary deletion and policy edits), `NotPrincipal`
not supported in SCPs, `PermissionsBoundary.of(...).apply(...)` and `permissions_boundary`.
Method: documentation only; no commands were run.
