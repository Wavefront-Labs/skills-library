---
id: computing-software.cloud-infrastructure-engineering.minio.users-and-access-keys
name: users-and-access-keys
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, users-and-access-keys, access-keys, service-accounts, mc-admin-user-add, svcacct, inline-policy, sts-expiry, internal-idp]
level: practitioner
status: docs-checked
description: "Manage MinIO internal IDP users and child access keys: parent policy inheritance, optional inline restriction, no Console login, and STS lifetime of 1 hour to 7 days."
sources: ["https://github.com/minio/docs/blob/main/source/administration/identity-access-management/minio-user-management.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO users and access keys

A user is an access key (username) plus secret key (password). Create one on the internal IDP:
```
mc admin user add ALIAS ACCESSKEY SECRETKEY
```
Users receive permissions from policies attached directly or inherited from groups.

## Access keys (formerly service accounts)
- Child identities of an authenticated user, including externally managed identities.
- Inherit the parent's effective policies, with an optional **inline policy** that can only narrow access.
- A user can create any number, letting application owners self-serve without admin action; created with `mc admin user svcacct add`.
- Programmatic access only: an access key cannot log in to the Console.
- No expiry; they live until removed or the parent is removed.
- Enabling external identity management (OIDC or LDAP) disables the internal IDP for users, but access key creation still works.

## STS
Temporary credentials can be created with the `AssumeRole` STS API endpoint. Tokens expire after 1 hour by default and can be set up to 7 days from creation.

## Site replication
Access keys sync between sites except those owned by `root` (`computing-software.cloud-infrastructure-engineering.minio.site-replication`). Root handling: `computing-software.cloud-infrastructure-engineering.minio.root-user`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: User Management page (minio-user-management.rst) and the site replication include (common-replication.rst) for the root access key exception. Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
