---
id: computing-software.data-engineering.apache-hadoop.yarn-node-labels
name: yarn-node-labels
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, node-labels, partitions, capacity-scheduler, gpu]
level: advanced
status: docs-checked
description: "YARN node labels: exclusive vs non-exclusive partitions, enabling and storing labels, rmadmin label commands, per-queue label capacities, and label expressions."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/NodeLabel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node labels

Only node partitions are supported. Each node has at most one partition, so the cluster splits into disjoint sub-clusters; unlabelled nodes are in the DEFAULT partition (partition=""). Exclusive: containers go only to nodes with exactly the requested partition (DEFAULT requests go to DEFAULT nodes). Non-exclusive: the partition shares idle resource with containers requesting DEFAULT. An application can use only the subset of labels its queue can access. A request with no label is allocated only on DEFAULT nodes.

Enable (yarn-site.xml on the RM):
- `yarn.node-labels.enabled` = true
- `yarn.node-labels.fs-store.root-dir` = e.g. `hdfs://namenode:port/path/to/store/node-labels/`; it must exist and the RM (typically user yarn) must be able to access it; a local `file://` path on the RM also works
- `yarn.node-labels.configuration-type`: `centralized` (default), `delegated-centralized` or `distributed`

Labels:

```
yarn rmadmin -addToClusterNodeLabels "label_1(exclusive=true),label_2(exclusive=false)"
yarn cluster --list-node-labels
yarn rmadmin -removeFromClusterNodeLabels "label_1,label_2"
```

`exclusive` defaults to true. A label associated with queues cannot be removed. Labels and node mappings survive RM restart, and both can be updated while the RM runs.

Centralized node mapping:

```
yarn rmadmin -replaceLabelsOnNode "node1[:port]=label1 node2=label2" [-failOnUnknownNodes]
yarn rmadmin -replaceLabelsOnNode "node1"     # no label removes the mapping
```

Without a port the label applies to all NodeManagers on the node. In every mode the partition must be one of the valid labels configured in the RM.

Distributed mode (`distributed` on the RM; NM-side keys): `yarn.nodemanager.node-labels.provider` = `config`, `script` or a class extending NodeLabelsProvider; `...provider.configured-node-partition` for `config`; `...provider.script.path` and `...script.opts` for `script`, where the last script output line starting with `NODE_PARTITION:` is used; `...provider.fetch-interval-ms` (default 10 min, -1 means only at initialization); `...provider.fetch-timeout-ms` (script, default 20 min); `...resync-interval-ms` (default 2 min). Delegated-centralized: `yarn.resourcemanager.node-labels.provider` (class extending RMNodeLabelsMappingProvider) and `...provider.fetch-interval-ms` (default 30 min, -1 means once after registration).

Capacity Scheduler keys, per `<queue-path>`:
- `accessible-node-labels`: comma-separated labels; inherited from parent if unset; a single space means no labels
- `accessible-node-labels.<label>.capacity`: default 0; the sum across direct children of a parent must equal 100
- `accessible-node-labels.<label>.maximum-capacity`: default 100
- `default-node-label-expression`: empty by default, so containers come from unlabelled nodes

Capacity (without the label prefix) covers DEFAULT-partition nodes and the children must also sum to 100. Apply with `yarn rmadmin -refreshQueues` and check the scheduler page of the RM web UI.

Page example: 5 nodes of 24G/24 vcores, h5 labelled GPU; engineering, marketing and sales get 33/34/33 of DEFAULT; engineering and marketing each get GPU capacity 50, giving each (12G, 12 vcores) on h5; engineering defaults to GPU.

Applications: `ApplicationSubmissionContext.setNodeLabelExpression(..)` for all containers, `ResourceRequest.setNodeLabelExpression(..)` per request (overrides the former), and the AM container request in ApplicationSubmissionContext. `yarn.resourcemanager.node-labels.am.default-node-label-expression` overrides the default expression only for the AM container (disabled by default).

Monitoring: RM web UI `/cluster/nodes`, `/cluster/nodelabels`, `/cluster/scheduler`; CLI `yarn cluster --list-node-labels` and `yarn node -status <NodeId>`.

## Checked

Method: 2026-11-08 compared against the Node Labels page (apache/hadoop trunk markdown, read in full). Keys, defaults, commands and example match the page; sections on distributed and delegated modes and AM default expression added, and invented content removed.
