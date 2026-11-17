---
id: computing-software.cloud-infrastructure-engineering.ansible.deprovisioning-mesh-and-controller-nodes
name: deprovisioning-mesh-and-controller-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-mesh, deprovision-node, node-removal, execution-nodes, hop-nodes, awx-manage, instance-groups, receptor]
level: advanced
status: docs-checked
description: "Remove execution, hop or control nodes from an automation mesh: node_state=deprovision in the installer, awx-manage deprovision_instance, and cleanup checks."
sources: ["https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-deprovisioning-mesh-nodes.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/ref-deprovisioning.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-controller-cluster-deprovision-instances.adoc", "https://github.com/ansible/awx/blob/devel/awx/main/management/commands/deprovision_instance.py", "https://github.com/ansible/awx/blob/devel/awx/main/models/ha.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprovisioning mesh and controller nodes

Goal: take a node out of the mesh without leaving a ghost instance that skews capacity.

## 1. Installer-based removal
In the installer inventory append `node_state=deprovision` to the node, then run the installer. Running it removes all configuration files and logs attached to the node.
```ini
[automationcontroller]
host1.example.com
host4.example.com   node_state=deprovision

[execution_nodes]
exec3.example.com   node_state=deprovision
```
To remove a whole instance group, put the variable in the group's vars:
```ini
[instance_group_restrictedzone:vars]
node_state=deprovision
```
Any host in the inventory can be deprovisioned except the first host listed in the `[automationcontroller]` group.

## 2. Removing a controller cluster instance by hand
Re-running the setup playbook does not deprovision instances automatically, because the cluster cannot tell an intentional shutdown from a failure. Instead:
1. Stop services on the instance (`automation-controller-service stop`) or shut it down.
2. From another instance run `awx-manage deprovision_instance --hostname=<name used in inventory file>`. This removes the instance from the database.
3. Restart services on the remaining instances with `automation-controller-service start`.
Deprovisioning an instance does not remove instance groups; groups are removed separately.

## 3. Instance states
The instance `node_state` field takes: provisioning, provision-fail, installed, ready, unavailable, deprovisioning, deprovision-fail. Node types are control, execution, hybrid and hop (a hop node passes messages and has no execution capability). The Instances page lets you remove an instance or run a health check against it.

## 4. Check afterwards
- `awx-manage list_instances` prints each instance group with its capacity and instances.
- Check that nodes that were reached through a removed hop node still have a route; re-peer them first.

## Gotchas
- Instance groups lose the removed node's capacity at once; check that queued jobs do not pile up.

## Verify
- [ ] The Instances page and `awx-manage list_instances` no longer show the node.
- [ ] A job in each affected instance group runs successfully.

## Checked
2026-11-09. Checked against ansible/aap-docs modules (deprovisioning individual nodes using the installer, deprovisioning nodes or groups, deprovisioning controller cluster instances), the AWX `deprovision_instance` and `list_instances` management commands, and the Instance model (`node_state` and `node_type` choices).
Removed as unsupported: API drain steps (`PATCH enabled`, `jobs_running`), operator-managed `node_state=deprovisioning` PATCH procedure, containerized uninstall claim, `systemctl disable --now receptor` step, and statements about ghost-node behaviour when the installer is re-run without the variable.
Method: documentation only; no commands were run.
