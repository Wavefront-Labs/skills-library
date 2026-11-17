---
id: computing-software.cloud-infrastructure-engineering.aws.rds-managed-master-user-password
name: rds-managed-master-user-password
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, aurora, secrets-manager, managed-master-password, managed-secrets, rds-managed-secret, manage-master-user-password, secret-rotation, master-user-secret, cloudformation, kms]
level: practitioner
status: docs-checked
description: "Let RDS and Aurora own the master password in Secrets Manager: enable on new or existing DBs, CMK choice, rotation schedule, app access, CloudFormation wiring and limits."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-secrets-manager.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_how-services-use-secrets_RDS.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-rds-dbinstance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS managed master user password (Secrets Manager integration)

**Goal:** no human ever sees the database master password; RDS generates it, stores it in a
service-managed Secrets Manager secret, rotates it, and applications read it by ARN.

## 1. Enable
New instance or cluster:
```bash
aws rds create-db-instance --db-instance-identifier app-db --engine postgres \
  --db-instance-class db.r6g.large --allocated-storage 100 \
  --master-username dbadmin --manage-master-user-password \
  --master-user-secret-kms-key-id alias/rds-secrets      # optional CMK; default is the Secrets Manager key
aws rds create-db-cluster --db-cluster-identifier app-aurora --engine aurora-postgresql \
  --master-username dbadmin --manage-master-user-password
```
Existing database (switches from a password you set; for Aurora and Multi-AZ DB clusters use `modify-db-cluster`):
```bash
aws rds modify-db-instance --db-instance-identifier app-db --manage-master-user-password --apply-immediately
aws rds describe-db-instances --db-instance-identifier app-db \
  --query 'DBInstances[0].MasterUserSecret'          # SecretArn, SecretStatus, KmsKeyId
```
`SecretStatus` values: `creating`, `active`, `rotating`, `impaired`. The secret is named like `rds!db-<uuid>` (instance)
or `rds!cluster-<uuid>`. After RDS manages the credentials you cannot change the KMS key that encrypts the secret.

## 2. Rotation
- RDS rotates the secret every seven days by default; you can change settings such as the schedule.
- Rotate immediately with RDS, not Secrets Manager: `aws rds modify-db-instance --db-instance-identifier app-db --rotate-master-user-password --apply-immediately`
  (`modify-db-cluster` for clusters). Rotation creates a new version of the existing secret.
- New connections using a cached old password fail after rotation until they refresh. Use the Secrets Manager
  caching client with a short TTL and retry auth failures once after a forced refresh, or connect through RDS
  Proxy pointing at the same secret.

## 3. CloudFormation / CDK
```yaml
Db:
  Type: AWS::RDS::DBInstance
  Properties:
    Engine: postgres
    MasterUsername: dbadmin
    ManageMasterUserPassword: true
    MasterUserSecret: { KmsKeyId: !Ref SecretsKey }
Outputs:
  DbSecretArn: { Value: !GetAtt Db.MasterUserSecret.SecretArn }
```
Pass `DbSecretArn` to the app (env var / Parameter Store), never the value. Grant the app
role `secretsmanager:GetSecretValue` on that ARN and `kms:Decrypt` on the CMK.

## 4. Turning it off
`modify-db-instance --no-manage-master-user-password` (and `modify-db-cluster` for clusters) opts out;
plan app config first. If the managed secret has Secrets Manager
cross-Region replication, the Aurora opt-out silently has no effect until you remove replication
(`aws secretsmanager remove-regions-from-replication`).
Deleting a DB instance that manages a secret also deletes the secret.

## Gotchas
- Limitations (RDS User Guide): not supported with RDS Blue/Green Deployments or RDS Custom; creating a read
  replica from a source that manages credentials is not supported (except RDS for SQL Server and Db2).
  Aurora adds: Aurora global database clusters, cross-Region read replicas, binary log external replication,
  and Aurora MySQL with `validate_password` enabled. Check the page for your engine before enabling.
- Restoring from a snapshot or point in time can enable managed passwords only for RDS for Oracle; for other
  engines enable it with a modify call after the restore. Other restore paths: from Amazon S3 (RDS, and Aurora MySQL).
- To read the secret from another account, give the secret a customer managed KMS key (specify the key ARN) and
  grant access in the key and secret policies.
- Only the master user is managed. Application users should be separate DB users with
  their own Secrets Manager secrets and alternating-user rotation.
- Secrets Manager charges apply to the managed secret (see the Secrets Manager pricing page).

## Verify
- [ ] `describe-db-instances` shows `MasterUserSecret.SecretStatus = active`.
- [ ] `aws secretsmanager describe-secret --secret-id <ARN>` shows `RotationEnabled: true`.
- [ ] Force a rotation; the app keeps serving and logs at most one retried auth failure.
- [ ] No plaintext password in templates, parameters or CI variables (`git grep -i password`).

## Checked
Date: 2026-10-27. Sources: RDS User Guide rds-secrets-manager and Aurora User Guide rds-secrets-manager (limitations,
7-day default, restore support, rotate-now flag, secret status values, KMS key immutability, opt-out behaviour);
CloudFormation `AWS::RDS::DBInstance` reference (`ManageMasterUserPassword`, `MasterUserSecret`,
`MasterUserSecret.SecretArn`); botocore `rds` model. Corrected rotate-now (RDS `--rotate-master-user-password`),
snapshot-restore behaviour and the limitations list; removed the unconfirmed secret-content, single-user rotation,
cross-account `aws/secretsmanager` and `OwningService` claims.
Method: documentation only; no commands were run.
