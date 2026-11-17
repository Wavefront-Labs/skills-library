---
id: computing-software.cloud-infrastructure-engineering.aws.secrets-manager-batch-retrieval-quotas-and-cost
name: secrets-manager-batch-retrieval-quotas-and-cost
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, secrets-manager, batch-get-secret-value, secrets-cost, quotas, caching]
level: practitioner
status: docs-checked
description: "Cut Secrets Manager calls and cost with BatchGetSecretValue, client-side caching and the Lambda extension, and plan around per-secret pricing and quotas."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_BatchGetSecretValue.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_limits.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BatchGetSecretValue, quotas and cost

## 1. Batch retrieval
```bash
aws secretsmanager batch-get-secret-value --secret-id-list prod/db prod/api-key prod/smtp
aws secretsmanager batch-get-secret-value --filters Key=tag-key,Values=app --max-results 20
```
- Retrieves up to 20 secrets per call. Give either `SecretIdList` (1 to 20 names or ARNs) or `Filters` (at most 10
  filters), not both. `MaxResults` (1 to 20) works only with `Filters`; use `NextToken` to page.
- Permissions: `secretsmanager:BatchGetSecretValue` plus `secretsmanager:GetSecretValue` on each secret, plus
  `secretsmanager:ListSecrets` with filters, plus `kms:Decrypt` for secrets encrypted with customer managed keys.
- Per-secret failures such as `AccessDeniedException` appear in `Errors` while the call succeeds; always check it.
- CloudTrail records a `GetSecretValue` entry for each secret requested.

## 2. Caching
- Lambda: the AWS Parameters and Secrets Lambda Extension caches secrets and parameters and serves them on
  `localhost:2773` (change with `PARAMETERS_SECRETS_EXTENSION_HTTP_PORT`); the cache TTL for Secrets Manager is set
  with `SECRETS_MANAGER_TTL`.
- Client-side caching components exist for Java, Python, .NET, Go and Rust (see the Secrets Manager user guide).
- Containers: inject secrets at task start instead of per-request calls.

## 3. Cost model
- Secrets Manager charges per secret and per API call; replica secrets are billed as secrets. Check the pricing
  page for current rates (prices were not checked). Secrets scheduled for deletion are not charged.
- Combine related keys into one JSON secret: one secret, one call.

## 4. Quotas to know
Regional quotas read from the Secrets Manager quotas page on 2026-10-27 (none adjustable):
| Quota | Value |
|---|---|
| `GetSecretValue` rate | 10,000 per second |
| `DescribeSecret` rate | 40,000 per second |
| `BatchGetSecretValue` rate | 100 per second |
| `ListSecrets` rate | 100 per second |
| `CreateSecret` and `DeleteSecret` rate | 50 per second each |
| Secret value size | 65,536 bytes |
| Resource policy length | 20,480 characters |
| Secrets per Region | 500,000 |
| Versions per secret | 100 |
| Staging labels across all versions of a secret | 20 |
- Quotas are per Region. For cross-account requests Secrets Manager throttles the account of the caller, not the
  secret owner.
- Avoid calling `PutSecretValue` or `UpdateSecret` more than once every 10 minutes: unlabeled versions are removed
  when there are more than 100, but never within 24 hours of creation.
- Retry throttled calls with backoff; caching removes most of the load.

## Verify
- [ ] Cost Explorer usage for Secrets Manager API requests drops after enabling caching.
- [ ] Batch call output has an empty `Errors` list.

## Checked
Date: 2026-10-27. Documentation release: AWS Secrets Manager User Guide and API Reference (latest), botocore
secretsmanager 2017-10-17 model, Systems Manager Lambda extension page. Confirmed: batch limits and parameter
rules, required permissions, `Errors` behaviour, quota table values, version pruning rule, cross-account throttling,
Lambda extension port and TTL variable names, and no charge for secrets scheduled for deletion. Removed the
unconfirmed Python caching package name and the Parameter Store "costs nothing" claim. Prices were not checked.
Method: documentation only; no commands were run.
