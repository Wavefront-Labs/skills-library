---
id: computing-software.cloud-infrastructure-engineering.aws.opensearch-snapshots-and-restore
name: opensearch-snapshots-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, opensearch, opensearch-snapshots, snapshot-repository, snapshot-management, restore, disaster-recovery]
level: practitioner
status: docs-checked
description: "Back up and restore Amazon OpenSearch Service domains: automated vs manual snapshots, registering an S3 repository with a passed role, snapshot management and restores."
sources:
  - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html
  - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshot-registerdirectory.html
  - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshot-create.html
  - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshot-restore.html
  - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshot-mgmt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSearch snapshots and restore

## Automated vs manual
| | Automated | Manual |
|---|---|---|
| Who | the service, hourly (OpenSearch, or Elasticsearch 5.3+) | you |
| Where | service-managed repository `cs-automated` (`cs-automated-enc` when the domain encrypts data at rest) | your S3 bucket |
| Retention | up to 336 snapshots, kept 14 days | your lifecycle |
Use manual snapshots for DR, migrations and long retention.

## Register a manual repository
1. Create an IAM role that OpenSearch Service can assume (trust principal `es.amazonaws.com`) with access to the S3 bucket.
2. The caller needs `iam:PassRole` on that role and the `es:ESHttpPut` action. With fine-grained access control, map the `manage_snapshots` role to the IAM role or user doing the registration.
3. Send the registration `PUT _snapshot/<REPOSITORY_NAME>` as a **SigV4-signed** request (the guide's example uses Python with `requests-aws4auth`), with body `{"type":"s3","settings":{"bucket":"<BUCKET>","region":"<REGION>","role_arn":"<ROLE_ARN>"}}`.
4. If the domain is in a VPC, your machine must be connected to the VPC for the request to succeed.

## Take and schedule
- Take a manual snapshot with `PUT _snapshot/<REPOSITORY_NAME>/<SNAPSHOT_NAME>` (see "Taking manual snapshots").
- Snapshots are incremental: they store only data changed since the last successful snapshot.
- Snapshot Management (SM) policies automate creation and deletion on a schedule; follow the SM page for the policy API and its fields.

## Restore
- Restore with `POST _snapshot/<REPOSITORY_NAME>/<SNAPSHOT_NAME>/_restore`, restricting `indices` and setting `include_global_state` to `false` unless you intend a whole-domain restore.
- You cannot restore an index into a cluster that already has an index of the same name: delete it first, or use `rename_pattern` and `rename_replacement` to restore under a new name.
- Exclude system and security indices from partial restores (the guide's examples use `-.kibana*,-.opendistro*`).
- Automated snapshots live in the `cs-automated` repository; if you cannot see your manual repository, register it first.

## Verify
- [ ] A scheduled snapshot exists in the manual repository with a recent successful state.
- [ ] Quarterly restore test into a scratch domain with document counts compared.

## Checked
2026-10-28. Confirmed in the OpenSearch Service Developer Guide pages "Creating index snapshots", "Registering a manual snapshot repository", "Taking manual snapshots" and "Restoring data from snapshots": hourly automated snapshots, 336 retained for 14 days, `cs-automated` / `cs-automated-enc`, trust principal `es.amazonaws.com`, `iam:PassRole` plus `es:ESHttpPut`, `manage_snapshots` mapping, VPC reachability, incremental snapshots, same-name restore conflict and rename parameters, `-.kibana*,-.opendistro*` exclusion.
Removed as unconfirmed: the "cost: free" and cross-domain restore rows, the exact S3 action list, `opensearchservice.amazonaws.com` as a trust principal, the curl `--aws-sigv4` command, the SM policy JSON, `wait_for_completion`, the closed-index and version-compatibility restore rules.
Method: documentation only; no commands were run.
