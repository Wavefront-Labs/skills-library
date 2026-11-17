---
id: computing-software.messaging-and-integration.apache-pulsar.standalone-quickstart
name: standalone-quickstart
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [standalone, quickstart, local-development, pulsar-daemon, advertised-address, rocksdb]
level: intro
status: docs-checked
description: "Run Pulsar standalone for local development: Java requirements, download and layout, bin/pulsar standalone, advertised address, data reuse and the public/default namespace."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/getting-started-standalone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start a one-process Pulsar for development and testing.

Standalone runs all cluster components in a single JVM. It is for local use only; production installs follow the bare-metal deployment guide. A Pulsar cluster is not meant for the public internet; deploy in private networks.

Prerequisites: 64-bit macOS or Linux (use Docker on Windows). Pulsar servers including standalone require Java 21 or later; Java 25 is recommended and is in the Docker image. The Java client libraries have a separate minimum of Java 17, which does not mean the broker can run on 17.

Steps:
```bash
curl -LO "https://www.apache.org/dyn/closer.lua/pulsar/pulsar-<version>/apache-pulsar-<version>-bin.tar.gz?action=download"
tar xvfz apache-pulsar-<version>-bin.tar.gz
cd apache-pulsar-<version>
bin/pulsar standalone
```
Distribution directories: `bin` (the pulsar entry script and tools), `conf` (including broker.conf), `lib`, `examples` and `instances` (Functions). Starting creates `data` (BookKeeper and RocksDB data) and `logs`.

Access: standalone advertises `localhost` unless configured; set `--advertised-address` to an address reachable from another machine. Run in background with `bin/pulsar-daemon start standalone`.

Metadata: standalone uses RocksDB for metadata by default with embedded BookKeeper; embedded ZooKeeper is available with `PULSAR_STANDALONE_USE_ZOOKEEPER=1`. Before reusing data with a different release, stop the old instance and back up data, metadata and configuration together, and keep the old binaries for rollback. New instances with RocksDB or an explicit metadata-store URL use index-based bookie identities (`bk-0`, `bk-1`), independent of hostname, port and path.

The `public/default` namespace is created at startup for development; all topics live inside namespaces.

## Checked

2026-11-03. Confirmed against the pulsar-site page getting-started-standalone: Java requirements, download and layout, start command, advertised address, data reuse, daemon command and the `public/default` namespace. Removed the invented Verify step.

Method: documentation only; no commands were run.
