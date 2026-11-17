---
id: computing-software.data-engineering.apache-flink.state-processor-api
name: state-processor-api
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, state-processor-api, savepoint, state-bootstrap, state-migration, operator-uid]
level: advanced
status: docs-checked
description: "Read, modify and bootstrap Flink savepoints offline with the State Processor API: inspect keyed state, fix bad values, migrate schemas, and seed new jobs from historical data."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/libs/state_processor_api/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State Processor API

Treat a savepoint (or retained checkpoint) as a dataset: read it with the DataStream API (batch mode), transform it, and write a new savepoint. Requires operators with stable `uid`s.

Dependency: `org.apache.flink:flink-state-processor-api`.

## Read keyed state
```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setRuntimeMode(RuntimeExecutionMode.BATCH);
SavepointReader sp = SavepointReader.read(env, "s3://ckpt/savepoints/savepoint-7f3a", new EmbeddedRocksDBStateBackend());
DataStream<KeyedTotal> totals = sp.readKeyedState(OperatorIdentifier.forUid("customer-totals"), new KeyedStateReaderFunction<String, KeyedTotal>() {
  ValueState<Long> total;
  public void open(OpenContext ctx) { total = getRuntimeContext().getState(new ValueStateDescriptor<>("total", Long.class)); }
  public void readKey(String key, Context ctx, Collector<KeyedTotal> out) throws Exception { out.collect(new KeyedTotal(key, total.value())); }
});
totals.sinkTo(fileSink); env.execute();
```
The state descriptor name and type must match what the job registered. Operator state: `readListState`, `readUnionState`, `readBroadcastState`.

## Bootstrap a new savepoint (seed state from history)
```java
DataStream<Account> history = env.fromSource(jdbcOrFileSource, WatermarkStrategy.noWatermarks(), "hist");
StateBootstrapTransformation<Account> t = OperatorTransformation.bootstrapWith(history)
    .keyBy(Account::id)
    .transform(new KeyedStateBootstrapFunction<String, Account>() {
      ValueState<Long> total;
      public void open(OpenContext c) { total = getRuntimeContext().getState(new ValueStateDescriptor<>("total", Long.class)); }
      public void processElement(Account a, Context ctx) throws Exception { total.update(a.balance()); }
    });
SavepointWriter.newSavepoint(env, new EmbeddedRocksDBStateBackend(), 128)    // max parallelism
    .withOperator(OperatorIdentifier.forUid("customer-totals"), t)
    .write("s3://ckpt/savepoints/bootstrap-2026-10-18");
env.execute();
```
Then start the streaming job with `-s <that path>`.

## Modify an existing savepoint
`SavepointWriter.fromExistingSavepoint(env, path, backend)` then `.withOperator(uid, transformation)` (replace with corrected state), and `.write(newPath)`.

## Uses
- Debug: dump suspicious keys' state to files.
- Fix: rewrite state after a bug wrote bad values, instead of replaying months of input.
- Migrate: change a state type incompatibly (read old, write new descriptor).
- Change operator identifiers with `changeOperatorIdentifier`.

## Rules
- Max parallelism of the new savepoint must equal the job's max parallelism.
- Same state backend type family as the job will use on restore (canonical savepoints are portable across backends; native ones are not).
- Run with the same Flink version as the job.

## Verify
- [ ] Read back the written savepoint and compare key counts/values.
- [ ] Job restores from it without "Cannot map checkpoint/savepoint state" errors.

## Checked

2026-10-28. Confirmed: SavepointWriter.newSavepoint(env, backend, maxParallelism), fromExistingSavepoint, withOperator, OperatorIdentifier.forUid and open(OpenContext) on the State Processor API page. Removed: `removeOperator` (not on the page) and a copy-by-reference claim.

Method: documentation only; no commands were run.
