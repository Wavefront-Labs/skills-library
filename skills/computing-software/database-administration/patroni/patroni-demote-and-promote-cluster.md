---
id: computing-software.database-administration.patroni.patroni-demote-and-promote-cluster
name: patroni-demote-and-promote-cluster
category: computing-software
field: database-administration
product: patroni
tags: [patroni, patronictl, standby-cluster, demote-cluster, promote-cluster]
level: practitioner
status: docs-checked
description: "Switch a cluster between regular and standby mode with patronictl demote-cluster and promote-cluster."
sources:
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: flip an existing cluster to or from a standby cluster safely.

`patronictl demote-cluster [CLUSTER_NAME] [--host HOST] [--port PORT] [--restore-command CMD] [--primary-slot-name SLOT] [--force]` patches the dynamic configuration with a `standby_cluster` section built from the options, then waits until the leader runs as a standby leader. It prints the topology first and asks for confirmation unless `--force` is given. At least one of `--host`, `--port` or `--restore-command` is required.

```
patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

`patronictl promote-cluster [CLUSTER_NAME] [--force]` converts a standby cluster back to a regular cluster. It removes the `standby_cluster` section from the dynamic configuration and waits until the leader runs as primary, with the same topology print and confirmation.

```
patronictl -c postgres0.yml promote-cluster batman --force
```

If CLUSTER_NAME is omitted, patronictl reads it from the `scope` configuration. Both commands were introduced in Patroni 4.1.0, which also made the demotion to a standby cluster clean when a `standby_cluster` section is introduced in dynamic configuration.

## Checked

2026-11-03. Confirmed against the patronictl page: demote-cluster and promote-cluster synopses, options, behaviour and examples; 4.1.0 introduction against the release notes.

Method: documentation only; no commands were run.
