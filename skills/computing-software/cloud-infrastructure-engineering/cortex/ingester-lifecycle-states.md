---
id: computing-software.cloud-infrastructure-engineering.cortex.ingester-lifecycle-states
name: ingester-lifecycle-states
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ingester, ring-states, lifecycler, tokens-file, readiness]
level: practitioner
status: docs-checked
description: "Read the ingester ring states PENDING, JOINING, ACTIVE, LEAVING and UNHEALTHY and what each means for reads and writes."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each ingester has a lifecycler that records its state in the hash ring.

- PENDING: just started; receives neither writes nor reads.
- JOINING: starting up and joining the ring; no reads or writes. It uses tokens loaded from disk if `-ingester.tokens-file-path` is configured, otherwise generates random ones, and may observe the ring for token conflicts before becoming active once any conflict is resolved.
- ACTIVE: running; receives reads and writes.
- LEAVING: shutting down; no writes, but still serves reads.
- UNHEALTHY: failed to heartbeat to the ring KV store; distributors skip it when building the replication set, and it receives neither writes nor reads.

Ingesters are semi-stateful, so the state matters during rollouts.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page (raw markdown, read in full). Claims about the tokens file reducing churn and about where the ring page is served were dropped as not on this page.
