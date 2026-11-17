---
id: computing-software.database-administration.influxdb.create-bucket-and-naming-rules
name: create-bucket-and-naming-rules
category: computing-software
field: database-administration
product: influxdb
tags: [bucket, influx-bucket-create, retention, naming]
level: practitioner
status: docs-checked
description: "Create an InfluxDB 2.x OSS bucket with influx bucket create or the API, with its retention flag units, 1 hour minimum, naming limits and the roughly 20 active bucket guideline."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/buckets/create-bucket/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Create a bucket with the `influx` CLI:

```sh
influx bucket create \
  --name my-bucket \
  --org my-org \
  --retention 72h
```

Flags: `-n/--name`, `-o/--org` or `--org-id`, `-r/--retention`. Retention units are `ns`, `us` (or `µs`), `ms`, `s`, `m`, `h`, `d`, `w`. The minimum retention period is one hour.

Bucket naming restrictions: at least two characters, cannot start with an underscore (`_`, reserved for system buckets), cannot contain a double quote.

Over the API, `POST` to the buckets endpoint with `Authorization: Token ...` and `Content-type: application/json`. The body takes `name`, `orgID`, `description` and `retentionRules`, a JSON array holding one object: `type: expire`, `everySecond` (seconds to retain, 0 means forever) and `shardGroupDuration` (seconds to retain shard groups; the page says 0 means forever).

Sizing guideline: a single OSS instance supports approximately 20 buckets actively written to or queried across all organizations.

In the UI, create from Data (Load Data) > Buckets or from the Data Explorer `+ Create Bucket`; choose Delete Data Never or Older than.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/admin/buckets/create-bucket/
- Scope: bucket creation flags, naming rules, API body fields and the 20 bucket guideline.
- Removed: the unconfirmed performance and per-tenant advice.
Method: documentation only; no commands were run.
