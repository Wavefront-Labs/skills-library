---
id: computing-software.systems-network-administration.duplicati.duplicati-s3-compatible-destination
name: duplicati-s3-compatible-destination
category: computing-software
field: systems-network-administration
product: duplicati
tags: [s3-destination, s3-client-minio, bucket-name, s3-disable-chunk-encoding, forcepathstyle, storage-class]
level: practitioner
status: docs-checked
description: "Configure Duplicati's S3-compatible destination, including bucket naming, SSL, choosing the AWS or Minio client and flags for non-AWS providers."
sources: ["https://docs.duplicati.com/backup-destinations/standard-based-destinations/s3-compatible-destination"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3-compatible destination

S3 stores objects in a top-level bucket; `/` in an object name acts as a subfolder for most providers. Bucket names are global across users on AWS and most providers, so a name like `backup` is likely taken and causes permission errors; AWS recommends a GUID in the name. Create the bucket before use, via the provider UI or, with Duplicati, `--s3-location-constraint` for the region (support varies).

The UI needs bucket, folder path, server, access key ID and secret access key (providers may call these username and password). CLI URL form:
`s3://<bucket>/<prefix>?aws-access-key-id=<id>&aws-secret-access-key=<key>&s3-server-name=<host>&use-ssl=true`
The default is unencrypted connections; requests are signed but data can be captured, so add `--use-ssl=true` where the provider supports TLS (most do).

Client: the AWS library by default, or the Minio library with `--s3-client=minio`. The AWS defaults may not suit other providers; Minio with defaults is often simpler.

Non-AWS providers often use an older protocol version, so set either `--s3-disable-chunk-encoding` or `--s3-client=minio`, but not both. Other options:
- `--s3-disable-payload-signing` (AWS client only)
- `--s3-authentication-region` (from 2.3.0.0; falls back to the location constraint)
- `--s3-recursive-list` to list objects in subfolders too
- `--s3-ext-<name>` passes AWS library settings, such as `--s3-ext-forcepathstyle=true`, which Duplicati sets automatically for servers not ending in `.amazonaws.com`.
`duplicati-cli help s3` lists them all. The storage class option tunes cost versus performance.

## Checked

2026-11-04. Confirmed against the S3-compatible Destination page. Nothing removed.

Method: documentation only; no commands were run.
