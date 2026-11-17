---
id: computing-software.cryptography-implementation.key-management.aws-secrets-manager-rotation
name: aws-secrets-manager-rotation
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, aws-secrets-manager, secret-rotation, rotation-lambda, awscurrent, awspending, rds-rotation, secrets-manager, aws]
level: practitioner
status: docs-checked
description: "Rotate secrets with AWS Secrets Manager: rotation function steps, staging labels, single-user versus alternating-user strategies, managed RDS rotation and caching."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda-functions.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Secrets Manager rotation

## Rotation function contract
Secrets Manager calls your Lambda four times per rotation with `Step`:
1. `createSecret` - generate the new value, store it as a new version labelled `AWSPENDING`.
2. `setSecret` - apply it to the target (database or third-party service).
3. `testSecret` - log in with the pending value.
4. `finishSecret` - move `AWSCURRENT` to the new version (old version gets `AWSPREVIOUS`).

```
aws secretsmanager rotate-secret --secret-id prod/orders/db \
  --rotation-lambda-arn arn:aws:lambda:...:function:rotate-db \
  --rotation-rules '{"ScheduleExpression":"rate(30 days)"}'
aws secretsmanager describe-secret --secret-id prod/orders/db   # VersionIdsToStages, last rotated
```

## Notes
- `setSecret` changes the credential in the target to match `AWSPENDING`; `testSecret` uses the pending version to
  access the target. Do not remove `AWSPENDING` yourself before `finishSecret`.
- Apps read `AWSCURRENT`; `AWSPENDING` exists only during rotation.

## Verify
- [ ] Manual `rotate-secret` completes all four steps (check Lambda logs) and the app keeps working.
- [ ] Old password fails after rotation.

## Checked
2026-10-31. Confirmed against the Secrets Manager rotation Lambda page: the four steps, `AWSPENDING`, `AWSCURRENT` and
`AWSPREVIOUS` behaviour; CLI commands and flags via check_commands. Removed (no readable source fetched): rotation
strategies table, client caching advice, security bullets, idempotency claim.
Method: documentation only; no commands were run.
