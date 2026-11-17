---
id: computing-software.cloud-infrastructure-engineering.aws.rds-encrypting-unencrypted-instances-and-sharing-snapshots
name: rds-encrypting-unencrypted-instances-and-sharing-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, rds-encryption, encrypted-snapshot-copy, kms, snapshot-sharing, minimal-downtime-migration]
level: advanced
status: docs-checked
description: "Encrypt an existing unencrypted RDS database (snapshot copy with KMS, or replica/DMS for low downtime), change keys, and share encrypted snapshots with other accounts."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CopySnapshot.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ShareSnapshot.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypting RDS and sharing encrypted snapshots

You cannot turn on encryption for an existing RDS instance in place, and you cannot
change the KMS key of an encrypted instance. Both require a copy.

## 1. Snapshot-copy method (simple, has downtime)
```bash
aws rds create-db-snapshot --db-instance-identifier orders --db-snapshot-identifier orders-pre-enc
aws rds wait db-snapshot-available --db-snapshot-identifier orders-pre-enc
aws rds copy-db-snapshot --source-db-snapshot-identifier orders-pre-enc \
  --target-db-snapshot-identifier orders-enc --kms-key-id alias/rds-prod
aws rds wait db-snapshot-available --db-snapshot-identifier orders-enc
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier orders-new \
  --db-snapshot-identifier orders-enc --db-subnet-group-name prod-db \
  --vpc-security-group-ids sg-0db --db-parameter-group-name orders-pg --multi-az
```
Downtime = stop writes, final snapshot, copy, restore, cutover. For large databases
that is hours. Cut over by renaming (`modify-db-instance --new-db-instance-identifier`)
the old to `orders-old` and the new to `orders` so the endpoint DNS name stays the same,
or update application config / a Route 53 CNAME.

## 2. Low-downtime options
- **Read replicas do not help**: an RDS replica's encryption must match its source. Use
  logical replication instead: restore an encrypted copy from snapshot, then
  replicate changes since the snapshot with **DMS CDC** or native logical replication
  (binlog replication into the new instance for MySQL, `pglogical`/publication-subscription
  for PostgreSQL), then cut over with seconds to minutes of downtime.
- **Blue/green deployments** can create a green environment encrypted with a different KMS key than blue, which
  encrypts an unencrypted instance or changes the key with a short switchover (see the blue/green limitations
  page for your engine).
- Aurora: you cannot encrypt an unencrypted cluster snapshot by copying it. Restore the unencrypted
  snapshot into a new cluster and choose a KMS key (restore with `--kms-key-id`), or use a blue/green deployment.

## 3. Changing the KMS key
For an RDS instance, copy the snapshot specifying the new `--kms-key-id` and restore (a snapshot of an
encrypted instance always uses the instance's key until you copy it), or use blue/green. Use customer
managed keys from the start (needed for cross-account sharing).

## 4. Sharing encrypted snapshots
- Snapshots encrypted with the AWS managed key `aws/rds` **cannot be shared**. Copy with a
  customer managed key first.
- Create the customer managed key (symmetric, encrypt and decrypt) in the same Region as the snapshot and give the
  target account access to it in the key policy (console: "Other AWS accounts"); a key from another account also
  works if its policy grants both accounts access. See the "Sharing encrypted snapshots" page for the console steps.
- You can share a manual snapshot with up to 20 accounts; encrypted snapshots can never be public.
- Share:
```bash
aws rds modify-db-snapshot-attribute --db-snapshot-identifier orders-enc \
  --attribute-name restore --values-to-add 444455556666
```
- The target account copies the shared snapshot re-encrypting with its own key
  (`copy-db-snapshot --source-db-snapshot-identifier arn:aws:rds:...:snapshot:orders-enc
  --kms-key-id <target-key>`), then restores from its copy. Cross-region: copy with
  `--source-region` and a key in the destination region.
- Cluster snapshots (Aurora) use `modify-db-cluster-snapshot-attribute`.

## Gotchas
- Oracle and SQL Server snapshots encrypted with TDE cannot be shared, and a snapshot whose option group has
  permanent or persistent options cannot be shared (exceptions are listed on the share page).
- Automated snapshots (including AWS Backup ones) cannot be shared directly; copy them to manual snapshots first.
- Encrypted read replicas in another region need a KMS key in that region; an encrypted replica of an encrypted
  source can use a different key, but an unencrypted source cannot have an encrypted replica.
- When restoring from a shared snapshot with the CLI or API, use the snapshot ARN as the identifier; a snapshot
  that is both shared and encrypted cannot be restored directly, so copy it first.

## Verify
- [ ] `describe-db-instances --query 'DBInstances[].{id:DBInstanceIdentifier,enc:StorageEncrypted,key:KmsKeyId}'` shows encryption with the intended key.
- [ ] Application connects to the same endpoint name after cutover; data current.
- [ ] Target account restored the shared snapshot from its own re-encrypted copy.

## Checked
Date: 2026-10-27. Sources: RDS User Guide Overview.Encryption, USER_ShareSnapshot, share-encrypted-snapshot;
Aurora User Guide Overview.Encryption; botocore `rds` model (ModifyDBSnapshotAttribute, CopyDBSnapshot). Corrected the
blue/green claim (it can encrypt or re-key), the Aurora restore wording, and the TDE/option-group sharing limits; removed
the unconfirmed KMS action list and the unconfirmed `--option-group-name` advice.
Method: documentation only; no commands were run.
