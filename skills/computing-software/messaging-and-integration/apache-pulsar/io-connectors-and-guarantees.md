---
id: computing-software.messaging-and-integration.apache-pulsar.io-connectors-and-guarantees
name: io-connectors-and-guarantees
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [pulsar-io, source-connector, sink-connector, processing-guarantees, connector-admin]
level: practitioner
status: docs-checked
description: "Pulsar IO source and sink connectors: what they do, shared processing guarantees with Functions, setting them on create or update, and the sink idempotency caveat."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/io-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move data between Pulsar and external systems with the right delivery semantics.

Types: source connectors feed data from external systems into Pulsar (other messaging systems, firehose-style pipelines); sink connectors feed data from Pulsar into external systems (other messaging systems, SQL and NoSQL databases). Connectors and Functions are components that run as instances on Functions workers, so managing a connector starts an instance on a worker.

Processing guarantees are the same as for Functions:
- `at-most-once`: processed once or not at all.
- `at-least-once`: processed once or more.
- `effectively-once`: one output per message.
Set with `--processing-guarantees` using the values `ATLEAST_ONCE`, `ATMOST_ONCE`, `EFFECTIVELY_ONCE`. If the flag is omitted when creating a connector, the default is `ATLEAST_ONCE`.
```bash
bin/pulsar-admin sources create --processing-guarantees ATMOST_ONCE   # plus other source configs
bin/pulsar-admin sinks create --processing-guarantees EFFECTIVELY_ONCE # plus other sink configs
bin/pulsar-admin sources update --processing-guarantees EFFECTIVELY_ONCE
bin/pulsar-admin sinks update --processing-guarantees ATMOST_ONCE
```

Gotcha: guarantees depend on the external system too. For a source, Pulsar controls the write to Pulsar topics so the guarantee holds. For a sink, the guarantee depends on the sink implementation: if its retry handling is not idempotent, the sink does not respect the processing guarantee, even when EFFECTIVELY_ONCE is set.

Lifecycle: use the connector admin CLI (`sources` and `sinks` subcommands) to create, update, start, stop, restart, reload and delete connectors; REST and Java admin APIs offer the same operations. The overview points to the source and sink connector pages for the list of built-in connectors.

## Checked

2026-11-03. Confirmed against the pulsar-site page io-overview: source and sink roles, the guarantee table, `--processing-guarantees` values and ATLEAST_ONCE default, create and update commands, the sink idempotency caveat and the Functions-worker note. Removed the unsourced download statement and the invented Verify step.

Method: documentation only; no commands were run.
