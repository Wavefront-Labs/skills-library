---
id: computing-software.cloud-infrastructure-engineering.aws.secrets-manager-and-parameter-store
name: secrets-manager-and-parameter-store
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, secrets-manager, parameter-store, ssm-parameter-store, systems-manager, secret-rotation, rotation-lambda, securestring, staging-labels, awscurrent, awspending, secrets-caching, cross-account-secrets, secret-replication, get-parameters-by-path, secrets-management, configuration-management]
level: practitioner
status: docs-checked
description: "Choose and run SSM Parameter Store vs Secrets Manager: tiers, SecureString with KMS, rotation and staging labels, caching, quotas, cross-account."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-advanced-parameters.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-throughput.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_limits.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/troubleshoot_rotation.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Secrets Manager and Parameter Store — configuration and secrets that rotate themselves

**Goal:** no credential in code, env files or Terraform state; every secret has an owner,
a KMS key, a rotation schedule and a cache in front of it so the API quota never becomes
an outage. Key policy details live in `...aws.kms-key-management`.

## 1. Which store
| | Parameter Store standard | Parameter Store advanced | Secrets Manager |
|---|---|---|---|
| Size | 4 KB | 8 KB | 65,536 bytes |
| Count | 10,000 per account and Region | 100,000 | 500,000 secrets per Region |
| Cost | no additional charge | charges apply | charged per secret plus API calls (see the pricing pages) |
| Parameter policies | not supported | supported | n/a |
| Cross-account | not supported | shared parameters supported | resource-based policy |
Standard can be upgraded to advanced; advanced cannot be downgraded (delete and recreate).
Rule of thumb: **config and non-rotating values → Parameter Store**; **database/API
credentials that must rotate, be shared cross-account or replicated → Secrets Manager**.
Do not put secrets in `String` parameters: `SecureString` with a customer managed key
is the floor.

## 2. Parameter Store mechanics
- Hierarchies are the organising principle: `/prod/payments/db/host`. Fetch a subtree
  with `aws ssm get-parameters-by-path --path /prod/payments --recursive --with-decryption`
  and grant IAM on the prefix ARN `arn:aws:ssm:<region>:<acct>:parameter/prod/payments/*`.
- `GetParameters` takes at most 10 names and returns unreadable or missing names in
  `InvalidParameters` instead of an error; check that list.
- Default throughput is 40 TPS shared by GetParameter, GetParameters and GetParametersByPath.
  `update-service-setting --setting-id /ssm/parameter-store/high-throughput-enabled --setting-value true`
  raises it (GetParameter 10,000 TPS, GetParameters 1,000, GetParametersByPath 100) and
  switches on per-API-interaction charges (see the Parameter Store pricing page).

## 3. Secrets Manager mechanics
- A secret is a versioned value up to 65,536 bytes (`SecretString` or `SecretBinary`). Store
  structured values as JSON.
- **Staging labels** drive rotation: `AWSCURRENT` is what clients get by default,
  `AWSPENDING` is the new version mid-rotation, `AWSPREVIOUS` is the rollback. A
  rotation Lambda runs four steps (`createSecret`, `setSecret`, `testSecret`,
  `finishSecret`).
- **Managed rotation** needs no Lambda, and most managed secrets use it. For other
  secrets, rotation by Lambda function. The schedule is `RotationRules`:
  `AutomaticallyAfterDays` (1-1000) or a `ScheduleExpression`, plus an optional `Duration`
  window in hours (pattern `[0-9]+h`). Alternating-users rotation is one of the Lambda strategies.
- The rotation Lambda in a VPC needs a Secrets Manager VPC endpoint or a NAT/internet gateway;
  a missing route is a common reason a rotation stalls after `createSecret`.
- `delete-secret --recovery-window-in-days N` sets the recovery window;
  `--force-delete-without-recovery` skips it.
- Replicas: `replicate-secret-to-regions --add-replica-regions Region=...,KmsKeyId=...`
  adds replicas in other Regions.
- Versions: Secrets Manager keeps at most 100 versions per secret and 20 staging labels
  across a secret; updating the value more than once every 10 minutes can reach the version quota.

## 4. Getting values into workloads without API storms
- Cache secrets client-side and refresh on a TTL or on an authentication failure; never fetch per request.
- Secrets Manager default quotas per Region: `GetSecretValue` 10,000 per second,
  `DescribeSecret` 40,000, `BatchGetSecretValue` 100, `RotateSecret`/`CancelRotateSecret` combined 50.
  A fleet without caching can still trip them during a mass restart.
- Cross-account requests are throttled against the calling identity's account.
- **Terraform:** reading a secret puts the plaintext in state — see
  `computing-software.cloud-infrastructure-engineering.terraform.secrets-handling-in-state-and-plans`.

## 5. Cross-account and least privilege
- Attach a resource policy to the secret (limit 20,480 characters) granting the consumer's
  role `secretsmanager:GetSecretValue`, and grant the same role `kms:Decrypt` in the
  **customer managed** key policy.
- Scope IAM by ARN prefix (`secret:prod/payments/*`). Grant `secretsmanager:GetSecretValue`
  only, not `secretsmanager:*`.

## Gotchas
- Rotation immediately after creation fails if the stored credential is already
  wrong — test `get-secret-value` and a manual login first, then enable rotation.
- Standard parameters cannot hold more than 4 KB; a larger value needs the advanced tier.

## Verify
- [ ] No `String` parameters hold credentials; all SecureString/secrets use a CMK with scoped key policy.
- [ ] Every Secrets Manager secret has rotation enabled, and a forced `rotate-secret` completes with `AWSCURRENT` on the new version and a successful app login.
- [ ] Consumers cache values — CloudWatch `GetSecretValue` call rate is flat under load.
- [ ] Cross-account reads work from the consumer role and fail from an unlisted role.
- [ ] A restore after `delete-secret` within the recovery window returns the same value.

## Checked
2026-10-31. Confirmed against the Parameter Store tiers and throughput pages, the Secrets Manager quotas and
rotation-troubleshooting pages, and the botocore models for `secretsmanager` and `ssm`: tier sizes, counts,
sharing and downgrade rules, the 40 / 10,000 / 1,000 / 100 TPS figures, secret size, count, version, label and
policy-length quotas, GetSecretValue and other TPS quotas, `RotationRules` fields, `InvalidParameters`,
the four rotation steps and VPC endpoint or NAT need. Removed: prices, the Lambda extension port and cache TTL,
CloudFormation and ECS injection syntax, Config rule names, rotation-strategy side effects, the delete-secret
window range, ARN suffix length, and other unconfirmed specifics.
Method: documentation only; no commands were run.
