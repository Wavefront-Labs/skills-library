---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-container-copy-and-migration
name: cosmos-container-copy-and-migration
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-container-copy-and-migration, cosmos-backup, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Move data between containers and accounts."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/container-copy
  - https://learn.microsoft.com/en-us/cli/azure/cosmosdb/copy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/troubleshoot-request-rate-too-large
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container copy and data migration

**Goal:** Move data between containers and accounts.

## Steps
- Container copy jobs (preview): az cosmosdb copy create, from the cosmosdb-preview extension, copies a container within an account or to another account.
- Data import tools such as Azure Data Factory and the bulk executor library can load large datasets; they retry 429s automatically.
- Online copy mode replicates incremental changes from the source (using all versions and deletes change feed) until you complete the job.
- To change partition key, copy into a new container with the new key.

## Gotcha
Online copy needs the EnableOnlineContainerCopy account capability, and replace and delete operations on the source incur extra RU charges.

## Checked

2026-11-03. Confirmed against the container copy page and the az cosmosdb copy reference (preview extension; --src-account and --dest-account may differ): copy within or between accounts, partition key change via a new container, online copy via all versions and deletes change feed, EnableOnlineContainerCopy capability, extra source RU on replace and delete; data import tools named on the 429 page.
Removed: the Spark connector claim and the "throttle production" wording (unsupported). Replaced the unrelated backup source.
Method: documentation only; no commands were run.

## Verify
- [ ] Item counts and checksums match between source and target before cutover.
