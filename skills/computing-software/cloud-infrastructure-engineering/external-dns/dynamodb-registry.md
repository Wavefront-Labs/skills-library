---
id: computing-software.cloud-infrastructure-engineering.external-dns.dynamodb-registry
name: dynamodb-registry
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, dynamodb-registry, dynamodb-table, registry-dynamodb, txt-migration-to-dynamodb]
level: advanced
status: docs-checked
description: "Keep ExternalDNS ownership metadata in an AWS DynamoDB table instead of TXT records: table schema, IAM actions, flags, verification scan and migration from TXT."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/dynamodb.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamoDB registry

Stores record metadata in a DynamoDB table rather than TXT records in the hosted zone.

**Table** (default name `external-dns`, must exist beforehand). It needs a string HASH key named `k` and **no** sort key:
```bash
aws dynamodb create-table --table-name external-dns \
  --attribute-definitions AttributeName=k,AttributeType=S \
  --key-schema AttributeName=k,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --table-class STANDARD
```

**IAM:** in addition to the Route 53 policy, allow `DynamoDB:DescribeTable`, `DynamoDB:PartiQLDelete`, `DynamoDB:PartiQLInsert`, `DynamoDB:PartiQLUpdate`, `DynamoDB:Scan` on `arn:aws:dynamodb:*:*:table/external-dns` (region and account may be explicit).

**Flags:** change `--registry=txt` to `--registry=dynamodb`; `--dynamodb-table=external-dns` (default); `--dynamodb-region=us-east-1` if the table is in another region; keep `--txt-owner-id`.

**Verify** after about two minutes:
```bash
aws dynamodb scan --table-name external-dns
```
Items look like key `nginx.example.com#A#`, owner `o`, and labels `l` with `resource` = `service/default/nginx`.

**Caching:** `--txt-cache-interval` works as with the TXT registry.

**Migrating from TXT:** existing ownership TXT records for the configured owner are migrated into the table. If any exist, supply the previous `--txt-prefix`, `--txt-suffix`, `--txt-wildcard-replacement` and `--txt-encrypt-aes-key`. If TXT is in `--managed-record-types`, the TXT records are deleted on a later reconcile.

**Clean up:** also run `aws dynamodb delete-table --table-name external-dns`.

## Checked

2026-11-04. Read the DynamoDB registry page. Confirmed the table schema (HASH key k of type S, no sort key), the create-table example, the five IAM actions, the flags and defaults, the scan output shape, caching via --txt-cache-interval and the TXT migration rules. Removed the unsupported claim that the registry helps with rate limits.

Method: documentation only; no commands were run.
