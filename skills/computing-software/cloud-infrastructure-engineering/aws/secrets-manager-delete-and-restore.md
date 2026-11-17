---
id: computing-software.cloud-infrastructure-engineering.aws.secrets-manager-delete-and-restore
name: secrets-manager-delete-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, secrets-manager, recovery-window, restore-secret, delete-secret]
level: practitioner
status: docs-checked
description: "Delete Secrets Manager secrets with a 7-30 day recovery window, detect apps still using them, restore with restore-secret, and handle replicas and force delete."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_restore-secret.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/monitoring_cloudwatch_deleted-secrets.html", "https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_DeleteSecret.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting and restoring secrets

## 1. Schedule deletion
```bash
aws secretsmanager delete-secret --secret-id prod/legacy-api --recovery-window-in-days 14   # 7-30, default 30
aws secretsmanager list-secrets --include-planned-deletion --query 'SecretList[?DeletedDate].[Name,DeletedDate]'
```
- `RecoveryWindowInDays` is 7 to 30 days; the default is 30. You cannot combine it with
  `ForceDeleteWithoutRecovery`.
- Secrets Manager makes the secret inaccessible immediately and attaches a `DeletionDate`; until then you can restore
  it. There is no charge for secrets marked for deletion. Deleting needs `secretsmanager:ListSecrets` (console) and
  `secretsmanager:DeleteSecret`.
- You cannot delete a version directly: remove all its staging labels and Secrets Manager deletes it in the
  background.

## 2. Catch the apps you forgot
Send CloudTrail to CloudWatch Logs and add a metric filter to the log group:
```
{ $.eventName = "GetSecretValue" && $.errorMessage = "*secret because it was marked for deletion*" }
```
Alarm on a count above 0, then restore the secret if anything still depends on it. Only `GetSecretValue` calls
that return this error trigger the alarm; other API calls on the secret do not.

## 3. Restore
```bash
aws secretsmanager restore-secret --secret-id prod/legacy-api
```
Restore removes the `DeletionDate` and makes the secret accessible again. It needs `secretsmanager:RestoreSecret`
(and `ListSecrets` in the console). After the window the deletion is permanent.

## 4. Force delete
```bash
aws secretsmanager delete-secret --secret-id test/tmp --force-delete-without-recovery
```
Irreversible. The actual deletion is an asynchronous background process, so creating a secret with the same name
immediately afterwards needs backoff and retry. Limit who holds `secretsmanager:DeleteSecret`.

## 5. Replicated secrets
You cannot delete a primary secret that is replicated; delete the replicas first (a replica deletes immediately):
`aws secretsmanager remove-regions-from-replication --secret-id prod/db --remove-replica-regions eu-west-1`.

## Verify
- [ ] Metric filter alarm fires on a test read during the window.
- [ ] After restore `describe-secret` shows no `DeletedDate`.

## Checked
Date: 2026-10-27. Documentation release: AWS Secrets Manager User Guide and API Reference (latest), botocore
secretsmanager 2017-10-17 model. Confirmed: recovery window range and default, mutual exclusion with force delete,
asynchronous deletion and same-name retry guidance, replica rule, version deletion rule, restore effect, the
CloudTrail metric filter pattern, and no charge during the window. Removed the unconfirmed `InvalidRequestException`
wording, the claim that the name cannot be reused during the window, the claim that restore returns versions and
rotation config "unchanged", and the IAM condition-key guard (key names not found in readable documentation).
Method: documentation only; no commands were run.
