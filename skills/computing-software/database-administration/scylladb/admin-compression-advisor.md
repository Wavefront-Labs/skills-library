---
id: computing-software.database-administration.scylladb.admin-compression-advisor
name: admin-compression-advisor
category: computing-software
field: database-administration
product: scylladb
tags: [compression, compression-advisor, zstd, lz4, alter-table]
level: practitioner
status: docs-checked
description: "ScyllaDB Compression Advisor: estimate LZ4 and ZSTD compression ratios via the estimate_compression_ratios REST API, prerequisites, 5 percent threshold, generated ALTER TABLE."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/compression-advisor.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compression Advisor

`tools/compression_advisor.py` analyses the compression of one table and recommends a different compressor, compression level or chunk length when it would meaningfully shrink the on-disk size. It reads the current settings over CQL, asks the node to estimate ratios for many candidate configurations through the `estimate_compression_ratios` REST API, and prints a colour heatmap, a summary comparing the current configuration to the best LZ4 and ZSTD candidates, and one ready-to-run `ALTER TABLE` for the best overall option.

Decision rules: it recommends a change only if the estimated ratio improves by at least 5%, and it prefers the default 4 KB chunk length unless a larger chunk is more than 5% better. This avoids churn for negligible gains.

Prerequisites:
- Python 3 and the ScyllaDB Python driver (`pip install scylla-driver`); without it the tool still prints the heatmap and recommendations but cannot compare to the current configuration.
- Network access to CQL (port 9042) and the Admin REST API (port 10000).
- The `SSTABLE_COMPRESSION_DICTS` cluster feature enabled on all nodes. Otherwise the REST API is unavailable and the advisor reports that the API returned invalid JSON.

```
python3 tools/compression_advisor.py --host <node-ip> --keyspace myks --table mytbl
python3 tools/compression_advisor.py --host <node-ip> --keyspace myks --table mytbl --no-color
python3 tools/compression_advisor.py --host <node-ip> --keyspace myks --table mytbl --username <user> --password <pw>
```
Use `--no-color` when redirecting to a file, and pass credentials when `PasswordAuthenticator` is on. The advisor only estimates and recommends; it never modifies the table.

## Checked

2026-11-04: purpose, 5 percent rule, prerequisites, ports, options and output confirmed against the ScyllaDB Compression Advisor documentation page. Removed the unsupported note on how existing SSTables get rewritten.

Method: documentation only; no commands were run.
