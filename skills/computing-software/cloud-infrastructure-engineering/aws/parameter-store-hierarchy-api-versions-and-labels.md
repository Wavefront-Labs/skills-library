---
id: computing-software.cloud-infrastructure-engineering.aws.parameter-store-hierarchy-api-versions-and-labels
name: parameter-store-hierarchy-api-versions-and-labels
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, parameter-store, get-parameters-by-path, parameter-labels, parameter-versions, ssm, configuration-management]
level: practitioner
status: docs-checked
description: "Read and manage Parameter Store config at scale: GetParametersByPath recursion and paging, version selectors, labels for promotion, throughput limits and IAM scoping."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-hierarchies.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-labels.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-throughput.html", "https://docs.aws.amazon.com/cli/latest/reference/ssm/get-parameters-by-path.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter Store: paths, versions and labels in practice

## 1. Hierarchy conventions
`/<app>/<env>/<component>/<key>`, e.g. `/billing/prod/db/host`. A hierarchy can have a
maximum of 15 levels. Keep secrets as `SecureString` under the same tree, or in Secrets Manager.

## 2. Reading a subtree
```bash
aws ssm get-parameters-by-path --path /billing/prod/ --recursive --with-decryption \
  --query 'Parameters[].{n:Name,v:Value,ver:Version}' --output table
```
- Without `--recursive` only direct children are returned.
- API returns max **10 parameters per page**; the CLI auto-paginates, SDKs do not unless
  you use the paginator (`get_paginator('get_parameters_by_path')` in boto3). Apps that
  call the raw API and ignore `NextToken` silently miss config.
- Filters: `--parameter-filters` takes `Key=...,Option=...,Values=...` (see the CLI reference
  for the valid keys of this operation).
- IAM: grant `ssm:GetParametersByPath` on the path ARN plus `kms:Decrypt` for SecureStrings.
  Per the hierarchies page, a user explicitly denied `/a/b` can still read it by calling
  `GetParametersByPath` recursively on `/a`, so scope IAM at the path.

## 3. Versions
Every `put-parameter --overwrite` creates a new version. Check the Parameter Store
versions documentation for the retention limit and the behaviour when old versions carry labels.
```bash
aws ssm get-parameter --name /billing/prod/db/host:3          # specific version
aws ssm get-parameter-history --name /billing/prod/db/host \
  --query 'Parameters[].{v:Version,mod:LastModifiedDate,by:LastModifiedUser}'
```

## 4. Labels for promotion
Labels are aliases on versions (a version can have a maximum of ten labels):
```bash
aws ssm label-parameter-version --name /billing/prod/feature-flags \
  --parameter-version 7 --labels approved
aws ssm get-parameter --name /billing/prod/feature-flags:approved
aws ssm unlabel-parameter-version --name /billing/prod/feature-flags \
  --parameter-version 7 --labels approved
```
Pattern: CI writes new versions freely; a release step moves the `approved` label; the
app reads `name:approved`. Rollback = move the label back. Labels can contain letters
(case sensitive), numbers, periods, hyphens and underscores; they cannot begin with a number,
`aws` or `ssm` (not case sensitive); max 100 characters.

## 5. Throughput and cost
- Default throughput: 40 TPS shared across `GetParameter`, `GetParameters` and
  `GetParametersByPath` combined. Higher throughput is a paid setting (per-operation
  maximums are on the throughput page; GetParameter is 10,000 TPS): `aws ssm update-service-setting --setting-id
  arn:aws:ssm:<region>:<acct>:servicesetting/ssm/parameter-store/high-throughput-enabled
  --setting-value true`.
- Better: cache values in the application with a TTL instead of calling on every request.
- Parameter tiers (`--tier Standard|Advanced|Intelligent-Tiering`) differ in value size, count
  and cost; see the Parameter Store tier documentation.

## Gotchas
- `get-parameters` (plural, by names, up to 10) returns unknown names in
  `InvalidParameters` instead of failing; check that list.

## Verify
- [ ] App config loader uses a paginator; a subtree with more than 10 params loads fully.
- [ ] Reading `name:approved` returns the expected version after a label move; rollback by relabel tested.
- [ ] No ThrottlingException in CloudTrail/app logs at peak (or high throughput enabled deliberately).

## Checked

2026-10-28. Confirmed against the Parameter Store hierarchies, labels and throughput pages, the get-parameters-by-path CLI page and the ssm botocore model: 15-level hierarchy maximum, 10 parameters per GetParametersByPath page (MaxResults max 10), InvalidParameters on GetParameters, ten labels per version, label character and prefix rules and 100-character limit, 40 TPS default shared by the three read APIs, GetParameter 10,000 TPS, high-throughput-enabled service setting, path-level IAM note, Tier enum. Removed (unconfirmed): case sensitivity, Secrets Manager reference path, 100-version retention and labelled-version put failure, Lambda extension port, tier sizes and upgrade direction, EventBridge detail-type, with-decryption and trailing-slash notes, filter examples. Read end to end.

Method: documentation only; no commands were run.
