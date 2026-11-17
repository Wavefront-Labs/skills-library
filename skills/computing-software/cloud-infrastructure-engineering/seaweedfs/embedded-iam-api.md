---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.embedded-iam-api
name: embedded-iam-api
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [iam-api, embedded-iam, access-keys]
level: practitioner
status: docs-checked
description: "Manage S3 users, access keys and policies through the AWS IAM API embedded in the S3 server on port 8333; standalone weed iam is deprecated."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Amazon-IAM-API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# embedded iam api

The IAM API is embedded in the S3 server by default, on the same port (8333), as POST requests with an `Action` parameter at the root path.
```bash
weed s3 -filer=localhost:8888            # IAM on
weed s3 -iam=false -filer=localhost:8888 # disable
```
Standalone `weed iam -filer=localhost:8888 -port=8111` still works but is deprecated.

Actions include `CreateUser`, `DeleteUser`, `GetUser`, `UpdateUser`, `ListUsers`, `SetUserStatus`, `CreateAccessKey`, `DeleteAccessKey`, `UpdateAccessKey` (Active/Inactive), `ListAccessKeys` and policy operations. Admin-only except self-service ones: users can `GetUser` themselves and manage their own keys. `CreateAccessKey` can optionally take caller-supplied `AccessKeyId` and `SecretAccessKey`.

```bash
aws --endpoint-url http://localhost:8333 iam create-user --user-name alice
aws --endpoint-url http://localhost:8333 iam create-access-key --user-name alice
```
IAM configuration is stored on the filer at `/etc/iam/identity.json`; `echo 's3.configure' | weed shell` shows it. Before using the API, create an admin identity: `echo 's3.configure -access_key admin_key -secret_key admin_secret -user admin -actions Admin -apply' | weed shell`.

Verify: `aws iam list-users` returns the created user.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Amazon IAM API (raw markdown, read in full). A Kubernetes operator persistence claim was removed as unconfirmed.
