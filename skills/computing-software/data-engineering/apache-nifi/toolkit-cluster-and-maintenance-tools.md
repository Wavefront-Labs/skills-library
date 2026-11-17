---
id: computing-software.data-engineering.apache-nifi.toolkit-cluster-and-maintenance-tools
name: toolkit-cluster-and-maintenance-tools
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, toolkit, node-manager, file-manager, notify, flow-analyzer]
level: advanced
status: docs-checked
description: "node-manager, file-manager, notify and flow-analyzer toolkit scripts: operations, required flags and version support."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/toolkit-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster and maintenance scripts

node-manager (NiFi 1.0.0+): `-d` NiFi root and `-b` bootstrap.conf (both required); `-o` `status`, `connect`, `disconnect` or `remove`; `-p` proxy DN (required on secured nodes for connect, disconnect and remove; ignored for status); `-u` comma-delimited active cluster URLs, needed to connect or remove (not for disconnect).

file-manager (1.0.0+): `-o` `install`, `backup` or `restore`; `-b` backup dir, `-c` current dir, `-d` install dir, `-r` rollback dir, `-i` install archive (tar.gz or zip), `-t` bootstrap.conf, `-m` move repositories, `-x` overwrite config. Backup excludes repositories and logs.

notify (1.2.0+): `-d`, `-b`, `-m` message (required); `-l` `INFO`, `WARN` or `ERROR`; `-p` proxy DN on secured nodes. Sends a bulletin message to the node.

flow-analyzer: one positional argument, the path to flow.xml.gz; reports total bytes used and back-pressure and queue min/max/average.

Verify: node-manager `-o status` lists each node and its state.

## Checked

Confirmed against the NiFi Toolkit Guide sections File Manager, Flow Analyzer, Node Manager and Notify: option letters, required options, supported versions (1.0.0+ for node-manager and file-manager, 1.2.0+ for notify) and what flow-analyzer reports. Added the documented proxy DN, cluster URL and backup-exclusion details.

Method: docs-only read of cited pages, 2026-11-08
