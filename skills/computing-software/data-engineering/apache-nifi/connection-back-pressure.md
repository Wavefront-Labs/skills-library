---
id: computing-software.data-engineering.apache-nifi.connection-back-pressure
name: connection-back-pressure
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, back-pressure, connections, queues, thresholds]
level: practitioner
status: docs-checked
description: "Connection back pressure in NiFi: default thresholds of 10,000 objects and 1 GB, queue colour bands at 60 and 85 percent, and how it relates to swapping."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/nifi-in-depth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Back pressure

Each connection has two thresholds: a back pressure object threshold (number of FlowFiles) and a back pressure data size threshold (a number plus B, KB, MB, GB or TB). Once the queue passes a threshold, the connection's source component is no longer scheduled to run until the queue drains.

Each new connection defaults to 10,000 objects and 1 GB. The defaults can be changed in nifi.properties.

The queue progress bars on the connection label are green for 0-60%, yellow for 61-85% and red for 86-100%. Hovering shows the exact percentage; a completely full queue highlights the connection in red.

Process groups carry Default Back Pressure Object and Data Size Threshold settings. They set the defaults for new connections in that group only (existing connections are unchanged) and are inherited by child groups created afterwards. The root group takes its defaults from nifi.properties.

Setting the threshold to 0 disables back pressure. The user guide recommends this, or a threshold above the largest expected FlowFile count, on connections ending in an Output Port when the group uses the "Batch Output" outbound policy, because a full queue there deadlocks the group.

Swapping is separate: when a queue exceeds `nifi.queue.swap.threshold` (default 20000), NiFi serialises the lowest-priority FlowFiles to swap files on disk (batches of 10,000, per NiFi In Depth).

Verify: filling a queue to threshold stops the upstream processor and the bar turns red.

## Checked

Confirmed against the NiFi user guide (Back Pressure; Default Settings for Connections; Process Group FlowFile Concurrency), the administration guide (Swap Management) and NiFi In Depth (swapping). Removed the claim that thresholds above the swap threshold swap (the pages describe the swap threshold only).

Method: docs-only read of cited pages, 2026-11-08
