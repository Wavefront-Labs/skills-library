---
id: computing-software.data-engineering.metabase.database-routing
name: database-routing
category: computing-software
field: data-engineering
product: metabase
tags: [database-routing, router-database, destination-databases, slug, multi-tenant]
level: sme
status: docs-checked
description: "Route Metabase users to per-tenant databases: router database setup, destination slugs, the user attribute, unsupported databases and features, and testing."
sources:
  - https://www.metabase.com/docs/latest/permissions/database-routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Availability: Pro or Enterprise only, self-hosted or Cloud.

Setup: connect a router database with the same schema as your customer databases, ideally a mock or dev database. Enable routing in its Database routing section, enter the user attribute, then add destination databases, each with a slug.

User attribute: the slug must match the attribute value. Users can get it by manual entry, JWT or SAML. Admins without a value see the router database. A user's value can be set to `__METABASE_ROUTER__`. Non-admins without a valid value cannot view the question.

Limitations:
- Not supported on ClickHouse, Oracle, Spark SQL or Vertica; Athena, BigQuery and Databricks have restrictions.
- Cannot be used with writable connections, editable tables, actions, CSV uploads or model persistence.

Gotchas:
- Guest embedding always uses the router database.
- Public links do not work.
- The router database's name is what all users see.

Testing: use a private or incognito window logged in as a test user.

API: add destinations via `POST /api/ee/database-routing/mirror-database` using an API key; copy the payload from the browser's Network tab.

Failure mode: a mismatch between the attribute value and the slug leaves non-admins unable to view the question.

## Checked
2026-11-03. Confirmed against the Metabase docs page Permissions, Database routing: Pro/Enterprise availability, router and destination database setup with slugs, user attribute rules and __METABASE_ROUTER__, unsupported drivers and per-driver restrictions, unsupported features, guest embedding and public link behaviour, testing steps, mirror-database API path (fixed to the full /api/ee/database-routing path shown on the page).
Method: documentation only; no commands were run.
