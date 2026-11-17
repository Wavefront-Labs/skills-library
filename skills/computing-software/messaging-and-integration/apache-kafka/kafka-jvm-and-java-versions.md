---
id: computing-software.messaging-and-integration.apache-kafka.kafka-jvm-and-java-versions
name: kafka-jvm-and-java-versions
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, java-version, g1gc, jvm-heap, java-17]
level: intro
status: docs-checked
description: "Run Kafka 4.2 on a supported Java and start from the documented G1GC heap settings."
sources:
  - https://kafka.apache.org/42/operations/java-version/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick a Java version and baseline JVM flags.

Support: Java 17, Java 21 and Java 25 are fully supported. Java 11 is supported for a subset of modules (clients, streams and related). Versions newer than the latest LTS are best-effort. The docs recommend the most recent LTS (Java 25 at the time of writing) and the latest patch release, because older patch versions typically have disclosed security vulnerabilities.
Typical arguments for OpenJDK-based Java (including Oracle JDK):
```
-Xmx6g -Xms6g -XX:MetaspaceSize=96m -XX:+UseG1GC
-XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:G1HeapRegionSize=16M
-XX:MinMetaspaceFreeRatio=50 -XX:MaxMetaspaceFreeRatio=80 -XX:+ExplicitGCInvokesConcurrent
```

Reference point from the docs: one of LinkedIn's busiest clusters at peak ran 60 brokers, 50k partitions (replication factor 2), 800k messages/sec in, 300 MB/sec inbound and over 1 GB/sec outbound with those arguments. All its brokers had a 90% GC pause time of about 21ms with fewer than 1 young GC per second.

Summary: prefer a current LTS Java at its latest patch release, and treat the argument list above as the documented starting point rather than a tuned result for your own workload.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 java-version page. Removed the claim that the broker quickstart requires Java 17+ (not on this page) and the "Java 17 floor" advice. Other claims unchanged. No hands-on run.
