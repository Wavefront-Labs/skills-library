---
id: computing-software.database-administration.influxdb.create-api-tokens-all-access-and-custom
name: create-api-tokens-all-access-and-custom
category: computing-software
field: database-administration
product: influxdb
tags: [tokens, influx-auth-create, operator-token, permissions, authorization]
level: practitioner
status: docs-checked
description: "Create All Access, operator and scoped read/write API tokens with influx auth create, and understand that token values and permissions are fixed at creation."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/create-token/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Rules InfluxDB enforces: a token is visible to the user who created it, the value is shown only right after creation, permissions cannot be changed afterwards, and tokens stop working if the creating user is deleted. Only tokens with `write: authorizations` can create tokens. The docs recommend a generic user to own write tokens and storing tokens in a password vault.

```sh
# all resources in one org
influx auth create --org my-org --all-access

# all resources in all orgs
influx auth create --org my-org --operator

# scoped read/write
influx auth create --org my-org \
  --read-buckets --write-buckets --read-dashboards --read-tasks
```

Add `--user USERNAME` to scope the token to a user. Permission flags follow a read/write pattern such as `--read-authorizations`, `--write-buckets`, `--read-dashboards`, `--read-tasks`, `--read-telegrafs` and `--write-users`.

Creating a new operator token after setup requires an existing operator token. Without one, use `influxd recovery auth` (see the credential recovery skill).

API: `POST /api/v2/authorizations` with `orgID` in the request body; pass `userID` to scope the token to a user other than the creator.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/admin/tokens/create-token/
- Scope: restrictions, influx auth create variants, operator-token caveat and API fields.
- Removed: the unconfirmed `permissions` array wording.
Method: documentation only; no commands were run.
