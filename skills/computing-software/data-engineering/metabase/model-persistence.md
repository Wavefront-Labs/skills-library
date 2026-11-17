---
id: computing-software.data-engineering.metabase.model-persistence
name: model-persistence
category: computing-software
field: data-engineering
product: metabase
tags: [model-persistence, persisted-models, cron-schedule, warehouse-schema, refresh]
level: advanced
status: docs-checked
description: "Enable Metabase model persistence: supported databases, instance, database and model switches, refresh scheduling, security feature conflicts and the move to transforms."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/models/model-persistence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs say to prefer Transforms instead of model persistence, which will be deprecated in future versions.

Storage: results are stored as tables in a dedicated schema in your data warehouse, not the application database. Supported databases: PostgreSQL, MySQL and Redshift only.

Limitations: does not work with row and column security or impersonation.

Setup:
- Instance-wide: Admin, Performance, Model persistence, with preset intervals or a custom cron schedule. Cron uses the report timezone if set, otherwise the system timezone (GMT on Cloud).
- Per database: Admin, Databases, your database, turn model persistence on. Metabase creates the schema if credentials allow; otherwise create it manually with the exact name shown in the info icon.
- Per model: Edit settings, Persist model data. This needs Pro or Enterprise and Curate access to the collection.

Defaults: new models are not persisted until enabled.

Refresh: runs on the schedule, or manually from the model's Edit settings sidebar. After you edit a model's query, questions re-run that query until the next refresh. Check Monitor, Model persistence log.

## Checked
2026-11-03. Confirmed against the Metabase docs page Data modeling, Model persistence: Transforms recommendation, warehouse storage, supported databases, row and column security / impersonation conflict, instance, database and model switches, cron timezone rule, manual schema creation, refresh and log locations. Removed the claim that persistence needs `CREATE` on the database (the page only says permissive credentials let Metabase create the schema, otherwise create it yourself).
Method: documentation only; no commands were run.
