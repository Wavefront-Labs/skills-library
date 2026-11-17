---
id: computing-software.data-engineering.druid.druid-overlord-task-distribution
name: druid-overlord-task-distribution
category: computing-software
field: data-engineering
product: druid
tags: [overlord, tasks, middle-manager, blacklist, local-mode, remote-mode]
level: practitioner
status: docs-checked
description: "Explain Overlord local versus remote mode and how failing Middle Managers are blacklisted."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/overlord.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Overlord accepts tasks, coordinates task distribution, creates locks around tasks and returns statuses to callers. It runs in one of two modes, with local as the default.

In local mode the Overlord also creates Peons to execute tasks, so all Middle Manager and Peon configuration must be supplied to it as well. Local mode suits simple workflows. In remote mode the Overlord and Middle Managers run as separate services, possibly on different servers. Remote mode is recommended if you intend to use the indexing service as the single endpoint for all Druid indexing.

Blacklisting: if a Middle Manager has task failures above a threshold, the Overlord blacklists it. No more than 20 percent of Middle Managers can be blacklisted, and blacklisted ones are periodically whitelisted again. The relevant properties are:

```
druid.indexer.runner.maxRetriesBeforeBlacklist
druid.indexer.runner.workerBlackListBackoffTime
druid.indexer.runner.workerBlackListCleanupPeriod
druid.indexer.runner.maxPercentageBlacklistWorkers
```

Autoscaling exists as a framework, but the shipped mechanisms are tightly coupled to the authors' AWS deployment. If autoscaling is enabled, new Middle Managers may be added when a task has been pending too long, and Middle Managers may be terminated if they have run no tasks for a period of time.

## Checked

2026-11-08. Read design/overlord.md in full. Removed an unsourced run command and added the scale-down behaviour of autoscaling.

Method: documentation only; no commands were run.
