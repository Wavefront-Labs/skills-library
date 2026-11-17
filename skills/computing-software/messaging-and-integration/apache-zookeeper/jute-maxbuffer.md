---
id: computing-software.messaging-and-integration.apache-zookeeper.jute-maxbuffer
name: jute-maxbuffer
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, jute-maxbuffer, znode-size, data-limits, unsafe-options]
level: advanced
status: docs-checked
description: "jute.maxbuffer caps znode data and request size: 1048575 byte default, extrasize property, and why servers and clients must agree."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jute.maxbuffer

- Java property `jute.maxbuffer`, default 0xfffff (1048575 bytes): maximum znode data size.
- It is listed among the options the admin guide says to use carefully. Set the same value on every server and every client; a mismatch causes problems.
- `jute.maxbuffer.extrasize` (`zookeeper.jute.maxbuffer.extrasize`, 3.5.7+): defaults to the jute.maxbuffer size and gives extra room for transaction records.
- Design guidance: znodes hold kilobytes, with a sanity limit under 1 MB.
- For benchmarks with large znodes pass `-Djute.maxbuffer` via the tool's jvm-args.

Verify: `jute.maxbuffer` is identical in server and client JVM flags and a write near the limit succeeds.

## Checked

Read the Administrator's Guide, Programmer's Guide and Tools pages. Confirmed the 0xfffff (1048575 byte) default, the matching server and client requirement, jute.maxbuffer.extrasize (3.5.7), the kilobytes-sized design guidance, and the YCSB -jvm-args example. Removed the advice to store pointers, which the pages do not give.

Method: docs-only read of cited pages, 2026-11-08
