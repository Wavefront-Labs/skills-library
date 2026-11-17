---
id: computing-software.messaging-and-integration.apache-zookeeper.znode-path-and-size-rules
name: znode-path-and-size-rules
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, znode-paths, path-rules, data-size, reserved-names]
level: intro
status: docs-checked
description: "Valid ZooKeeper znode paths and data sizes: absolute canonical paths, forbidden characters and segments, reserved zookeeper token and the under-1M guidance."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path and size rules

- Paths are canonical, absolute, slash-separated; there are no relative references.
- Not allowed: the null character (\u0000); \u0001-\u001F and \u007F-\u009F; \ud800-uF8FF and ￰-uFFFF.
- "." may be part of a name, but "." and ".." cannot stand alone as a path segment (`/a/b/./c` and `/a/b/../c` are invalid).
- The token "zookeeper" is reserved.
- Data is coordination data (configuration, status, rendezvous), measured in kilobytes. Client and server sanity checks ensure a znode holds less than 1M, and data should be much smaller on average. Large values slow some operations and raise latency.
- For large data, store it in bulk storage such as NFS or HDFS and keep pointers to it in ZooKeeper.
- Each write replaces all of a znode's data; reads return all of it.

## Checked
Confirmed against the Programmers Guide data model section, 2026-11-08. Removed: the jute.maxbuffer default, the in-memory claim, the /zookeeper subtree description and the rejection check, which that page does not state.
Method: docs-only read of cited pages, 2026-11-08
