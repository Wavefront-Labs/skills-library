---
id: computing-software.messaging-and-integration.temporal.dynamic-configuration
name: dynamic-configuration
category: computing-software
field: messaging-and-integration
product: temporal
tags: [dynamic-configuration, dynamicconfigclient, constraints, rps-limits, persistence-qps, size-limits, partitions, self-hosted]
level: practitioner
status: docs-checked
description: "Temporal self-hosted dynamic configuration: YAML format, constraints by namespace and task queue, pollInterval, key defaults for RPS, QPS and size limits."
sources:
  - https://docs.temporal.io/references/dynamic-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic configuration changes a running self-hosted Temporal Service without restart. The server re-reads the YAML file at the `pollInterval` set in the `dynamicConfigClient` section of static config. Keys and defaults are defined in `constants.go` in the Temporal Server repository and can be renamed between releases, so check release notes before upgrading.

Format: each key maps to a list of values, optionally with `constraints` (`namespace`, `taskQueueName`, and `taskType` of `Workflow` or `Activity`). No constraints means global; `constraints: {}` applies to everything else. The most specific matching constraint wins, regardless of order in the file.

Example, raising partitions (default 4; set read and write to the same value):

    matching.numTaskqueueReadPartitions:
      - constraints: { namespace: 'ns1', taskQueueName: 'tq' }
        value: 8
      - constraints: {}
        value: 16

Defaults (v1.32.0):
- `frontend.rps` 2400, `frontend.namespaceRPS` 2400, `history.rps` 3000, `matching.rps` 1200. Over-limit requests fail with `ResourceExhausted`.
- `frontend.globalNamespaceRPS` 0; when set it overrides `frontend.namespaceRPS`, divided evenly among Frontend hosts.
- Persistence QPS: frontend 2000, history 9000, matching 3000, worker 500; visibility read and write 9000 each.
- `limit.blobSize.warn` 512 KB, `.error` 2 MB; `limit.historySize` warn 10 MB, error 50 MB; `limit.historyCount` warn 10,240, error 51,200.
- `limit.numPendingActivities.error`, child workflows, signals and cancels: 2000 each; `history.maximumSignalsPerExecution` 10000; `limit.maxIDLength` 1000.
- Dual visibility: `system.secondaryVisibilityWritingMode` of off, on or dual; `system.enableReadFromSecondaryVisibility` false.

Raising limits needs matching compute and database capacity.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: references/dynamic-configuration (under https://docs.temporal.io/). Reworded the path to constants.go (page gives no directory).

Method: documentation only; no commands were run.
