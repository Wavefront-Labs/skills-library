---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-resource-based-policies-and-add-permission
name: lambda-resource-based-policies-and-add-permission
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, resource-based-policy, add-permission, put-resource-policy, cross-account, confused-deputy]
level: practitioner
status: docs-checked
description: "Grant services, accounts and organizations access to a Lambda function with add-permission or full JSON policies via put-resource-policy: scoping, qualifiers, limits."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html", "https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda resource-based policies

**Rule:** a resource-based policy grants other AWS accounts, users, organizations and services access to the
function (principal, action, effect, resource, optional condition). It is limited to 20 KB.

## 1. Two ways to write it
- **Individual permissions** (`add-permission` / `AddPermission`): single Allow statements; only the condition
  keys `aws:SourceArn`, `aws:SourceAccount` and `aws:PrincipalOrgID` are supported. It appends to the existing policy.
- **Full JSON policy** (`put-resource-policy` / `PutResourcePolicy`): any IAM global condition key, many
  statements and principals, explicit Deny. AWS recommends it. It **replaces** the whole existing policy, so read
  it first with `get-resource-policy` and pass `--revision-id`.
```bash
aws lambda add-permission --function-name thumbnailer --statement-id s3-uploads \
  --action lambda:InvokeFunction --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::uploads-bucket --source-account 111122223333
aws lambda get-resource-policy --resource-arn arn:aws:lambda:eu-west-1:111122223333:function:thumbnailer
aws lambda put-resource-policy --resource-arn arn:aws:lambda:eu-west-1:111122223333:function:thumbnailer \
  --policy file://policy.json --revision-id <REVISION_ID>
```
`put-resource-policy` needs `lambda:PutResourcePolicy`, `lambda:AddPermission` and `lambda:RemovePermission`;
`get-resource-policy` needs `lambda:GetResourcePolicy` and `lambda:GetPolicy`.
Scope every service principal with a source ARN or source account; without one any resource of that service could
invoke the function (confused deputy). S3 bucket ARNs contain no account ID, so add the source account as well.

## 2. Example policies (from AWS)
Allow an organization to invoke:
```json
{"Version":"2012-10-17","Statement":[{"Sid":"org-access","Effect":"Allow","Action":"lambda:InvokeFunction",
 "Principal":"*","Resource":"arn:aws:lambda:us-east-2:111122223333:function:my-function",
 "Condition":{"StringEquals":{"aws:PrincipalOrgID":"o-a1b2c3d4e5f"}}}]}
```
The same page shows an Allow for all S3 buckets in an account with an explicit Deny for one bucket, and how
to restrict to organization paths with `aws:PrincipalOrgPaths`.

## 3. Aliases and versions
The policy resource can be the unqualified function, a version or an alias ARN (a wildcard covers all versions
and aliases). `get-resource-policy` and `delete-resource-policy` accept the unqualified ARN or a version or alias ARN.

## 4. Inspect and clean up
```bash
aws lambda get-policy --function-name thumbnailer --output text
aws lambda remove-permission --function-name thumbnailer --statement-id s3-uploads
aws lambda delete-resource-policy --resource-arn arn:aws:lambda:eu-west-1:111122223333:function:thumbnailer
```
Remove single statements with `remove-permission`; `delete-resource-policy` deletes the whole policy.

## Gotchas
- `put-resource-policy` overwrites permissions that `add-permission` created earlier.
- If `add-permission` runs after `put-resource-policy`, the new statement is appended to the JSON policy.
- A provided older `--revision-id` means Lambda does not update the policy.

## Verify
- [ ] Every service statement has a source ARN or source account; cross-account statements name specific accounts or an organization condition.
- [ ] The integration works end to end after granting.

## Checked
Date 2026-10-23. Lambda Developer Guide resource-based policy and quotas pages. Confirmed: 20 KB limit, the two methods and their
condition-key differences, overwrite versus append behaviour, revision-id guard, required IAM actions, CLI
commands, organization example. Removed unconfirmed claims: function URL statements
(`InvokeFunctionUrl` and `InvokedViaFunctionUrl`), the alias-permission semantics beyond the documented
ARN forms, layer permissions, Access Analyzer and CloudFormation remarks, and the S3 notification ordering gotcha.
Method: documentation only; no commands were run.
