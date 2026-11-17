---
id: computing-software.data-engineering.apache-flink.managed-flink-services
name: managed-flink-services
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, managed-flink, amazon-managed-service-for-apache-flink, confluent-cloud-flink, cloud]
level: practitioner
status: docs-checked
description: "Choose and run a managed Flink service (Amazon Managed Service for Apache Flink, Confluent Cloud Flink): what they manage, limits, and migration notes."
sources:
  - https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html
  - https://docs.confluent.io/cloud/current/flink/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed Flink services

## Options
| Service | Interface | Documented traits |
|---|---|---|
| Amazon Managed Service for Apache Flink | Java, Scala, Python (and embedded SQL) with the DataStream or Table APIs from your IDE; or a Studio notebook (SQL, Python, Scala) | Provisions compute, AZ failover resilience, parallel computation, automatic scaling, application backups (checkpoints and snapshots) |
| Confluent Cloud for Apache Flink | Flink SQL, Table API (Java and Python), user-defined functions | Serverless on Confluent Cloud: provisioning, autoscaling, fault tolerance handled; available on AWS, Azure and Google Cloud |

Other vendors (Ververica, Alibaba, self-managed on Kubernetes) are outside the two pages checked here.

## Amazon: pick the flavour
- Long-running streaming ETL or continuous applications: use the service with your own IDE; this supports Git, CI/CD and unit testing.
- Ad-hoc exploration, interactive queries or private dashboards: Studio notebook. A notebook can be promoted to a long-running application, but AWS recommends the IDE route if you need SDLC tooling.
- Flink offers four API levels: SQL, Table API, DataStream API, and Process Function (with DataStream). Start at the highest abstraction that works. Choose DataStream when you need fine-grained state control, asynchronous calls to an external database or endpoint, custom timers, or the ability to change the application flow without resetting state.
- Evolving logic without a state reset depends on setting operator UIDs, which is available only in the DataStream API (Java and Python).
- Language: not every connector is supported in Python with DataStream; for low latency or high throughput consider Java/Scala; Async IO in Process Functions requires Java; SQL can be embedded in any language.

## Confluent: how it works
- Kafka topics appear automatically as Flink tables, and Flink tables appear as topics. Mapping: environment = catalog, cluster = database, topic plus schema = table. Creating a table creates the topic and schema, so DDL acts on physical objects, not only metadata.
- No runtime version to choose: you always run the latest Flink, and running statements get security patches and minor upgrades. You do not manage clusters, state backends or checkpointing.
- Autoscaling follows each statement's input topic rates; billing is usage-based and compute deallocates when unused (scale to zero).
- Compute pools are regional and shared by statements; a default pool is used unless you create pools for workload isolation or cost control. Flink reads and writes any Kafka cluster in the same region and cannot query across regions. RBAC still governs access.

## Trade-offs to weigh
- With a serverless SQL service you give up control of Flink runtime version, cluster and state configuration (Confluent), so confirm required connectors, APIs and languages are supported before committing.
- Check the cost model (usage-based vs provisioned) against your steady-state workload.

## Migration notes
Keep jobs portable: set stable operator UIDs where the API allows, use standard connectors, and pass configuration via arguments rather than service-specific APIs. Plan cutover by source offsets; the pages do not describe cross-provider savepoint portability.

## Verify
- [ ] Required connectors, language and API are supported by the chosen service.
- [ ] Cost model checked against expected steady-state load.

## Checked
Method: docs-only read on 2026-11-09 of the AWS what-is page in full and the first 150 lines of the Confluent Cloud Flink overview (partial read; billing and later sections not read). Removed unread or unstated claims: the Ververica row and its source (docs.ververica.com not read), Alibaba, Google Cloud and Azure HDInsight rows, KPU sizing, snapshot and allow-listed config details, API parameter names, runtime properties call, watermark and TTL specifics, and the statement that savepoints are generally not portable.
