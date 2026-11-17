---
id: computing-software.data-engineering.dbt.semantic-layer-apis-and-integrations
name: semantic-layer-apis-and-integrations
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, semantic-layer-api, metricflow, jdbc, graphql]
level: advanced
status: docs-checked
description: "Query dbt Semantic Layer metrics from tools and code: JDBC (Arrow Flight SQL) syntax, GraphQL, the Python SDK, BI integrations, service tokens and environments."
sources:
  - https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview
  - https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc
  - https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic Layer APIs and integrations

**Goal:** serve governed metrics defined in MetricFlow to BI tools, notebooks and apps through one interface.

## Prerequisites
dbt Cloud with the Semantic Layer configured for a production environment (credentials for the warehouse), and a **service token** with Semantic Layer permission. Note the environment id.

## JDBC (Arrow Flight SQL)
```
jdbc:arrow-flight-sql://semantic-layer.cloud.getdbt.com:443?&environmentId=123456&token=<service_token>
```
Queries use templated calls, not plain SQL over tables:
```sql
select * from {{
  semantic_layer.query(metrics=['revenue', 'orders'],
                       group_by=['customer__customer_type'])
}}
```
Further arguments (where, order, limit) and metadata calls are on the JDBC page. Metadata: `select * from {{ semantic_layer.metrics() }}`, `semantic_layer.dimensions(metrics=['revenue'])`.

## GraphQL
The GraphQL page lists hosts per region (North America, EMEA, APAC, single tenant); each request needs the environment id and a token. Pattern: `createQuery` mutation returns a query id; poll `query(queryId)` for status and results (Arrow/JSON).

## Python SDK
The API overview page also lists a Python SDK; take its install and call signatures from there.

## Integrations
The JDBC docs mention connecting tools such as Tableau, DBeaver and DataGrip; see the integrations docs for the supported list.

## Gotchas
- Host differs by region and tenancy; use the one for your account.
- Saved queries + exports materialize results to tables for tools without a connector.

## Verify
`semantic_layer.metrics()` through JDBC returns your metric list; the same query through MetricFlow CLI (`mf query`) gives matching numbers.

## Checked

2026-10-28. Confirmed against: Semantic Layer JDBC page (URL format, environmentId, token, semantic_layer.query/metrics/dimensions), GraphQL page (createQuery, fetch result, per-region hosts, environmentId), API overview (Python SDK, service token requirement). Removed (not confirmable in the fetched pages): where/order_by/limit syntax, dbtsl client code, named BI connector list, caching claim.

Method: documentation only; no commands were run.
