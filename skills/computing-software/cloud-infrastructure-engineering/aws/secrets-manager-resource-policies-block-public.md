---
id: computing-software.cloud-infrastructure-engineering.aws.secrets-manager-resource-policies-block-public
name: secrets-manager-resource-policies-block-public
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, secrets-manager, secret-resource-policy, block-public-policy, cross-account-secrets]
level: advanced
status: docs-checked
description: "Attach Secrets Manager resource policies for cross-account or VPC-restricted access, validate them, and use BlockPublicPolicy to reject broad grants."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_resource-policies.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples_cross.html", "https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret resource policies and BlockPublicPolicy

## 1. Cross-account read
Policy on the secret (owner account):
```json
{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Principal":{"AWS":"arn:aws:iam::<CONSUMER_ACCOUNT_ID>:role/app"},
  "Action":"secretsmanager:GetSecretValue","Resource":"*"}]}
```
```bash
aws secretsmanager validate-resource-policy --secret-id prod/db --resource-policy file://policy.json
aws secretsmanager put-resource-policy --secret-id prod/db --resource-policy file://policy.json --block-public-policy
```
Cross-account access needs all three:
- The resource policy on the secret and an identity policy in the consumer account (both must allow).
- A customer managed KMS key on the secret: the `aws/secretsmanager` key cannot be used cross-account. Its key
  policy allows the consumer role `kms:Decrypt` and `kms:DescribeKey`; add `kms:GenerateDataKey` if the role also
  creates or changes secret values.
- The consumer's identity policy allows `GetSecretValue` on the secret ARN and `kms:Decrypt` on the key.
Cross-account permission is effective only for a listed set of operations (for example `GetSecretValue`,
`DescribeSecret`, `PutSecretValue`, `DeleteSecret`, `RotateSecret`, `PutResourcePolicy`); other actions are not
shared. Granting `secretsmanager:PutResourcePolicy` lets a principal rewrite the policy and escalate access, so
keep it to administrators.

## 2. Restrict to a VPC endpoint
```json
{"Effect":"Deny","Principal":"*","Action":"secretsmanager:GetSecretValue","Resource":"*",
 "Condition":{"StringNotEquals":{"aws:SourceVpce":"vpce-0abc"}}}
```
`aws:SourceVpce` is an IAM global condition key. Exempt rotation or admin roles that do not use the endpoint
(for example with `aws:PrincipalArn`), or they will be denied.

## 3. BlockPublicPolicy
Attaching a policy in the console runs the Zelkova automated reasoning engine through `ValidateResourcePolicy`
to prevent granting a wide range of principals access. From the CLI or SDK, pass `BlockPublicPolicy` to
`PutResourcePolicy` (`--block-public-policy`) to get the same check. It covers only policies attached directly
to the secret: also review identity policies on the principals and key policies on associated KMS keys.

## Gotchas
- Cross-account callers must use the secret's ARN (a name resolves only in the owner account); AWS recommends the
  complete ARN rather than a partial one.
- `get-resource-policy` reads the policy and `delete-resource-policy` removes it. The policy is at most 20,480
  characters.

## Verify
- [ ] From the consumer account `aws secretsmanager get-secret-value --secret-id <FULL_ARN>` succeeds.
- [ ] Putting a policy with `"Principal":"*"` and `--block-public-policy` fails.

## Checked
Date: 2026-10-27. Documentation release: AWS Secrets Manager User Guide and API Reference (latest), botocore
secretsmanager 2017-10-17 model. Confirmed: cross-account requirements, KMS rules and key actions, the operation list
effective cross-account, the `PutResourcePolicy` escalation warning, `BlockPublicPolicy` behaviour and
Zelkova validation, the ARN requirement, and the 20,480-character policy limit. Removed the `VersionStage` condition,
the `kms:ViaService` condition and the `aws:PrincipalOrgID` remedy (not confirmed in the pages read).
Method: documentation only; no commands were run.
