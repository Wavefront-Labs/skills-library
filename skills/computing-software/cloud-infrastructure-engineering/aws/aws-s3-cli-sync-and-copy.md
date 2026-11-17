---
id: computing-software.cloud-infrastructure-engineering.aws.aws-s3-cli-sync-and-copy
name: aws-s3-cli-sync-and-copy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, s3-commands, s3-sync, s3-cp, multipart-upload, crt, data-transfer]
level: practitioner
status: docs-checked
description: "Move data with aws s3 cp, sync, mv and rm: filter ordering, --delete safety, metadata and storage class flags, concurrency and multipart tuning, CRT, sync edge cases."
sources: ["https://github.com/aws/aws-cli/blob/v2/awscli/examples/s3/_concepts.rst", "https://github.com/aws/aws-cli/blob/v2/awscli/topics/s3-config.rst", "https://github.com/aws/aws-cli/blob/v2/awscli/customizations/s3/subcommands.py", "https://github.com/aws/aws-cli/tree/v2/awscli/customizations/s3/syncstrategy", "https://docs.aws.amazon.com/cli/latest/reference/s3/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `aws s3` cp, sync, mv, rm

## 1. Everyday commands
```bash
aws s3 cp build/app.zip s3://artifacts/app/1.4.2/app.zip --sse aws:kms --sse-kms-key-id alias/artifacts
aws s3 cp s3://logs/2026/10/ ./logs --recursive --exclude "*" --include "*.gz"
aws s3 sync ./site s3://site-bucket --delete --cache-control "max-age=31536000,immutable" --exclude "index.html"
aws s3 cp ./site/index.html s3://site-bucket/index.html --cache-control "no-cache"
aws s3 sync s3://src-bucket s3://dst-bucket --storage-class STANDARD_IA --source-region us-east-1
aws s3 rm s3://scratch/tmp/ --recursive --dryrun
```

## 2. Filters
Filters support `*`, `?`, `[sequence]` and `[!sequence]`. Filters that appear **later on the command line take precedence**, and each is evaluated against the source directory (the source path is prepended to the pattern). By default everything is included, so `--include` alone changes nothing: `--exclude "*" --include "*.csv"` = only CSVs, while `--include "*.csv" --exclude "*"` excludes everything. Quote patterns so the shell doesn't expand them.

## 3. sync semantics
- A file is synced when it is missing at the destination, its size differs, or its modification time differs in the direction the CLI treats as newer. When syncing S3 to local, same-sized items are skipped unless the local version is older than the S3 version; `--exact-timestamps` skips them only when the timestamps match exactly. `--size-only` compares sizes only.
- A same-size change with an unchanged or older timestamp can therefore be missed; for correctness-critical copies verify with another method or use `cp --recursive`.
- `--delete` removes destination files absent in source — **always run with `--dryrun` first**.

## 4. Performance tuning (`~/.aws/config`)
```ini
[default]
s3 =
  max_concurrent_requests = 32
  multipart_threshold = 64MB
  multipart_chunksize = 64MB
  preferred_transfer_client = crt
  target_bandwidth = 5GB/s
```
- `max_concurrent_requests`, `multipart_threshold` and `multipart_chunksize` apply to the classic transfer client; see `aws help topics s3-config`.
- `preferred_transfer_client` defaults to `auto`, which resolves to `crt` only when criteria are met: not an S3-to-S3 copy, no other CLI process already using CRT, and (except on certain large instance types) none of `max_bandwidth`, `retry_mode = adaptive`, `max_attempts` outside 2 to 64, or an upload from a non-seekable stream. Otherwise the `classic` client is used. Set the value explicitly if you need a specific client.
- `target_bandwidth` is supported only with the `crt` client (units such as `MB/s`, `GB/s`, `Gb/s`); `max_bandwidth` is not supported by CRT on most hosts.

## 5. Useful flags
`--only-show-errors`, `--no-progress` (CI logs), `--metadata key=val`, `--content-type`,
`--acl bucket-owner-full-control` (requires `s3:PutObjectAcl`), `--request-payer requester`,
`--expected-size` (needed only for stream uploads larger than 50 GB: `tar c dir | aws s3 cp - s3://b/x.tar --expected-size 200000000000`). Stream uploads (`cp -`) are not supported by the CRT client.

## Gotchas
- For S3-to-S3 copies, `--copy-props` (`none`, `metadata-directive`, `default`, `all`) controls which properties are copied; the CLI help recommends it over `--metadata-directive`, and setting `--metadata-directive` disables `--copy-props`. Check object headers after a copy.
- With S3-to-S3 transfers, `--source-region` names the source bucket's region; `--region` refers to the destination.

## Verify
- [ ] `aws s3 sync ... --dryrun` output reviewed before any `--delete` run.
- [ ] Object count/size match after transfer (`aws s3 ls --recursive --summarize`).
- [ ] Transfer throughput meets target after tuning.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch (s3 high-level concepts, s3-config topic, s3 subcommand argument definitions, sync strategy classes).
Confirmed: filter wildcard syntax, later-filter precedence, evaluation against the source directory, default include-all behaviour; sync decision logic and --exact-timestamps behaviour; existence of --delete, --size-only, --dryrun, --only-show-errors, --no-progress, --metadata, --content-type, --acl (needs s3:PutObjectAcl), --request-payer, --expected-size (streams over 50 GB), --source-region, --copy-props and --metadata-directive; S3 config keys including preferred_transfer_client auto-resolution rules and target_bandwidth units.
Corrected: preferred_transfer_client = crt does not apply to S3-to-S3 copies or stream uploads and other CRT limits; the earlier throughput claim and the 5GB/s example were rewritten.
Removed as unconfirmed: empty-directory note, mv atomicity note, KMS permission note, 10,000-part chunk limit.
Method: documentation only; no commands were run.
