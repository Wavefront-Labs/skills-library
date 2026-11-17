---
id: computing-software.cloud-infrastructure-engineering.aws.secrets-manager-rotation-troubleshooting
name: secrets-manager-rotation-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, secrets-manager, rotation-failure, rotation-troubleshooting, awspending, staging-labels-recovery, lambda]
level: advanced
status: docs-checked
description: "Diagnose and recover failed Secrets Manager rotations: read the four-step logs, fix network causes, clear a stuck AWSPENDING label, and rerun safely."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/troubleshoot_rotation.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda-functions.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Secrets Manager rotation

## 1. How rotation runs (so you can read the logs)
The rotation Lambda is invoked with `Step` = `createSecret`, `setSecret`, `testSecret`,
`finishSecret`, each with the same `ClientRequestToken` (the new version ID).
- `createSecret`: generate a password, store it as a new version labelled `AWSPENDING`.
- `setSecret`: change the password in the database (or service) to the pending value.
- `testSecret`: log in with the pending value.
- `finishSecret`: move `AWSCURRENT` to the new version; old one becomes `AWSPREVIOUS`.
Managed rotation does not use a Lambda function.

## 2. Find the failure
```bash
aws secretsmanager describe-secret --secret-id prod/db/app \
  --query '{last:LastRotatedDate,next:NextRotationDate,versions:VersionIdsToStages,enabled:RotationEnabled}'
aws logs tail /aws/lambda/<rotation-function-name> --since 2h
```
CloudTrail records `RotationFailed` events. The Lambda log line names the step that threw.

## 3. Causes by symptom
| Symptom in logs | Cause | Fix |
|---|---|---|
| No activity after "Found credentials in environment variables"; task near the Lambda timeout (default 30000 ms) | Lambda in a VPC cannot reach the Secrets Manager endpoint | Add a Secrets Manager VPC endpoint (recommended) or a NAT/internet gateway |
| Rotation stops after `createSecret` | Lambda timeout too short; VPC endpoint security groups do not allow the VPC CIDRs on ingress; endpoint policy does not allow Lambda; alternating-users rotation with an RDS-managed superuser secret and no path to the RDS API | Fix the matching item; for the RDS case add a VPC endpoint for the database service |
| `RotationFailed` "Pending secret version ... was not created by Lambda" (assumed role or cross-account rotation) | Lambda does not pass the `RotationToken` | Remove the `AWSPENDING` label, update the Lambda to pass `RotationToken` to `PutSecretValue`, restart rotation |
| `password authentication failed` in `setSecret` | `AWSCURRENT` already wrong (someone changed the DB password manually) | Put the real current password back into the secret (`put-secret-value`), then rotate |

## 4. Clearing a stuck AWSPENDING
If rotation keeps failing, clear the `AWSPENDING` staging label and retry rotation. Check
that `AWSPREVIOUS` and `AWSPENDING` versions are valid first.
```bash
aws secretsmanager describe-secret --secret-id prod/db/app --query VersionIdsToStages
# remove the label from the pending version
aws secretsmanager update-secret-version-stage --secret-id prod/db/app \
  --version-stage AWSPENDING --remove-from-version-id <pending-version-id>
aws secretsmanager rotate-secret --secret-id prod/db/app
```
If `setSecret` did succeed (the DB now has the pending password) but `finishSecret`
failed, either finish manually by moving `AWSCURRENT`
(`update-secret-version-stage --version-stage AWSCURRENT --move-to-version-id <pending>
--remove-from-version-id <current>`) or set the DB back to the current password.
Test with the actual credentials before touching labels.

## 5. Prevent repeats
- Rotation window: `--rotation-rules '{"ScheduleExpression":"<schedule>","Duration":"2h"}'`
  to rotate during low traffic (`Duration` is hours, pattern `[0-9]+h`).
- Apps must re-fetch the secret on auth failure (cache with TTL, refresh on login error).
- Avoid calling `PutSecretValue` or `UpdateSecret` more than once every 10 minutes: each call
  creates a version and the quota is 100 versions per secret.

## Verify
- [ ] `aws secretsmanager rotate-secret --secret-id ...` completes; `VersionIdsToStages` shows a new AWSCURRENT and the old as AWSPREVIOUS, no orphan AWSPENDING.
- [ ] Application connections succeed with the new password (check DB login logs).
- [ ] An alert on `RotationFailed` is wired and tested.

## Checked
2026-10-31. Confirmed against the Secrets Manager rotation-troubleshooting and quotas pages and the botocore
`secretsmanager` model: the four step names, `AWSPENDING` clearing, VPC endpoint or NAT need, default Lambda
timeout 30000 ms, the causes of rotation stopping after `createSecret`, `RotationToken`, `RotationFailed`,
`RotationRules.Duration` pattern, 100 versions per secret and the 10-minute guidance. Removed: the IAM
permission list, `RotationSucceeded`, `masterarn` and Lambda resource-policy rows, port 443 egress and
other unconfirmed specifics.
Method: documentation only; no commands were run.
