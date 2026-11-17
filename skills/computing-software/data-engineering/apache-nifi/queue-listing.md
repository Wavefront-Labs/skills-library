---
id: computing-software.data-engineering.apache-nifi.queue-listing
name: queue-listing
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, queue, list-queue, empty-queue, connections]
level: intro
status: docs-checked
description: "Inspect and clear a NiFi connection queue: List queue shows the top 100 FlowFiles, Empty queue, and the rule that deleting a connection needs it empty with stopped endpoints."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue listing

- List queue (connection context menu) returns the top 100 FlowFiles in the active queue according to the configured priority. It can run while source and destination are running.
- Empty queue clears the queue after the user confirms. It can also run while the endpoints are running.
- Deleting a connection requires the components on both sides to be stopped and the connection to be empty.
- Viewing FlowFile metadata and content in queues needs the "view the data" component policy.

Verify: the listing count matches the queued number shown on the connection.

## Checked

Confirmed against the NiFi user guide (Queue Interaction; connection context menu; component policies).

Method: docs-only read of cited pages, 2026-11-08
