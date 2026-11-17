---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-topology-parameters-node-and-pool
name: mayastor-topology-parameters-node-and-pool
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, topology, nodeaffinitytopologylabel, nodehastopologykey, nodespreadtopologykey, poolaffinitytopologylabel, poolhastopologykey, placement]
level: advanced
status: docs-checked
description: "Place Mayastor replicas by topology: the five StorageClass parameters for node and pool labels, how each one matches, and the one-topology-parameter-per-class rule."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/configuration/rs-topology-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Topology parameters in the StorageClass decide which nodes or pools may hold a volume's replicas. **Only one type of topology parameter is supported per StorageClass.**

Node-based parameters match labels on **nodes**:

- **`nodeAffinityTopologyLabel`**: replicas go only on nodes whose labels exactly match what the class lists. In the docs' example, `zone=us-west-1` places replicas on `worker-node-1` and `worker-node-3`, the nodes carrying that label.
- **`nodeHasTopologyKey`**: replicas may go on any nodes that have a label with the given **key**, whatever the value. With key `rack` on three labelled nodes and two replicas, any two of the three qualify.
- **`nodeSpreadTopologyKey`**: replicas go on nodes that share the label key but have **different values**. With key `zone`, the pairs allowed are those in different zones, such as node-1 with node-2, or node-2 with node-3, in the docs' example.

Pool-based parameters match labels on **DiskPools**:

- **`poolAffinityTopologyLabel`**: replicas only on pools matching the exact labels, for example `zone=us-west-1` giving `pool-on-node-0` and `pool-on-node-2`.
- **`poolHasTopologyKey`**: pools that have the label key.

Apply node labels with `kubectl mayastor label node` and pool labels in the DiskPool `spec.topology.labelled` field. List pools filtered by label with `kubectl mayastor get pools -n openebs --selector zone=eu-west-1`.

## Checked

2026-11-04. Confirmed against the Topology Parameters page: the one-type-per-StorageClass rule, all five parameters with the page's worked examples, node labelling, DiskPool topology labels and the `--selector` listing. Removed the `label pool` command and the existing-volumes remark, which this page does not give.

Method: documentation only; no commands were run.
