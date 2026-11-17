---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-drain-and-cordon-nodes
name: mayastor-drain-and-cordon-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, drain, cordon, uncordon, maintenance, kubectl-plugin, volume-target]
level: practitioner
status: docs-checked
description: "Use the Mayastor plugin to cordon a node (stop new resources) or drain it (also move volume targets off), and halt a drain or uncordon afterwards."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/cordon-node
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/drain-node
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both operations mirror the Kubernetes concepts of the same names but act on Mayastor's view of a node.

**Cordon.** Cordoning labels the node as unschedulable so the scheduler will not deploy **new** resources on it; anything deployed before the cordon stays intact. The plugin can add the cordon label, list cordoned nodes, and show the labels on a cordoned node. To make the node schedulable again, **uncordon** it, which lets the Kubernetes scheduler deploy resources there once more.

**Drain.** Draining marks the node unschedulable and then gracefully **moves all volume targets off** the drained node, in line with Kubernetes' safe node drain. You can list the nodes on which a drain has been performed. To halt the drain or make the node schedulable again, the page uses the same `uncordon node` command as for cordon.

Commands as the pages give them (`<label>` is a label you supply):

- `kubectl-mayastor cordon node <node_name> <label>`
- `kubectl-mayastor get cordon nodes`
- `kubectl-mayastor get cordon node <node_name>` (labels on a cordoned node)
- `kubectl-mayastor uncordon node <node_name> <label>`
- `kubectl-mayastor drain node <node_name> <label>`
- `kubectl-mayastor get drain nodes`

The Drain page links to the Kubernetes safe node drain documentation as the model for the feature.

## Checked

Method: 2026-11-08, read both source pages (openebs/website docs markdown for cordon-node and drain-node) in full. Replaced the invented maintenance sequence, the `kubectl openebs mayastor` alias claim and the pool-cordon cross-reference (none stated by these pages) with the exact commands listed. Halting a drain is done with `uncordon node`, not a separate halt command.
