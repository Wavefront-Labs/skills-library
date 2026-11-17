---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-permission-sets-and-assignments
name: identity-center-permission-sets-and-assignments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, identity-center, permission-sets, permission-set, account-assignment, sso, multi-account, least-privilege]
level: practitioner
status: docs-checked
description: "Design Identity Center permission sets (managed, inline, customer-managed refs, session length) and assign them to groups across accounts, including reprovisioning."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/useraccess.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/howtocmp.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity Center permission sets and account assignments

**Model:** permission set (a policy template) × group × account = an Identity Center-controlled
IAM role (its name starts with `AWSReservedSSO_`) provisioned into that account.

## 1. Create a permission set
```bash
INST=$(aws sso-admin list-instances --query 'Instances[0].InstanceArn' --output text)
PS=$(aws sso-admin create-permission-set --instance-arn $INST --name DataEngineer \
  --session-duration PT4H --description "Glue/Athena/S3 data lake" --query PermissionSet.PermissionSetArn --output text)
aws sso-admin attach-managed-policy-to-permission-set --instance-arn $INST --permission-set-arn $PS \
  --managed-policy-arn arn:aws:iam::aws:policy/AmazonAthenaFullAccess
aws sso-admin attach-customer-managed-policy-reference-to-permission-set --instance-arn $INST --permission-set-arn $PS \
  --customer-managed-policy-reference Name=datalake-access,Path=/
aws sso-admin put-inline-policy-to-permission-set --instance-arn $INST --permission-set-arn $PS --inline-policy file://deny-prod-delete.json
aws sso-admin put-permissions-boundary-to-permission-set ...   # optional
```
- **Customer-managed policy references** point to a policy *name and path* that must already exist
  in each target account (deploy it via StackSets); Identity Center creates no policy there and the
  assignment fails if the policy is missing. The name match is not case sensitive and the
  permissions need not be identical between accounts.
- Session duration is 1 to 12 hours (default 1 h; `PT4H` is an ISO 8601 duration).

## 2. Assign to groups (users directly only for management-account access)
```bash
aws sso-admin create-account-assignment --instance-arn $INST --target-type AWS_ACCOUNT --target-id 222222222222 \
  --permission-set-arn $PS --principal-type GROUP --principal-id <GROUP_ID>
aws sso-admin describe-account-assignment-creation-status --instance-arn $INST --account-assignment-creation-request-id <ID>
```
Group IDs from `aws identitystore list-groups --identity-store-id d-xxxx`.

## 3. Changes need provisioning
After editing a permission set, push it to accounts:
```bash
aws sso-admin provision-permission-set --instance-arn $INST --permission-set-arn $PS --target-type ALL_PROVISIONED_ACCOUNTS
```
Console edits reprovision the affected accounts automatically; with the API, call `provision-permission-set`.

## 4. Design guidance
- A small catalogue: ReadOnly, Developer, DataEngineer, Admin, BreakGlass — mapped to IdP groups.
- Production: narrower permission sets, shorter sessions; Admin assigned to few accounts.
- Use ABAC attributes instead of one permission set per team where access differs only by tag.

## Gotchas
- Don't edit the `AWSReservedSSO_*` roles in accounts; Identity Center manages them and updates them as the permission set changes.
- Permission sets live in the management account (or delegated admin); a delegated admin cannot
  manage permission sets provisioned in the management account.
- Permission sets need an organization instance with multi-account permissions enabled (on by default).

## Verify
- [ ] `aws sso-admin list-account-assignments --account-id ... --permission-set-arn ...` shows groups only.
- [ ] A test user in the group sees the account/role in the access portal and can do the intended actions only.
- [ ] Permission sets are in IaC; drift-free after `provision-permission-set`.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages on permission sets, using IAM policies in permission sets, session duration for AWS accounts and delegated administration, plus the botocore sso-admin model:
- Customer managed policy reference rules (pre-created per account, name match, failure if missing, case-insensitive name, permissions need not match).
- Session duration default 1 hour, maximum 12 hours; console edits reprovision accounts.
- `create-permission-set`, `create-account-assignment` (target type `AWS_ACCOUNT`), `list-account-assignments` (requires account ID and permission set ARN), `attach-customer-managed-policy-reference-to-permission-set`, `provision-permission-set` exist with the parameters shown.
- Delegated administrators cannot manage permission sets provisioned in the management account.
Removed: the CloudFormation update behaviour and IAM size-quota statements, which these pages do not cover. The CLI examples were not run.

Method: documentation only; no commands were run.
