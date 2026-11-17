---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.serverless-database
name: serverless-database
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, serverless-database, aurora-serverless, dynamodb-on-demand, neon, scale-to-zero]
level: practitioner
status: draft
description: "Evaluate serverless databases: scaling and scale-to-zero behaviour, cold resume latency, connection limits, pricing crossover vs provisioned and good-fit workloads."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html", "https://learn.microsoft.com/azure/azure-sql/database/serverless-tier-overview", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html", "https://neon.com/docs/introduction/scale-to-zero"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serverless databases

## Steps
1. **Understand the scaling unit**: Aurora Serverless v2 scales in ACUs (0.5 ACU steps;
   minimum 0 with auto-pause supported in newer versions); Azure SQL serverless scales vCores
   with auto-pause after a delay; DynamoDB on-demand charges per request; Neon/Cosmos DB
   serverless and Firestore bill per use.
2. **Cold resume**: auto-pause saves money but first query after pause waits (seconds to tens
   of seconds); fine for dev/test and internal tools, not for latency-sensitive production.
3. **Connections**: serverless compute (Lambda) plus relational DB needs a pooler (RDS Proxy,
   PgBouncer, Data API); check max connections at minimum capacity.
4. **Pricing crossover**: serverless per-unit price is higher; steady high utilisation is
   cheaper provisioned (plus reservations). Model your load curve over a month.
5. **Good fits**: spiky or unpredictable traffic, many small tenant databases, dev/test,
   new products with unknown load.
6. **Set guardrails**: maximum capacity caps to bound cost and protect downstream systems.

## Gotchas
- Scaling up is fast but buffer pools reset on some resumes, causing slow first queries.
- DynamoDB on-demand has throughput ramp behaviour for sudden extreme spikes; pre-warm for launches.

## Verify
- [ ] Cost modelled at expected and peak load vs provisioned.
- [ ] Resume latency acceptable for the workload.
