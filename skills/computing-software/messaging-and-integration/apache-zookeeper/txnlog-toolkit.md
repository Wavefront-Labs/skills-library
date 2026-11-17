---
id: computing-software.messaging-and-integration.apache-zookeeper.txnlog-toolkit
name: txnlog-toolkit
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, zktxnlogtoolkit, transaction-log, crc, recovery, corrupted-log]
level: advanced
status: docs-checked
description: "zkTxnLogToolkit.sh: dump transaction log entries or recover entries with broken CRCs, with -d -r -v -y options and the .fixed output file."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zkTxnLogToolkit

Usage per the Tools guide: `bin/zkTxnLogToolkit.sh [-dhrv] txn_log_file_name` (with `-y` also listed).

- `-d, --dump`: dump all entries of the log file to the screen; the default and safe mode, the original is not touched.
- `-r, --recover`: re-calculate CRC for broken entries. The original file stays untouched and all transactions are copied to a new file with a `.fixed` suffix.
- `-v, --verbose`: in recovery mode print all entries, not just fixed ones (recovery is otherwise silent apart from CRC-error entries).
- `-y, --yes`: non-interactive; repair all CRC errors without asking.
- `-h, --help`: print help (also printed when run with no parameters).
- Recovery is interactive by default: at each CRC error it asks `Would you like to fix it (Yes/No/Abort)`. Yes writes the newly calculated CRC, No copies the original CRC, Abort ends the operation and leaves the `.fixed` file half-complete (only the entries already processed, or just the header).
- On success it prints `Recovery file <log>.fixed has been written with N fixed CRC error(s)`.
- The Administrator's Guide lists the tool under "Recovery - TxnLogToolkit" in the data file management section.

Dump output marks bad entries with `CRC ERROR -`.

## Checked

Confirmed against the Tools guide (zkTxnLogToolkit.sh section) and the Administrator's Guide table of contents and Recovery heading. Removed the advice to stop the server and copy the log, which neither page states.

Method: docs-only read of cited pages, 2026-11-08
