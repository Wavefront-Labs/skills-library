---
id: computing-software.database-administration.influxdb.design-a-schema-for-influxdb
name: design-a-schema-for-influxdb
category: computing-software
field: database-administration
product: influxdb
tags: [schema-design, tags, fields, measurements, line-protocol, flux]
level: practitioner
status: docs-checked
description: "Schema rules: encode data in tag and field values (not names), use tags for indexed filters, avoid keywords and duplicate tag/field names."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/schema-design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Rules from the schema design page:

- Store data in tag values and field values. Do not encode it in measurement names or in tag/field keys.
- Tags are indexed and always strings; use them for values you filter or group by. Fields hold unique or numeric values and are not indexed.
- Avoid Flux keywords and special characters in tag and field keys: keywords must be wrapped in double quotes and non-alphanumeric keys need bracket notation in Flux.
- Do not use the same name for a tag key and a field key in the same schema; query results may be unpredictable.
- Use one tag per data attribute rather than packing several attributes into one tag value.
- Filter on a tag in queries to reduce the rows scanned.

Bad: measurement `cpu_host1` with fields `usage_a`. Better: measurement `cpu`, tag `host=host1`, field `usage`.

Related reading: the high-cardinality skill for unbounded tag values, and the duplicate-points skill, since the tag set is part of point identity.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 schema design page, tag/field/keys sections read from the downloaded text.

Confirmed: keep data out of measurement and key names, tags indexed and string-only, fields for unique or numeric data, keyword and duplicate-name rules. The cpu_host1 example is the skill's own illustration of the page's guidance, not a quote.
