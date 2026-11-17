---
id: computing-software.cloud-infrastructure-engineering.garage.lifecycle-worker-use-local-tz
name: lifecycle-worker-use-local-tz
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [use-local-tz, lifecycle-worker, midnight-utc]
level: advanced
status: docs-checked
description: "Control when the daily lifecycle worker runs by switching it from UTC to the local timezone."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`use_local_tz` (since v1.1.0) concerns the lifecycle worker. By default Garage runs it every day at midnight UTC.

Set `use_local_tz = true` to run it at midnight in the local timezone of the node instead. With several nodes, the page says to ensure that each node has the same timezone configuration.

Configuration summary for this parameter:

- key: `use_local_tz`
- type: boolean
- default: `false` (midnight UTC)
- available since: v1.1.0
- applies to: the daily lifecycle worker, on each node
- caveat: use the same value and timezone on every node

The page's full example shows `use_local_tz = false` as a top-level option, placed before the sections such as `[s3_api]`.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the option, the v1.1.0 gate, the UTC midnight default, the local time option, the same-timezone advice and the example placement. Removed two sentences the page does not state (host timezone setup, and a pointer to worker commands).
Method: documentation only; no commands were run.
