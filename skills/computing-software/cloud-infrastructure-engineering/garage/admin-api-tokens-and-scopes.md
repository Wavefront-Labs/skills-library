---
id: computing-software.cloud-infrastructure-engineering.garage.admin-api-tokens-and-scopes
name: admin-api-tokens-and-scopes
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [admin-token, admin-token-create, token-scope, bearer-token]
level: advanced
status: docs-checked
description: "Authenticate the admin API with bearer tokens and create expiring, scoped tokens with garage admin-token create."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/admin-api/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The admin API listens on the address set by `api_bind_addr` in `[admin]`. The current version is v2 (v1 and v0 are deprecated), and breaking changes will only appear in major releases.

Authentication is an HTTP bearer header: `Authorization: Bearer <token>`.

Since v2.0.0, administrators can define tokens dynamically with the `garage admin-token` commands. A token can be limited in scope to a subset of API calls and can expire. The page's example:

`garage admin-token create --expires-in 30d --scope ListBuckets,GetBucketInfo,ListKeys,GetKeyInfo,CreateBucket,CreateKey,AllowBucketKey,DenyBucketKey my-token`

The secret is shown only once. Internally it is hashed and identified by its prefix, 32 hex digits followed by a dot. `garage admin-token list` shows ID, creation date, name, expiration and scope.

Master tokens in the config file still work but are discouraged: `admin_token` (all endpoints except metrics; if unset, only user-defined tokens can access them) and `metrics_token`. Config `admin_token` acts as an unexpiring full-scope token. Before v2.0 an unset token disabled the endpoints.

Quick check: `curl -H 'Authorization: Bearer s3cr3t' http://localhost:3903/v2/GetClusterStatus`.

## Checked

2026-11-04. Read the Administration API and Configuration file format pages in full. Confirmed the v2 API and deprecations, the bearer header, the create example, hashing and prefix identification, the list columns, master token behaviour and the pre-v2.0 behaviour. Nothing removed.
Method: documentation only; no commands were run.
