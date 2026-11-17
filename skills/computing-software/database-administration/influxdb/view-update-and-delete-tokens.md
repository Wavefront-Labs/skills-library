---
id: computing-software.database-administration.influxdb.view-update-and-delete-tokens
name: view-update-and-delete-tokens
category: computing-software
field: database-administration
product: influxdb
tags: [tokens, influx-auth-list, influx-auth-delete, token-status, authorization]
level: practitioner
status: docs-checked
description: "List tokens, disable or re-enable them with influx auth inactive and active, change a description, and delete a token by authorization ID."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/view-tokens/
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/update-tokens/
  - https://docs.influxdata.com/influxdb/v2/admin/tokens/delete-token/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

List and inspect:

```sh
influx auth list
influx auth find --json   # JSON output shows each token status
```

Tokens are visible to their creator; a user with an operator token sees all tokens. Full token values are only shown at creation. API: `GET /api/v2/authorizations` (add `userID`, or with an operator token `org`/`orgID`, to filter) and `GET /api/v2/authorizations/{authID}`.

Enable or disable (needs the authorization ID):

```sh
influx auth inactive -i 0804f74142bbf000
influx auth active   -i 0804f74142bbf000
```

API: `PATCH /api/v2/authorizations/{authID}` with `{"description": "...", "status": "inactive"}`. The caller needs `write: authorizations`.

Delete:

```sh
influx auth delete -i 03a2bee5a9c9a000
```

Deletion is immediate: every user and integration using that token loses access. Prefer `inactive` first to see what breaks, then delete.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages view-tokens, update-tokens and delete-token, article bodies (lines 570-640) read from the downloaded text.

Confirmed: visibility rules and UI note, `influx auth list|find --json|active|inactive|delete -i`, API paths and the `write: authorizations` permission, immediate loss of access on deletion. The `read: authorizations` permission applies to the GET endpoints. The "inactive before delete" ordering is the skill's own advice.
