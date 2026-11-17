---
id: computing-software.data-engineering.apache-flink.async-io-enrichment
name: async-io-enrichment
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, datastream-api, async-io, asyncfunction, stream-enrichment, external-lookup, lookup-join, retries, backpressure]
level: practitioner
status: docs-checked
description: "Enrich Flink streams from external services with Async I/O: AsyncFunction, ordered vs unordered wait, capacity and timeouts, retry strategies, caching and SQL async lookup joins."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/asyncio/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/joins/#lookup-join
  - https://github.com/apache/flink-connector-jdbc/blob/main/docs/content/docs/connectors/table/jdbc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async I/O for stream enrichment

**Goal:** look up external data (REST service, database, cache) per event without the operator blocking on each request and throttling the whole job.

## 1. Why async
A synchronous lookup in a `map` handles one request at a time per subtask, so latency caps its throughput. Async I/O keeps up to `capacity` requests in flight per subtask.

## 2. Implement AsyncFunction
```java
public class EnrichCustomer extends RichAsyncFunction<Order, EnrichedOrder> {
  private transient CustomerClient client;     // must be non-blocking (returns CompletableFuture)

  @Override public void open(OpenContext ctx) { client = CustomerClient.create(); }
  @Override public void close() { client.close(); }

  @Override public void asyncInvoke(Order o, ResultFuture<EnrichedOrder> rf) {
    client.getCustomer(o.customerId).whenComplete((c, err) -> {
      if (err != null) rf.completeExceptionally(err);              // fails the job (or retry, below)
      else rf.complete(Collections.singleton(new EnrichedOrder(o, c)));
    });
  }
  @Override public void timeout(Order o, ResultFuture<EnrichedOrder> rf) {
    rf.complete(Collections.singleton(new EnrichedOrder(o, null)));  // degrade instead of failing
  }
}
DataStream<EnrichedOrder> out = AsyncDataStream.unorderedWait(
    orders, new EnrichCustomer(), 2, TimeUnit.SECONDS, 200);       // timeout, capacity
```
- Blocking client only? Run calls on your own bounded `ExecutorService` inside `asyncInvoke` — never block the callback thread.
- `complete` must be called exactly once per input (result, empty collection to drop, or exception).

## 3. Ordered vs unordered
| | `orderedWait` | `unorderedWait` |
|---|---|---|
| Output order | same as input | completion order |
| Latency | head-of-line blocking | lower |
With event time, `unorderedWait` still keeps records between watermarks together — watermarks are not overtaken — so event-time correctness holds. Use ordered only when downstream logic depends on per-key arrival order.

## 4. Capacity, timeouts, retries
- `capacity` = max in-flight requests per subtask; when full, the operator backpressures upstream. Size it to the service's concurrency limit divided by parallelism.
- Retries:
```java
AsyncRetryStrategy<EnrichedOrder> retry = new AsyncRetryStrategies.ExponentialBackoffDelayRetryStrategyBuilder<EnrichedOrder>(
        3, 100L, 2000L, 2.0)
    .ifException(RetryPredicates.HAS_EXCEPTION_PREDICATE).build();
AsyncDataStream.unorderedWaitWithRetry(orders, new EnrichCustomer(), 5, TimeUnit.SECONDS, 200, retry);
```
The timeout covers all attempts.
- Fault tolerance: in-flight requests are stored in checkpoints and re-issued after recovery — lookups must be idempotent reads.

## 5. Reduce calls
- Cache hot keys inside the function with a TTL cache; the cache is per subtask, so `keyBy` before the async operator improves the hit rate.
- For slowly changing reference data, prefer broadcast state or a CDC stream joined in Flink over per-event lookups.

## 6. Flink SQL equivalent
```sql
SELECT o.*, c.segment
FROM orders AS o
JOIN customers FOR SYSTEM_TIME AS OF o.proc_time AS c ON o.customer_id = c.id;
```
The JDBC connector's lookup source runs in sync mode and supports a partial cache (`'lookup.cache' = 'PARTIAL'` with `'lookup.partial-cache.max-rows'` and `'lookup.partial-cache.expire-after-write'`). Check each connector's page for whether it offers an async lookup.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Async I/O page, `AsyncRetryStrategies` source and the JDBC connector docs: `open(OpenContext)`, `timeout()` override, capacity semantics, ordered vs unordered watermark behaviour, in-flight requests re-triggered after recovery, the retry builder signatures, lookup join syntax, JDBC lookup cache options. Removed the unconfirmed version gate, throughput arithmetic, caching-library names and `lookup.async`.

Method: documentation only; no commands were run.

## Verify
- [ ] Throughput scales with capacity until the external service limit, not with parallelism alone.
- [ ] Timeout path tested (service down) and produces the intended degraded output.
- [ ] External service QPS stays within its quota under peak load.
