---
id: computing-software.data-engineering.apache-pinot.apache-pinot-server-process-and-startup-flags
name: apache-pinot-server-process-and-startup-flags
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, server, startserver, serverhost, serverport, serveradminport, datadir, segmentdir, offline-server, realtime-server]
level: intro
status: docs-checked
description: "Pinot server basics: offline and realtime share one process type, plus StartServer flags for ports, directories and config file."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/server.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinot server process and startup flags

Servers provide the primary storage for segments and perform the computation to execute queries. Servers are typically segregated into real-time servers (hosting only real-time tables) and offline servers (hosting only offline tables), but this is an operational convention, not a difference or explicit configuration in the server process itself.

- Offline servers download segments from the segment store and serve queries from them. When a segment is uploaded to the controller, the controller picks as many servers as the replication and notifies them to download it.
- Real-time servers ingest directly from a stream (such as Kafka or EventHubs). Periodically, based on thresholds, they make segments from the in-memory data and persist them to the segment store.
- Servers are Helix participants; a server hosts one or more segments (Helix partitions) of one or more tables (Helix resources).

Start one:
```
bin/pinot-admin.sh StartServer -zkAddress localhost:2181
```
Docker: run the Pinot image with the `StartServer -zkAddress <zookeeper-host>:2181` arguments.

`StartServer` options (all `required=false`):
- `-serverHost <String>`: host name (the help text says "controller", an error in the docs).
- `-serverPort <int>`: port number to start the server at.
- `-serverAdminPort <int>`: port to serve the server admin API at.
- `-dataDir <string>`: path to the directory containing data.
- `-segmentDir <string>`: path to the directory containing segments.
- `-zkAddress`: address of ZooKeeper.
- `-clusterName <String>`: Pinot cluster name.
- `-configFileName`: config file for the server starter.
- `-help`: print usage.

The page gives no default port numbers; check the server configuration reference for them.

## Checked

2026-11-08. Read the whole pinot-docs server page. Confirmed the offline versus real-time convention, Helix modelling and the StartServer option list. Removed the example with specific IP, ports and directory paths (the page gives none), the capacity-planning paragraph, and the claim that -serverHost and -serverPort are the address brokers use.

Method: documentation only; no commands were run.
