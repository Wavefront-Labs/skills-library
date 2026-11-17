---
id: computing-software.data-engineering.apache-nifi.relationships-and-retry
name: relationships-and-retry
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, relationships, auto-terminate, retry, back-off]
level: practitioner
status: docs-checked
description: "Relationships tab rules: every relationship must be connected or auto-terminated, and automatic retry with Penalize or Yield back-off before termination."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relationships and retry

- The user guide states that all defined relationships of a component must be connected to another component or auto-terminated.
- The Relationships tab lists each relationship with its description under "Automatically Terminate / Retry Relationships".
- Retry settings per relationship: Number of Retry Attempts (how many times a FlowFile is reprocessed before it is routed elsewhere), Retry Back Off Policy, and Retry Maximum Back Off Period.
- Back off policy Penalize: retries occur over time while the processor keeps processing other FlowFiles. Yield: no other FlowFile processing occurs until all retry attempts have been made.
- Initial retries use the Penalty/Yield Duration from the Settings tab; the duration doubles on each later attempt, and the maximum back off period caps it.
- If both terminate and retry are selected, the retry logic runs first, then auto-termination.

Example in the user guide: on the Settings tab, tick Auto-terminate relationships for Success to terminate FlowFiles after the processor handles them.

Verify: the processor shows no invalid icon, and failures are not silently terminated when you meant to route them.

## Checked

Confirmed against the NiFi user guide (Settings tab, Relationships, Automatically Retry). Removed the rule that a connected relationship cannot also be auto-terminated and the "dropped" wording, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
