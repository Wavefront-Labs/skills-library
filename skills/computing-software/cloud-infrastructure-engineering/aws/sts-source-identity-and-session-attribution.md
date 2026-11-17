---
id: computing-software.cloud-infrastructure-engineering.aws.sts-source-identity-and-session-attribution
name: sts-source-identity-and-session-attribution
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sts, source-identity, role-session-name, session-attribution, cloudtrail, audit, identity-center]
level: practitioner
status: docs-checked
description: "Attribute actions in shared roles to a person: role session names, SourceIdentity that survives chaining, trust policy conditions and CloudTrail queries."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_monitor.html", "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SourceIdentity and session attribution

**Question auditors ask:** "Who deleted this bucket?" CloudTrail says
`assumed-role/Admin/botocore-session-1699...` — useless. Fix attribution at assume time.

## 1. Role session name
Set it to the human or job identity; it appears in the ARN
`arn:aws:sts::<ACCOUNT_ID>:assumed-role/Admin/jo.smith`.
```bash
aws sts assume-role --role-arn arn:aws:iam::<ACCOUNT_ID>:role/Admin --role-session-name jo.smith
```
Enforce in the trust policy:
```json
"Condition": {"StringLike": {"sts:RoleSessionName": "${aws:username}"}}
```
(for IAM users) or match a claim for federated users. Weakness: a chained role can choose a
new session name, losing the original identity.

## 2. SourceIdentity (survives chaining)
```bash
aws sts assume-role --role-arn arn:aws:iam::<ACCOUNT_ID>:role/Admin --role-session-name ops \
  --source-identity jo.smith@example.com
```
- Once set, it **cannot be changed** in any subsequent chained `AssumeRole`; actions in the
  session carry `aws:SourceIdentity` and CloudTrail records it in the session context.
- The trust policy must allow `sts:SetSourceIdentity` (alongside `sts:AssumeRole`); require it:
```json
{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_ID>:role/Bastion"},
 "Action": ["sts:AssumeRole", "sts:SetSourceIdentity"],
 "Condition": {"StringLike": {"sts:SourceIdentity": "*@example.com"}}}
```
- When chaining, `sts:SetSourceIdentity` is required in both the calling principal's permissions policy and
  the target role's trust policy; across accounts it must be in the originating principal's policy and the
  target role's trust policy.
- IdPs can set it via SAML attribute `https://aws.amazon.com/SAML/Attributes/SourceIdentity`
  or OIDC claim `https://aws.amazon.com/source_identity`.
- Policies can use `aws:SourceIdentity` in conditions (e.g. deny destructive actions unless set).
- You cannot switch in the console to a role that requires a source identity; use the CLI or API.
- A value cannot begin with `aws:`, and AWS does not control its content, so choose an attribute whose
  provenance you control. CloudTrail does not capture it when an AWS service or service-linked role acts
  on a federated identity's behalf.

## 3. Query CloudTrail
```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteBucket \
  --query 'Events[].CloudTrailEvent' --output text | jq -r '.userIdentity.sessionContext.sourceIdentity, .userIdentity.arn'
```
CloudTrail Lake: `SELECT eventTime, eventName, userIdentity.sessionContext.sourceIdentity FROM <EDS> WHERE eventName='DeleteBucket'`.

## Gotchas
- Trust policies without `sts:SetSourceIdentity` reject assume calls that pass it; roll out
  trust policy updates before tooling starts sending it.
- Session names are 2 to 64 characters from `[\w+=,.@-]`. The STS API reference and model limit a source
  identity to 2 to 64 characters with the same pattern, while the IAM guide page says 256; stay within 64.

## Verify
- [ ] A chained session (A → B → C) shows the same `sourceIdentity` in CloudTrail events from role C.
- [ ] Assume without SourceIdentity is denied where the trust policy requires it.
- [ ] Incident drill: identify the person behind a test deletion from CloudTrail within 5 minutes.

## Checked

Checked 2026-10-27 against the IAM User Guide page "Monitor and control actions taken with assumed roles", the AWS STS API reference for AssumeRole and AssumeRoleWithSAML, the IAM condition keys page and the botocore sts model:
- `sts:SetSourceIdentity` requirements (trust policy, chaining and cross-account), immutability after it is set, the SAML attribute and OIDC claim names, the console limitation and the CloudTrail locations (`requestParameters.sourceIdentity` on the assume call and `userIdentity.sessionContext.sourceIdentity` on later calls).
- `--source-identity` is an `AssumeRole` parameter; `sts:RoleSessionName`, `sts:SourceIdentity` and `aws:SourceIdentity` condition keys are documented.
- The length limit for a source identity differs between the IAM guide (256) and the API reference and model (64); the skill advises 64.
Removed: the statement that Identity Center sets user context automatically. The lookup-events command was not run.

Method: documentation only; no commands were run.
