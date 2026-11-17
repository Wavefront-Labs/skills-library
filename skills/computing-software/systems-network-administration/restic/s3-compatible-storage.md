---
id: computing-software.systems-network-administration.restic.s3-compatible-storage
name: s3-compatible-storage
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, s3-compatible, wasabi, alibaba-oss, bucket-lookup, region]
level: practitioner
status: docs-checked
description: "Use restic with S3-compatible services: endpoint URLs, region and bucket-lookup options, Wasabi, Alibaba OSS and Ceph workarounds."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3-compatible storage

For a non-Amazon endpoint put the full URL after `s3:`:

```
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
restic -r s3:https://server:port/bucket_name init
```

## Options

- `-o s3.region="us-east-1"` sets the region. The default is `us-east-1`.
- `-o s3.bucket-lookup=auto|dns|path` chooses addressing. `auto` uses DNS style for Amazon and Google and path style otherwise.
- `-o s3.list-objects-v1=true` works around Ceph older than v14.2.5. The docs note it may be removed later.

## Wasabi

```
restic -r s3:https://<WASABI-SERVICE-URL>/<WASABI-BUCKET-NAME> init
```

with the same AWS credential variables.

## Alibaba Cloud OSS

OSS needs DNS-style lookup and its own region name:

```
restic -o s3.bucket-lookup=dns -o s3.region=oss-eu-west-1 \
  -r s3:https://oss-eu-west-1.aliyuncs.com/<OSS-BUCKET-NAME> init
```

## Backblaze B2

The restic docs recommend Backblaze B2's S3-compatible API over the native B2 backend, because of error-handling issues in the B2 library restic uses. Create S3-compatible keys in Backblaze and set up restic as for S3. See the b2-backend skill for the native option.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (S3-compatible storage, Wasabi, Alibaba Cloud OSS, Backblaze B2 sections): `s3:https://server:port/bucket_name`, `AWS_DEFAULT_REGION` and `s3.region` with default `us-east-1`, the three `s3.bucket-lookup` values and the `auto` behaviour, `s3.list-objects-v1` for Ceph before v14.2.5 and the removal note, the Wasabi and OSS command lines. The OSS region shown is an example of the form the docs describe. Removed: the RESTIC_REPOSITORY and smoke-test advice (not in the docs).

Method: documentation only; no commands were run.
