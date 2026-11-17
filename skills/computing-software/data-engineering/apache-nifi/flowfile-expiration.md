---
id: computing-software.data-engineering.apache-nifi.flowfile-expiration
name: flowfile-expiration
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, flowfile-expiration, connections, data-loss, queues]
level: intro
status: docs-checked
description: "FlowFile Expiration on connections: default 0 sec means never, measured from entry into NiFi, clock icon indicator, group defaults for new connections, data-loss warning."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FlowFile expiration

- Set on the connection's Settings tab; default `0 sec` means data never expires.
- Expiration is measured from when the data entered the NiFi instance, not from when it joined this queue.
- A clock icon on the connection marks a non-zero value.
- Process groups hold default expiration (root default 0 sec) that applies only to connections created afterwards.
- The guide warns that non-zero expiration can cause data loss; expired FlowFiles produce EXPIRE provenance events.

Verify: the connection shows the clock icon and expired items appear as EXPIRE events in provenance.

## Checked

Checked against the NiFi User Guide, connection FlowFile Expiration, Default Settings for Connections and provenance event type sections: the 0 sec default, the entry-time basis, the clock icon, group defaults applying only to new connections, the root default and the data-loss warning match.

Method: docs-only read of cited pages, 2026-11-08
