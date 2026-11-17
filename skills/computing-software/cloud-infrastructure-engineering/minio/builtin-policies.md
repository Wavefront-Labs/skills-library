---
id: computing-software.cloud-infrastructure-engineering.minio.builtin-policies
name: builtin-policies
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, builtin-policies, consoleadmin, readonly, readwrite, writeonly, diagnostics, mc-admin-policy-attach]
level: intro
status: docs-checked
description: "Pick among MinIO built-in policies consoleAdmin, readonly, readwrite, writeonly and diagnostics, including why readonly omits listing."
sources: ["https://github.com/minio/docs/blob/main/source/administration/identity-access-management/policy-based-access-control.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO built-in policies

Assign with `mc admin policy attach ALIAS POLICY --user=...` (or to a group).

- `consoleAdmin` - everything: `s3:*` and `admin:*` on all resources.
- `readwrite` - read and write on all buckets and objects (`s3:*`).
- `readonly` - `s3:GetBucketLocation` and `s3:GetObject`. GET must target a specific object; listing is intentionally excluded so a read-only role cannot discover every bucket and object. Works for `mc cp`, `mc stat`, `mc head`, `mc cat` against a known path.
- `writeonly` - `s3:PutObject` to a specific location, without listing.
- `diagnostics` - `admin:ServerTrace`, `admin:Profiling`, `admin:ConsoleLog`, `admin:ServerInfo`, `admin:TopLocksInfo`, `admin:OBDInfo`, `admin:BandwidthMonitor`, `admin:Prometheus`.

Policies can be scoped to a bucket: the docs' example gives user `Operations` readwrite on `finance` and readonly on `audit`, user `Auditing` readonly on `audit`, and user `Admin` `admin:*` (all `mc admin` commands).

Write custom documents when the built-ins are too broad: `computing-software.cloud-infrastructure-engineering.minio.policy-based-access-control`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: policy and built-in policy pages: policy names, attach command. Removed or fixed: nothing.

Method: documentation only; no commands were run.
