---
id: computing-software.database-administration.influxdb.map-influxdb-1x-databases-with-dbrp
name: map-influxdb-1x-databases-with-dbrp
category: computing-software
field: database-administration
product: influxdb
tags: [dbrp, influxql, v1-api, retention-policy, compatibility]
level: practitioner
status: docs-checked
description: "Map a database and retention policy to a v2 bucket so InfluxQL and v1 write clients work, with the CLI and API forms."
sources:
  - https://docs.influxdata.com/influxdb/v2/query-data/influxql/dbrp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

InfluxQL and the v1 `/write` endpoint address data by database and retention policy (DBRP). A DBRP mapping points one pair at one bucket.

Mappings arise from: the v1 write endpoint (auto-created), the 1.x to 2.x upgrade, and virtual read-only mappings derived from bucket names. An explicit mapping overrides a virtual one.

```sh
influx v1 dbrp create --db example-db --rp example-rp --bucket-id BUCKET_ID --default
influx v1 dbrp list
```

Update and delete use `influx v1 dbrp update` and `delete`. API: `/api/v2/dbrps` with POST, GET, PATCH and DELETE.

Each unique DBRP combination can only be mapped to a single bucket.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/query-data/influxql/dbrp/
- Scope: creation sources, flags and API verbs from the DBRP page.
- Removed: the unconfirmed claim that a second mapping replaces the first.
Method: documentation only; no commands were run.
