---
id: computing-software.cloud-infrastructure-engineering.aws.iam-service-roles-linked-roles-and-passrole
name: iam-service-roles-linked-roles-and-passrole
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, service-role, service-linked-role, passrole, privilege-escalation, iam-roles, least-privilege]
level: practitioner
status: docs-checked
description: "Distinguish service roles from service-linked roles, scope iam:PassRole so users cannot escalate privileges through services, and fix PassRole and SLR creation errors."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create-service-linked-role.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service roles, service-linked roles and iam:PassRole

## 1. Two kinds of role for services
| | Service role | Service-linked role (SLR) |
|---|---|---|
| Created by | you (an administrator can create, modify and delete it in IAM) | the service, or you through the service or IAM when the service allows it |
| Path/name | anything | `role/aws-service-role/<service>.amazonaws.com/...`; the service defines the name |
| Permissions | you define | predefined by the service, including trust and permissions policy; you can view but not edit them |
| Examples | Lambda execution role, ECS task role, CodeBuild role | `AWSServiceRoleForAutoScaling` |
SLR creation needs `iam:CreateServiceLinkedRole`, which the IAM guide scopes with a resource of
`arn:aws:iam::*:role/aws-service-role/<SERVICE>.amazonaws.com/<ROLE_NAME_PREFIX>*` and a condition
`"StringLike": {"iam:AWSServiceName": "<SERVICE>.amazonaws.com"}`; attaching policies needs `iam:AttachRolePolicy`
or `iam:PutRolePolicy` on that role. Do not guess the service principal: it is case sensitive and varies by
service, so read the service's SLR documentation. Some services create their SLR automatically when you perform
an action; if you must create one yourself:
```bash
aws iam create-service-linked-role --aws-service-name autoscaling.amazonaws.com
```
Users and roles allowed to call a service that uses an SLR can gain indirect access to whatever the SLR can reach.
Only SLRs may exceed the account's role-count limit.

## 2. PassRole: the escalation path
To pass a role to an AWS service a user needs the `iam:PassRole` permission. Whoever can create a Lambda function,
EC2 instance or ECS task **and pass any role** can have the service act with that role's permissions, for example
Amazon S3 access the caller does not have. `iam:PassRole` controls which roles a principal may hand to a service.
```json
{"Effect": "Allow", "Action": "iam:PassRole",
 "Resource": "arn:aws:iam::<ACCOUNT_ID>:role/app/*",
 "Condition": {"StringEquals": {"iam:PassedToService": ["lambda.amazonaws.com", "ecs-tasks.amazonaws.com"]}}}
```
- Scope `Resource` to a role path (`/app/`) or named roles reserved for workloads; the IAM guide's examples scope by
  role name pattern, and it usually pairs `iam:PassRole` with `iam:GetRole`.
- `iam:PassedToService` limits which service principal can receive the role.
- `PassRole` only works for passing a role to a service in the **same account**. To use a role from another account
  you must first create a role in the service's account that can assume it.
- Do not control who can pass a role by tagging the role and using `ResourceTag` with `iam:PassRole`: the guide says
  this does not give reliable results.
- PassRole isn't an API call and produces no CloudTrail event of its own: look at the CloudTrail record of the
  call that created or changed the resource (for example `CreateFunction`) to see which role was passed.
- If you name a service-linked role explicitly (for example for an Auto Scaling group) you also need `iam:PassRole`
  for it; if you do not name one, the permission is not required and the default SLR is used.

## 3. Common errors
- A "not authorized to perform iam:PassRole on resource ...role/X" error: add a scoped PassRole statement for that
  role.
- A missing service-linked role: grant `iam:CreateServiceLinkedRole` for that service's principal or pre-create the
  role in account baselines.
- Service role trust policy with the wrong service principal: the service cannot assume the role. Check the
  service's documentation for the exact principal.

## Gotchas
- Before a service-linked role can be deleted its related resources must be deleted first.
- A role passed to a service should have only the permissions you are happy for the caller to use indirectly; a
  permissions boundary on the created roles plus PassRole limited to bounded roles is a common self-service
  pattern.

## Verify
- [ ] Developer role cannot create a Lambda with an admin role (AccessDenied on PassRole); can with an `/app/` role.
- [ ] IAM Access Analyzer policy validation shows no PassRole with `Resource: *`.
- [ ] New-account baseline pre-creates the SLRs your pipelines rely on.

## Checked
Checked 2026-10-24 against the IAM User Guide pages "Create a service-linked role", "Grant a user permissions to
pass a role to an AWS service". Confirmed: SLR path format and ownership, predefined
and non-editable permissions, `iam:CreateServiceLinkedRole` with the `iam:AWSServiceName` condition, `aws iam
create-service-linked-role --aws-service-name`, `AWSServiceRoleForAutoScaling` as an automatically created SLR,
indirect permission transfer, SLRs exceeding the role limit, PassRole semantics, `iam:PassedToService`, the
same-account restriction, the unreliable-ResourceTag warning, CloudTrail behaviour, and deletion needing related
resources removed first. Removed unchecked examples: the `AWSServiceRoleForECS` and `...ElasticLoadBalancing`
names, the quoted Lambda trust error text, the "first use in a new account fails" claim and the confused-deputy
condition advice for service role trust policies.
Method: documentation only; no commands were run.
