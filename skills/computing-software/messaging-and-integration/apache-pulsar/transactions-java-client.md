---
id: computing-software.messaging-and-integration.apache-pulsar.transactions-java-client
name: transactions-java-client
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [transactions, transaction-coordinator, enable-transaction, consume-transform-produce, system-topic]
level: advanced
status: docs-checked
description: "Use Pulsar transactions from the Java client: broker flags, initialize-transaction-coordinator-metadata, enableTransaction, timeouts, commit and abort, individual acks only."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/txn-use.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: atomically consume from one topic and produce to others (and ack the input) with a Pulsar transaction.

Transactions are a server-side and protocol-level feature; the transaction API is available for Java, Go and .NET clients. They are disabled by default.

Step 1, enable on brokers (`broker.conf` or `standalone.conf`):
```conf
transactionCoordinatorEnabled=true
systemTopicEnabled=true
```
Step 2, initialize coordinator metadata (partitioned-topic-like, load balanced):
```shell
bin/pulsar initialize-transaction-coordinator-metadata -cs 127.0.0.1:2181 -c standalone
```
Expected output: `Transaction coordinator metadata setup success`.

Step 3 onward (Java): build the client with `.enableTransaction(true)`. The client role needs produce/consume permissions on the system namespace `pulsar/system`, because it discovers the coordinator through a system topic. Create producers with `.sendTimeout(0, TimeUnit.SECONDS)`.

Run a transaction:
```java
Transaction txn = client.newTransaction().withTransactionTimeout(10, TimeUnit.SECONDS).build().get();
outputProducer.newMessage(txn).value("...").send();
inputConsumer.acknowledgeAsync(message.getMessageId(), txn).get();
txn.commit().get();
```
If the transaction is not committed within the timeout it is aborted automatically. On `ExecutionException`, unless the cause is `PulsarClientException.TransactionConflictException`, call `inputConsumer.negativeAcknowledge(message)` or the message will not be received again; abort the old transaction with `txn.abort()` before creating a new one.

Constraint: within a transaction messages can be acked individually, not cumulatively.

Scalable topics: also need `transactionCoordinatorEnabled=true` (default false) with `scalableTopicsEnabled` and `transactionCoordinatorScalableTopicsEnabled` (both default true); `transactionCoordinatorScalableTopicsParallelism` defaults to 16 and must be identical on all brokers; use a `pulsar://` or `pulsar+ssl://` URL because discovery requires the binary protocol.

Verify: after commit, consume the output topics and see the messages; after abort, see none.

## Checked

2026-11-03. Confirmed against the Pulsar transactions usage page: Java, Go and .NET client support, `transactionCoordinatorEnabled` default false, `initialize-transaction-coordinator-metadata` command and success message, `pulsar/system` permissions, `sendTimeout(0)`, the `TransactionConflictException` / `negativeAcknowledge` handling, individual (not cumulative) acks, and the scalable-topics settings and parallelism default of 16 that must match on all brokers.

Method: documentation only; no commands were run.
