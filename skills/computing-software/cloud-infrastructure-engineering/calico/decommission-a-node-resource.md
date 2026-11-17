---
id: computing-software.cloud-infrastructure-engineering.calico.decommission-a-node-resource
name: decommission-a-node-resource
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [node, decommission, calicoctl, rename, cleanup, ipam, node-controller, workload-endpoint]
level: practitioner
status: docs-checked
description: "Remove a Calico Node resource after a host is gone, with calicoctl delete node, the multi-node file form, and what else is deleted."
sources:
  - https://docs.tigera.io/calico/latest/operations/decommissioning-a-node
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If you run the node controller (in kube-controllers) or use the Kubernetes datastore in policy-only mode, you do not need to decommission nodes by hand. Otherwise do it when:

- you are removing a host running calico-node from the cluster, or renaming a node;
- you see an error that an IP address is already in use;
- readiness checks fail because peers no longer in the cluster are unreachable;
- hosts are added and removed regularly.

**Prerequisites.** Stop the calico-node container on that host and make sure it will not restart before touching the Node resource. calicoctl must be configured.

**Consequences.** Deleting a Node resource also removes its Workload Endpoint, Host Endpoint and IP address resources and any other sub-configuration, including node-specific BGP peerings and custom Felix configs. It may disrupt service if the host is still in use.

**One node:**

```bash
calicoctl delete node <nodeName>
```

**Several nodes.** Put them in a file and pass it with `-f`:

```yaml
- apiVersion: projectcalico.org/v3
  kind: Node
  metadata:
    name: node-02
- apiVersion: projectcalico.org/v3
  kind: Node
  metadata:
    name: node-03
```

then `calicoctl delete -f <file>`.

The page cautions that deleting a Node resource may be service impacting, so make sure the host is out of service first.

## Checked

Read in full on 2026-11-08: the Decommission a node page. The reasons, prerequisites, side effects, the single delete command, the multi-node YAML and the `-f` delete form match it. An unsourced remark about checking node names was removed.

Method: documentation only; no commands were run.
