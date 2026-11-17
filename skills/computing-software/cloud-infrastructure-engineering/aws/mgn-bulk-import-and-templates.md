---
id: computing-software.cloud-infrastructure-engineering.aws.mgn-bulk-import-and-templates
name: mgn-bulk-import-and-templates
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, application-migration-service, mgn, mgn-import, bulk-import, launch-templates, migration-waves]
level: practitioner
status: gated
description: "Large migrations with AWS MGN: bulk import of servers, applications and waves from a CSV in S3, replication and launch templates, and post-launch actions."
sources: ["https://docs.aws.amazon.com/mgn/latest/ug/import-export.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MGN bulk import and templates

## Bulk import
Instead of configuring hundreds of source servers in the console, describe them in the import file:
- Download the import template from the MGN console and fill one row per server; use the column names from that template. (gated: unconfirmed, source is paywalled or blocked)
- Upload to S3 and import:
```bash
aws s3 cp mgn-import.csv s3://<BUCKET>/wave1.csv
aws mgn start-import --s3-bucket-source s3Bucket=<BUCKET>,s3Key=wave1.csv
aws mgn list-imports
aws mgn list-import-errors --import-id "$ID"
```
- Import creates/updates **applications** and **waves** and applies launch settings to source servers. (gated: unconfirmed, source is paywalled or blocked)
- Export the current state (`start-export`) for review in a spreadsheet; edit and re-import to change in bulk.

## Replication template
Same model as DRS. Set it before installing agents: new servers inherit it. (gated: unconfirmed, source is paywalled or blocked)

## Launch template
- MGN keeps an EC2 launch template per source server; the MGN **launch settings** drive it. (gated: unconfirmed, source is paywalled or blocked)
- Default launch template for the account sets organisation-wide defaults (subnet per wave, SGs, instance profile, tags).

## Post-launch actions
SSM documents run on test and cutover instances, with custom actions per application. (gated: unconfirmed, source is paywalled or blocked)

## Wave flow
1. Import wave file, install agents (or agentless vCenter replication), wait for initial sync.
2. Launch **test** instances per wave, run validation, mark ready for cutover.
3. **Cutover** window: final sync, launch cutover instances, switch DNS, finalise, archive the source servers. (gated: unconfirmed, source is paywalled or blocked)

## Gotchas
- Import file column names and allowed values must match the template version exactly; errors are listed by `list-import-errors`.
- Keep waves small until the process is stable.

## Verify
- [ ] Import has zero errors; applications and waves visible with correct servers.
- [ ] Test launch of a wave passes post-launch validation actions.

## Checked

2026-10-28

Confirmed: start-import with s3BucketSource (s3Bucket, s3Key ending .csv), list-imports, list-import-errors --import-id, StartExport operation (botocore mgn, check_commands).

Removed: console menu path, import column list, bucket example with an account-number-like name, per-row error claim, overwrite-on-reimport claim, wave size range, DRS-parity and finalise details.

Gated: template contents, launch template, post-launch actions and cutover finalise: the fetched import-export page is short and the other cited pages were prose-only.

Method: documentation only; no commands were run.
