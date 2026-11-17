---
id: computing-software.data-engineering.data-warehouse-architecture.serving-data-to-external-consumers
name: serving-data-to-external-consumers
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-sharing-external, secure-data-sharing, delta-sharing, data-marketplace, sftp-extracts, clean-rooms]
level: practitioner
status: docs-checked
description: "Share data with partners and customers: native warehouse sharing, Delta Sharing, marketplaces, APIs and file drops, clean rooms, contracts, entitlements and monitoring."
sources:
  - https://docs.snowflake.com/en/user-guide/data-sharing-intro
  - https://delta.io/sharing/
  - https://cloud.google.com/bigquery/docs/analytics-hub-introduction
  - https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serving data to external consumers

## Choose the mechanism
| Mechanism | Best when | Notes |
|---|---|---|
| Snowflake Secure Data Sharing | consumer has a Snowflake account (or you create a reader account for them) | no data is copied; objects are read-only for the consumer; a direct share works only within a region |
| BigQuery sharing (formerly Analytics Hub) | consumer is on Google Cloud | publish a dataset (or Pub/Sub topic) as a listing in a data exchange; subscribers get a linked dataset; shared in place without replication |
| Delta Sharing (open protocol) | consumer on any engine | live data without copying; clients include pandas, Apache Spark and Power BI; access can be governed, tracked and audited |
| Marketplace listings | many consumers, commercial data products | Snowflake listings add metadata, cross-region fulfilment, charging and usage metrics; BigQuery listings can be monetised on Google Cloud Marketplace |
| APIs | app integration, small slices, low latency | needs a serving store, authentication and rate limits (design guidance) |
| File drops (bucket, SFTP) | legacy partners, batch | formats, manifests and checksums (design guidance) |
| Clean rooms | joint analysis without exposing raw data | AWS Clean Rooms: analysis rules, analysis templates agreed in advance, analysis logs, differential privacy; Snowflake offers clean rooms that control which queries can run |

## Snowflake specifics
- A share is a named object; the provider adds databases, schemas, tables, secure views and other objects (directly or through a database role) and then adds consumer accounts. New objects and updates are visible to consumers immediately, and access can be revoked at any time.
- Consumers pay only for compute (warehouses) used to query the data; providers pay for storage. A reader account is owned and paid for by the provider.
- A direct share works only with accounts in the same region; use a listing with cross-cloud auto-fulfilment (or the cross-region sharing guide) otherwise. Use a listing to charge for access, add metadata or see consumer usage metrics.
- Share secure views over a curated sharing schema rather than base tables. Providers of listings can see usage in the Data Sharing Usage schema views.

## Design rules (practice guidance)
- Treat each share as a data product with a contract: schema, semantics, freshness expectation, versioning and deprecation policy, support contact.
- Separate the external-facing schema from internal models so internal refactors do not break partners.
- Version breaking changes and give notice.
- Data minimisation: share only the columns and rows needed; check the legal basis and any data processing agreements and cross-border transfer rules with counsel.

## Entitlements and monitoring
- Keep a governed record of consumer, datasets and row filters, and automate grants from it; expire trial access and revoke at contract end.
- File drops: per-consumer prefixes, short-lived signed URLs, never public buckets.
- Monitor usage (Snowflake listing metrics, Delta Sharing audit capability, bucket access logs) and freshness of shared objects.

## Verify
- [ ] Each consumer sees only the data they are entitled to (test with consumer credentials).
- [ ] Contract (schema, freshness, deprecation) published; usage and freshness monitored.

## Checked
Date: 2026-11-09. Confirmed from the Snowflake sharing page (read in full), the Delta Sharing home page (a short overview), the BigQuery sharing introduction (searched, roles and exchange/listing model) and the AWS Clean Rooms page (first part read). Removed as unconfirmed: the Snowflake SQL example and CURRENT_ACCOUNT mapping, Databricks-to-Databricks sharing, Redshift data sharing, Databricks and BigQuery clean rooms, presigned-URL protocol detail, DATA_SHARING_USAGE view names beyond the schema, and who bears replication and egress costs outside Snowflake. Rows marked design guidance are not page claims.
Method: documentation only; no commands were run.
