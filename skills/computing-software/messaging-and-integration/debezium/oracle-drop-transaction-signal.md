---
id: computing-software.messaging-and-integration.debezium.oracle-drop-transaction-signal
name: oracle-drop-transaction-signal
category: computing-software
field: messaging-and-integration
product: debezium
tags: [oracle, signal, long-running-transaction, logminer]
level: sme
status: docs-checked
description: "Remove a stuck transaction from the Oracle LogMiner buffer with a drop-transaction signal or log.mining.window.max.ms."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A long-running transaction blocks the connector from processing later events, bloats the in-memory buffer and can cause SCN drift, where the connector's SCN falls behind the mining range. If a transaction outlasts the offset flush interval, no offset can be committed. A restart after the last offset leaves the redo logs then fails because no resume point exists.

The `drop-transaction` signal removes a transaction from the LogMiner buffer. Prerequisites: a configured signaling channel, and access to the connector log to find the transaction ID.

Source channel:

```sql
INSERT INTO debezium.debezium_signal VALUES('drop-tx-1', 'drop-transaction', '{"transaction-id": "1a.2b.001f"}');
```

Kafka channel:

```json
{"type": "drop-transaction", "data": {"transaction-id": "1a.2b.001f"}}
```

Key facts:

- The connector abandons the transaction's uncommitted changes and emits no events for them. Send the signal only when you are sure it should not be processed.
- The signal is handled at the start of the next mining iteration on the streaming thread, so on a busy connector the drop happens seconds later. The log reports whether the transaction was found and dropped.

Alternative: set `log.mining.window.max.ms` to advance the mining window automatically when a transaction exceeds a duration. The transaction is still tracked and buffered, unlike with a drop.

Gotcha: dropping loses real data if the transaction later commits.

## Checked

2026-11-08: read the Dropping a transaction section of the Debezium Oracle connector reference (raw AsciiDoc source of the cited page, connectors/oracle.adoc in the debezium/debezium repo) and the log.mining.window.max.ms property row. Confirmed: SCN drift and offset flush explanation, prerequisites, the source and kafka signal examples, the abandon-uncommitted-changes warning, next-mining-iteration timing and the log.mining.window.max.ms alternative. Removed: the unsupported closing Check line.

Method: documentation only; no commands were run.
