---
id: computing-software.software-engineering.software-architecture.database-per-service
name: database-per-service
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, microservices, database-per-service, shared-database, data-ownership, distributed-data]
level: advanced
status: docs-checked
description: "Decide between database-per-service and a shared database, enforce ownership boundaries, and handle the queries, joins and reporting the split makes harder."
sources: ["https://microservices.io/patterns/data/database-per-service.html", "https://microservices.io/patterns/data/shared-database.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database per service vs shared database

## Database per service
Keep each service's persistent data private and accessible only via its API; a service's transactions involve only its own database. The database is effectively part of the service's implementation.
- Benefits: services stay loosely coupled (a change to one service's database does not affect others), and each service can use the type of database best suited to it (for example a search engine for text search, a graph database for a social graph).
- Ways to keep data private with a relational database (private tables, schema, or server):
  - private tables per service: each service owns a set of tables only it may access
  - schema per service: a schema private to the service
  - database server per service: its own server
  Private tables and schema per service have the lowest overhead; a schema per service makes ownership clearer; some high-throughput services might need their own server.
- Enforce the barrier: for example give each service a different database user id and use access control grants. Without a barrier, developers will be tempted to bypass the service's API and read its data directly.
- Drawbacks: business transactions spanning services are not straightforward (distributed transactions are best avoided; many NoSQL databases do not support them), queries joining data from several databases are challenging, and several SQL and NoSQL databases must be managed.

## Shared database
One database shared by several services; each service freely accesses the others' tables using local ACID transactions.
- Benefits: familiar ACID transactions enforce consistency, and one database is simpler to operate.
- Drawbacks: development-time coupling (schema changes must be coordinated with the developers of other services that use the same tables), runtime coupling (a long-running transaction in one service can hold a lock that blocks another), and one database may not satisfy every service's storage and access needs.

## Handling the hard parts after splitting
| Need | Pattern |
|---|---|
| Transaction spanning services | Saga pattern |
| Query joining data from several services | API composition (the application, or a service or API gateway, performs the join) |
| Query joining data from several services, at the view level | CQRS: materialised views kept up to date by subscribing to events each service publishes |

## Checked
2026-11-08. Confirmed against the microservices.io Database per service and Shared database pages: private tables, schema and server options and their overhead, enforcement by separate user ids and grants, benefits and drawbacks of each approach, saga, API composition and CQRS as the answers. Removed (not stated on those pages): when a shared database is acceptable, the one-writer-per-table rule with views, the outbox and CDC row, replicating reference data, the reporting and warehouse row, and the migration steps attributed to Newman. The O'Reilly book page returned 403 and was not used.
Method: documentation only; no commands were run.
