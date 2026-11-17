---
id: computing-software.cloud-infrastructure-engineering.aws.lake-formation-cross-account-sharing
name: lake-formation-cross-account-sharing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lake-formation, lf-cross-account, resource-links, lf-tags, data-sharing, ram]
level: practitioner
status: docs-checked
description: "Share data lake tables across accounts with Lake Formation: named-resource vs LF-Tag grants, RAM shares, resource links and recipient grants."
sources:
  - https://docs.aws.amazon.com/lake-formation/latest/dg/cross-data-sharing-lf.html
  - https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account-data-share-steps.html
  - https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account-prereqs.html
  - https://docs.aws.amazon.com/lake-formation/latest/dg/optimize-ram.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lake Formation cross-account sharing

## Two grant methods
| Method | How |
|---|---|
| Named resource | grant permissions on a database or table directly to an external AWS account, IAM principal, organization or OU |
| LF-Tag based | tag databases, tables or columns and grant on tag expressions ("Data sharing using tag-based access control") |

## Producer (data owner) account
- Before granting cross-account, revoke all Lake Formation permissions from the `IAMAllowedPrincipals` group on the resource.
- The grantor needs IAM permissions on AWS Glue and AWS RAM (the guide's prerequisites name the `AWSLakeFormationCrossAccountManager` managed policy).
```bash
aws lakeformation grant-permissions --principal DataLakePrincipalIdentifier=<CONSUMER_ACCOUNT_ID> \
  --resource '{"Table":{"DatabaseName":"sales","Name":"orders"}}' \
  --permissions SELECT DESCRIBE --permissions-with-grant-option SELECT DESCRIBE
```
- Lake Formation uses AWS Resource Access Manager (RAM) to share the resources; data stays in the producer's account.

## Consumer account
1. The data lake administrator accepts the RAM share (needs the RAM-accept policy from the prerequisites page).
2. Create a **resource link** in the local Data Catalog; Athena and Redshift Spectrum cannot query shared resources without one:
```bash
aws glue create-database --database-input '{"Name":"sales_shared","TargetDatabase":{"CatalogId":"<PRODUCER_ACCOUNT_ID>","DatabaseName":"sales"}}'
```
3. The administrator grants `DESCRIBE` on the resource link and the needed permissions on the original (target) resource to local principals.
4. Query through the link, for example in Athena: `SELECT * FROM sales_shared.orders`.

## Fine-grained
Tables can be shared with data filters that restrict access at row and cell level.

## Gotchas
- Cross-account version settings change how shares are created; read "Updating cross-account data sharing version settings" before changing them.

## Verify
- [ ] Consumer analyst can query the shared table via the resource link and cannot see data outside the filter.

## Checked
2026-10-28. Confirmed on the Lake Formation Developer Guide pages "Cross-account data sharing in Lake Formation", "Prerequisites", the data-sharing steps page and the version-settings page: grant targets (account, principal, organization, OU), RAM mechanism, `IAMAllowedPrincipals` revocation, resource link requirement for Athena/Redshift Spectrum, administrator grants `DESCRIBE` on the link plus permissions on the target, data filters at row and cell level; `check_commands.py` accepted the CLI commands.
Removed as unconfirmed: the cross-account "version 4" claim, auto-accept within an organization, S3 location registration and KMS notes, the engine list beyond Athena and Redshift Spectrum, the re-share rule, new-table tag inheritance, the CloudTrail `GetDataAccess` check.
Method: documentation only; no commands were run.
