---
id: computing-software.database-administration.influxdb.add-and-delete-secrets
name: add-and-delete-secrets
category: computing-software
field: database-administration
product: influxdb
tags: [secrets, influx-secret-update, influx-secret-delete, orgs-secrets-api]
level: practitioner
status: docs-checked
description: "Store and remove per-org secret key-value pairs with influx secret update and delete, or the orgs/{orgID}/secrets API, without leaking values into shell history."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/secrets/add/
  - https://docs.influxdata.com/influxdb/v2/admin/secrets/delete/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Add or change a secret:

```sh
influx secret update -k foo          # prompts for the value
```

`-k/--key` names the secret. `-v/--value` provides it inline, but that may expose the secret in command history, so prefer the prompt.

API: `PATCH /api/v2/orgs/<org-id>/secrets` with the key-value pair as the JSON body.

Delete:

```sh
influx secret delete -k foo
```

API: `POST /api/v2/orgs/<org-id>/secrets/delete` with `{"secrets": ["<secret-key>"]}`. (The page's curl sample shows GET, but the text says POST; use POST.)

Secrets belong to an organization; both API calls take the organization ID in the URL and your API token in the `Authorization` header.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages "Add secrets" and "Delete secrets", article bodies (lines 574-605) read from the downloaded text.

Confirmed: `influx secret update` and `delete` with `-k`, the prompt for the value and the history warning on `-v`, PATCH and POST endpoints and bodies, and the page's GET-versus-POST inconsistency in the delete curl sample. Removed: the `secrets.get()` Flux advice, which these pages do not mention.
