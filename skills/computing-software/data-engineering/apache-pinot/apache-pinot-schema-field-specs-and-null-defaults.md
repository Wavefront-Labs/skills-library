---
id: computing-software.data-engineering.apache-pinot.apache-pinot-schema-field-specs-and-null-defaults
name: apache-pinot-schema-field-specs-and-null-defaults
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, schema, dimensionfieldspecs, metricfieldspecs, datetimefieldspecs, enablecolumnbasednullhandling, defaultnullvalue, timefieldspec]
level: practitioner
status: docs-checked
description: "Pinot schema shape: dimension, metric and dateTime field specs, enableColumnBasedNullHandling, defaultNullValue, TimeFieldSpec rejection."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/data-modeling/schema.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema field specs and null defaults

A schema defines the columns of a table, each column's data type, whether it is a dimension, metric or date-time field, and how missing values and time semantics are handled. Schema and table config are stored separately but should be designed together.

Example from the Pinot docs:
```
{
  "schemaName": "orders",
  "enableColumnBasedNullHandling": true,
  "dimensionFieldSpecs": [
    { "name": "orderId", "dataType": "STRING" },
    { "name": "region", "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "amount", "dataType": "DOUBLE", "defaultNullValue": 0 }
  ],
  "dateTimeFieldSpecs": [
    { "name": "eventTime", "dataType": "LONG", "format": "EPOCH", "granularity": "1:DAYS" }
  ]
}
```

Guidance from the page:
- Decide early whether the table needs column-based or table-based null semantics (`enableColumnBasedNullHandling`).
- `defaultNullValue` is set per field spec, as in the metric above.
- Keep one primary time field in mind for retention and hybrid-table boundary behaviour.
- Use stable, business-facing column names and simple types that match the source; add only fields you need at query time, because schema changes are additive and should be deliberate.
- Model time columns with `dateTimeFieldSpecs` only. The REST schema submission paths reject the deprecated `TimeFieldSpec` (`fieldType=TIME`); schemas already stored in the cluster still load for backward compatibility.

For the exact JSON fields, validation rules and date-time formats see the Pinot schema reference; for indexing, retention and routing see the table reference.

## Checked

2026-11-08. Read the whole pinot-docs schema and table shape page. Confirmed the three field spec arrays, enableColumnBasedNullHandling, per-field defaultNullValue, and the TimeFieldSpec rejection. Removed what the page does not state: the meaning of defaultNullValue at ingestion, the `1:MILLISECONDS:EPOCH` format string, primaryKeyColumns for upsert, the schema upload curl and the metric-versus-dimension gotcha.

Method: documentation only; no commands were run.
