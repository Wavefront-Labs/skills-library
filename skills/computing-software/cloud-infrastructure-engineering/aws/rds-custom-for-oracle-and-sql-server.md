---
id: computing-software.cloud-infrastructure-engineering.aws.rds-custom-for-oracle-and-sql-server
name: rds-custom-for-oracle-and-sql-server
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, rds-custom, oracle, sql-server, custom-engine-version]
level: advanced
status: docs-checked
description: "Decide when RDS Custom fits (OS and DB customisation for Oracle and SQL Server), and operate it: CEVs, automation pause, support perimeter and prerequisites."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-custom.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-managing.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS Custom

**End of support notice (read first):** the RDS User Guide states that AWS ends support for Amazon RDS Custom for
Oracle on 2027-03-31; after that date the RDS Custom for Oracle console and resources are no longer accessible. AWS
recommends migrating to Oracle on EC2 (RMAN active duplication or Data Guard) between 2026-03-31 and that date. Do not
start new RDS Custom for Oracle projects; the Oracle sections below are for operating or migrating existing
instances. RDS Custom for SQL Server is not covered by that notice (re-check the User Guide).

## 1. When
Applications needing OS access or privileges plain RDS forbids: custom patches, third-party agents, SQL Server
features requiring sysadmin or OS components. Otherwise use standard RDS.

## 2. Prerequisites
- Customer managed symmetric encryption KMS key.
- IAM role `AWSRDSCustomInstanceRole-<region>` in instance profile `AWSRDSCustomInstanceProfile-<region>` (the
  Oracle setup page creates these with CloudFormation templates); VPC connectivity (endpoints or NAT) to the
  dependent AWS services, as listed on the setup page for your engine.
- Oracle: build a **Custom Engine Version (CEV)** from your installation media and patches in S3:
```bash
aws rds create-custom-db-engine-version --engine custom-oracle-ee --engine-version 19.my_cev1 \
  --database-installation-files-s3-bucket-name oracle-media-<ACCOUNT_ID> --kms-key-id <KEY_ARN> \
  --manifest file://manifest.json
```
SQL Server: License Included (LI) or Bring Your Own Media (BYOM, you install your own binaries and licensing);
the User Guide describes a CEV (binary volume snapshot plus AMI) versus the RDS provided engine version. Oracle
always uses your own media and licences. Engine names include `custom-oracle-ee`, `custom-oracle-ee-cdb`,
`custom-sqlserver-ee`, `custom-sqlserver-se`, `custom-sqlserver-web` and `custom-sqlserver-dev` (RDS API model).

## 3. Pausing automation for changes
```bash
aws rds modify-db-instance --db-instance-identifier ebs-prod --automation-mode all-paused \
  --resume-full-automation-mode-minutes 120
# connect via SSM, make OS/DB changes
aws rds modify-db-instance --db-instance-identifier ebs-prod --automation-mode full
```
While paused, RDS does not monitor or recover the instance.

## 4. Support perimeter
RDS Custom monitors a support perimeter. A change that takes the host or database outside it moves the instance
to `unsupported-configuration` until you fix the configuration (see the "RDS Custom support perimeter" page).
TDE on RDS Custom for Oracle is turned on manually, not through an option group.

## 5. Still managed by RDS
Automation of routine administration (backups, monitoring, recovery) while automation mode is `full`.

## Verify
- [ ] Instance `available`, automation `full`, automated backups present.

## Checked
Date: 2026-10-27. Sources: RDS User Guide pages rds-custom, custom-managing, custom-setup-orcl,
RDS-Custom-for-Oracle-end-of-support; botocore `rds` model (`AutomationMode` enum `full`/`all-paused`,
`ResumeFullAutomationModeMinutes`, CreateCustomDBEngineVersion members). Confirmed the end of support date, role and
profile names, LI/BYOM licensing, support perimeter status. Removed unconfirmed specifics (named causes of
unsupported-configuration, Multi-AZ and PITR claims, Oracle E-Business Suite example).
Method: documentation only; no commands were run.
