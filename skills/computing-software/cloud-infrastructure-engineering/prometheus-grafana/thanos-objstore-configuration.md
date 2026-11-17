---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-objstore-configuration
name: thanos-objstore-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos-objstore-config, objstore-yml, thanos, object-storage, s3, gcs]
level: practitioner
status: docs-checked
description: "Write the Thanos objstore config for S3, GCS and Azure, understand the credential lookup order, share it across sidecar, store and compactor, and test it with tools bucket ls."
sources: ["https://thanos.io/tip/thanos/storage.md/", "https://thanos.io/tip/components/tools.md/#bucket-ls", "https://thanos.io/tip/components/sidecar.md/", "https://thanos.io/tip/components/compact.md/#vertical-compactions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos objstore configuration

Components that use the bucket take `--objstore.config-file` (a path) or `--objstore.config` (the YAML inline); the docs
recommend the inline form because it gives an explicit static view per component, though the S3 section calls the file
form preferable. Each component reads exactly one bucket: with a multi-document YAML (documents separated by `---`) only
the first is used and the rest are silently ignored. To use different buckets run separate component instances, each with
its own configuration.

## S3 (and compatible)
```yaml
type: S3
config:
  bucket: <bucket>
  endpoint: s3.<region>.amazonaws.com
  region: <region>
  insecure: false
  bucket_lookup_type: auto
  part_size: 67108864
  sse_config:
    type: SSE-S3
```
- `part_size` is in bytes and is the minimum file size for multipart uploads; 0 means the default 128 MiB. The sample
  value above comes from the docs' reference block.
- `bucket_lookup_type` can be `auto`, `virtual-hosted` or `path`.
- `insecure: true` switches to plain HTTP; `http_config.insecure_skip_verify: true` disables certificate verification
  (for self-signed certificates).
- `sse_config` supports `SSE-S3` (no other options needed), `SSE-KMS` and `SSE-C`; a block with another type raises an
  error.
- Credential lookup: access_key and secret_key from the config file if both are present; then the
  `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` environment variables; then `~/.aws/credentials`; then IAM credentials from an
  instance profile (which needs AWS STS; a custom STS endpoint can be set). Taking the access key from the file and the
  secret from elsewhere (or the reverse) is not supported.

## GCS
```yaml
type: GCS
config:
  bucket: <bucket>
  service_account: ""     # inline JSON; the docs also say to configure Google Application credentials
```

## Azure
```yaml
type: AZURE
config:
  storage_account: <account>
  container: <container>
  storage_account_key: ""   # or user_assigned_id for a user-assigned managed identity
```
With `storage_account_key` authentication uses the key; with `user_assigned_id` a user-assigned managed identity. If
neither is set, Thanos tries these credential types in order and stops at the first that yields a token:
EnvironmentCredential, WorkloadIdentityCredential, ManagedIdentityCredential, AzureCLICredential (the first three need
the right environment variables). The storage account must be created beforehand.

## Test
```bash
thanos tools bucket ls --objstore.config-file=objstore.yml
thanos tools bucket inspect --objstore.config-file=objstore.yml
```
`bucket ls` lists all blocks in the bucket (`-o json` for JSON); `bucket inspect` prints a detailed ASCII table.

## Rules from the docs
- Only one instance of Compactor may run against a single stream of blocks in a single object storage.
- The sidecar uploads TSDB blocks to the bucket as Prometheus produces them every 2 hours, and requires `--objstore.*`
  flags to do so.

## Checked

Checked 2026-11-08 against the Thanos storage page (S3, GCS, Azure sections), the Thanos tools page (`bucket ls` and
`bucket inspect`), the sidecar page and the Compact warning. Removed because the pages do not state them: MinIO/Ceph
endpoint examples, the Prometheus Operator `objectStorageConfig` snippet, the advice against bucket lifecycle rules and on
versioned buckets, IRSA and Workload Identity for GCS, the failure-counter metric name and the "2-4 hours" timing.
Method: docs-only read of cited pages, 2026-11-08
