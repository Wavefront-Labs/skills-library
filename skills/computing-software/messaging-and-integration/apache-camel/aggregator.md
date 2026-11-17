---
id: computing-software.messaging-and-integration.apache-camel.aggregator
name: aggregator
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, aggregate, completion, correlation, repository]
level: advanced
status: docs-checked
description: "Camel Aggregate EIP: correlationExpression, aggregationStrategy, completion options and defaults, repositories, CamelAggregated properties and forced completion."
sources:
  - https://camel.apache.org/components/next/eips/aggregate-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregator

Required: `correlationExpression` (the grouping key) and `aggregationStrategy` (merges new into old; the first call gets a null old exchange). An unevaluable key throws unless `ignoreInvalidCorrelationKeys` (default false).

Completion, per correlation key, first condition wins:
- `completionSize` / `completionSizeExpression`
- `completionTimeout` (inactivity) cannot be combined with `completionInterval` (fixed period for all groups)
- `completionTimeoutCheckerInterval` 1000 ms
- `completionPredicate`; `eagerCheckCompletion` false (true checks the incoming exchange)
- `completionFromBatchConsumer` false; `completionOnNewCorrelationGroup` false
- `forceCompletionOnStop` false; `completeAllOnStop` false

Others: `discardOnCompletionTimeout` false, `optimisticLocking` false (needs `OptimisticLockingAggregationRepository`), `closeCorrelationKeyOnCompletion` (late exchanges throw `ClosedCorrelationKeyException`), `parallelProcessing` false, `aggregateController`.

Repository: `aggregationRepository` defaults to `MemoryAggregationRepository` (lost on restart). Persistent ones exist for Caffeine, CassandraQL, EHCache, Infinispan, JCache, Redis and SQL.

Output properties: `CamelAggregatedSize`, `CamelAggregatedTimeout`, `CamelAggregatedCompletedBy`, `CamelAggregatedCorrelationKey`. Input properties that force completion: `CamelAggregationCompleteCurrentGroup`, `CamelAggregationCompleteAllGroups` (signal only, body not aggregated), `CamelAggregationCompleteAllGroupsInclusive`.

Verify: with `completionSize(3)` and one key, the first group emits after the third message.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/components/next/eips/aggregate-eip.html
