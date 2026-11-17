---
id: computing-software.cloud-infrastructure-engineering.terraform.s3-compatible-storage-as-a-state-backend
name: s3-compatible-storage-as-a-state-backend
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, s3-compatible, minio-backend, skip-credentials-validation, cloudflare-r2, digitalocean-spaces]
level: practitioner
status: docs-checked
description: "Use the s3 backend with MinIO, Cloudflare R2, DigitalOcean Spaces or Ceph: endpoints, skip_* flags, path-style addressing, checksums and locking caveats."
sources: ["https://developer.hashicorp.com/terraform/language/backend/s3", "https://developers.cloudflare.com/terraform/advanced-topics/remote-backend/", "https://docs.digitalocean.com/products/spaces/reference/terraform-backend/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3-compatible storage with the `s3` backend

```hcl
terraform {
  backend "s3" {
    bucket = "tfstate"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"                  # Spaces example uses us-east-1; R2 uses "auto"
    endpoints = { s3 = "https://<accountid>.r2.cloudflarestorage.com" }

    skip_credentials_validation = true    # no STS
    skip_requesting_account_id  = true    # no IAM/STS account lookup
    skip_metadata_api_check     = true    # no EC2 IMDS
    skip_region_validation      = true    # non-AWS region names
    skip_s3_checksum            = true    # "useful for some S3-compatible APIs"; R2 and Spaces examples set it
    use_path_style              = true    # the R2 example sets it
    use_lockfile                = true    # lock file in the same bucket (Spaces example needs Terraform ~> 1.11)
  }
}
```
Credentials: use the `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` environment variables
(DigitalOcean recommends this). Passing credentials with `-backend-config` or hard-coding
them can write them into the `.terraform` directory and plan files.

## Version notes
- `endpoint` and `force_path_style` are deprecated: use `endpoints = { s3 = ... }` and
  `use_path_style`.
- DigitalOcean's Spaces guide requires Terraform 1.6.3 or later for this configuration.
- HashiCorp only tests the `s3` backend against Amazon S3; support for S3-compatible
  providers is "best effort".

## Locking
- `use_lockfile` (default false) stores a lock file (`<key>.tflock`) beside the state; the
  identity needs GetObject, PutObject and DeleteObject on it. DigitalOcean documents it for
  Spaces; test it against your store before trusting it.
- `dynamodb_table` locking is deprecated in the s3 backend and is AWS-specific. Serialise
  pipelines (concurrency groups) as a fallback.

| Store | Notes |
|---|---|
| Cloudflare R2 | region `auto`, endpoint `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`, all `skip_*` flags and `use_path_style` as above; bucket-scoped token with Object Read and Write |
| DigitalOcean Spaces | endpoint `https://<region>.digitaloceanspaces.com` (for example `nyc3`), region `us-east-1`, `skip_*` flags as above |
| MinIO, Ceph | not covered by the fetched docs; test the `skip_*` and path-style settings yourself |

## Verify
- [ ] `terraform init -reconfigure` then `plan` works from a clean machine.
- [ ] Concurrent plan gets a lock error (if `use_lockfile`).

## Checked
- 2026-10-28. Confirmed against the Terraform `s3` backend page (`skip_credentials_validation`, `skip_region_validation`, `skip_requesting_account_id`, `skip_metadata_api_check`, `skip_s3_checksum`, `use_path_style`, `use_lockfile` default false and required permissions, deprecated `endpoint` / `force_path_style` / `dynamodb_table`, best-effort note), Cloudflare's "Remote R2 backend" page and DigitalOcean's Spaces backend page (settings, region values, Terraform 1.6.3 and ~> 1.11 requirements, environment-variable credentials).
- Removed: the Terraform 1.6 rename claim, the AWS SDK v2 checksum explanation and error symptoms, conditional-write wording, and MinIO and Ceph specifics (not in the fetched docs).
Method: documentation only; no commands were run.
