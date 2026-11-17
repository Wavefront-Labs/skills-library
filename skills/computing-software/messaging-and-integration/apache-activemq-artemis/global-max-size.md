---
id: computing-software.messaging-and-integration.apache-activemq-artemis.global-max-size
name: global-max-size
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,global-max-size,global-max-messages,global-max-size-percent-of-jvm-max-memory,paging,activemq-artemis]
level: advanced
status: docs-checked
description: "Cap memory across all addresses with global-max-size (default 50 percent of -Xmx) and global-max-messages, enforcing each address's address-full-policy."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/paging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global paging limits

**Goal:** bound the total memory used by messages across the whole broker, not just per address.

- `global-max-size`: total bytes that can be sent to all addresses. Unless set explicitly in `broker.xml` it is a percentage of the JVM max memory (`-Xmx`): by default 50%. Change the percentage with `global-max-size-percent-of-jvm-max-memory`. Use `-1` to disable.
- `global-max-messages`: total messages across all addresses; default `-1` (disabled).

When the total exceeds the global limit, the `address-full-policy` of the corresponding address is enforced. This holds even when an address has both `max-size-bytes` and `max-size-messages` set to `-1`. Memory used by the management address is not counted and cannot cause other addresses to trigger a policy.


## Pairing with policies
- `PAGE` (default) moves messages to disk.
- `DROP` silently discards. `FAIL` discards and throws on the producer.
- `BLOCK` blocks producers until memory frees up; producers unblock automatically. In the default configuration addresses block producers after 10 MiB of data.

## Checked
2026-11-03. Confirmed against the Artemis user manual page paging (Global Settings, address-full-policy sections, management-address note) and flow-control (10 MiB default block). Removed: the Verify step.
Method: documentation only; no commands were run.
