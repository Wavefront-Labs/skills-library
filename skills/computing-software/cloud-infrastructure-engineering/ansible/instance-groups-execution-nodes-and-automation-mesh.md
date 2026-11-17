---
id: computing-software.cloud-infrastructure-engineering.ansible.instance-groups-execution-nodes-and-automation-mesh
name: instance-groups-execution-nodes-and-automation-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, instance-groups, automation-mesh, execution-nodes, hop-nodes, control-nodes, hybrid-nodes, receptor, receptorctl, container-groups, capacity, forks-capacity, policy-instance-percentage, node-types, peers, mesh-topology, remote-execution, dmz-automation, install-bundle]
level: advanced
status: docs-checked
description: "Scale and segment AWX/controller execution: node types (control, execution, hop, hybrid), Receptor mesh, instance group policies, preferred groups and enable/disable."
sources: ["https://github.com/ansible/awx/blob/devel/docs/clustering.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance groups, execution nodes and automation mesh

**Goal:** jobs for a DMZ, a remote site or a cloud region run on nodes that can reach
those targets, with capacity you can reason about.

## 1. Node types (AWX clustering docs)
| Type | Meaning |
|---|---|
| **control** | control plane node that cannot run jobs (it still has the machinery, but job running is disabled through the API) |
| **hybrid** (AAP only) | control plane node that can also run jobs |
| **execution** | not a control node; can only run jobs |
| **hop** (AAP only) | not a control node; routes traffic from control nodes to execution nodes |
- Control and hybrid nodes are identical except for the `type` in the database. Smaller control nodes plus a separate execution fleet is the intended use of the `control` type.
- Scale AAP VM deployments by editing the installer inventory and re-running setup; on Kubernetes change the replica count. A new control node registers itself in the database as an instance.

## 2. How nodes talk
- Receptor is an overlay network connecting control, execution and hop nodes. It is used for heartbeats and for submitting jobs to execution nodes. Nodes connect by persistent TCP; once on the mesh a node is reachable from all others even without a direct connection, because intermediate nodes route traffic.
- Control nodes also hold websocket connections to each other (the websocket backplane, `wsbroadcast`) so a browser connected to one node can see job events emitted by another.
- Only control nodes need direct database access; execution and hop nodes do not.

## 3. Instance groups
- Control and execution nodes are instances; instances are grouped into instance groups through the API. Create groups by POST to `/api/v2/instance_groups` as a system administrator; add an instance with POST `{"id": N}` to `/api/v2/instance_groups/<id>/instances/`. An instance added to a group listens on the group's work queue.
- Policies, evaluated for each new instance that comes online: `policy_instance_percentage` (0-100, share of active instances), `policy_instance_minimum` (at least this many; if fewer exist, all are used) and `policy_instance_list` (fixed names). Percentage and minimum work together (50% and minimum 2 with 6 instances gives 3; with 2 instances both join). Making percentages sum to 100 spreads instances without overlap.
- Instances added directly through the API are put into `policy_instance_list` and then need manual management. To pin an instance exclusively to chosen groups, add it to their `policy_instance_list` and PATCH the instance with `managed_by_policy` false.
- Where a job runs: by default in the default queue (setting `DEFAULT_EXECUTION_QUEUE_NAME`); project updates and other administrative work run in the control plane queue (`DEFAULT_CONTROL_PLANE_QUEUE_NAME`). If the job template, inventory or organization have instance groups, the job is not eligible for the default behaviour and stays `pending` until one of those groups has capacity. Preference order: job template, then inventory, then organization. Associating the global `tower` group as a fallback keeps "any instance" as the last resort.
- An instance in several groups has its capacity reduced in all of them while it works. If every instance of a group is offline, jobs targeting only that group wait: plan fallback capacity.
- Instances can be disabled (`enabled` false): no new jobs are assigned and running jobs finish. Use this to drain a node for maintenance.
- A job running on an instance that fails is marked permanently failed.

## 4. Health and monitoring
- `cluster_node_heartbeat` runs on control nodes. For execution nodes it reads Receptor advertisements (`receptorctl status`) and runs a health check (`ansible-runner --worker-info`), which reports CPU cores, memory and the ansible-runner version used to compute capacity. Nodes missing heartbeats past `CLUSTER_NODE_HEARTBEAT_PERIOD` times `CLUSTER_NODE_MISSED_HEARTBEAT_TOLERANCE` are marked lost, their jobs reaped (failed) and the instance removed.
- A node with an older ansible-runner version than its peers stops its own services, so upgrade all nodes together.
- `/api/v2/ping` reports the serving instance, last heartbeats and instance group membership; `/api/v2/instances/` and `/api/v2/instance_groups` give detail.
- Project syncs run on the instance that prepares the job's private data directory, immediately before the job is sent, and may be skipped when the revision is already checked out.

## Gotchas
- A job stuck in `pending` usually means the groups on the template, inventory or organization have no free capacity or no reachable instance.
- For topology, installer inventory variables, install bundles, container groups, capacity tuning and mesh certificates, use the documentation for your release (AWX, or Red Hat's automation mesh guide for AAP); the Red Hat pages could not be read as text in this review and are not summarised here.

## Verify
- [ ] `receptorctl status` on a control node lists every execution and hop node with routes.
- [ ] Each execution node's health check shows nonzero capacity; a job template pinned to the group runs on one of its instances.
- [ ] Disabling a node stops new jobs landing on it and re-enabling restores capacity.

## Checked
2026-10-28. Confirmed in the AWX clustering overview: node types and their meanings, Receptor and websocket roles, database access, instance group API calls and policy fields with the worked example, `managed_by_policy`, queue settings, group preference order, pending behaviour, enable/disable, heartbeat and health-check flow, `/api/v2/ping`. Removed because not confirmed: the capacity formula and tuning settings, the port 27199 default, the installer inventory syntax, install bundle steps, container group fields, `max_concurrent_jobs`/`max_forks`, `receptorctl ping`/`work list`, the module example and `node_state=deprovision`, advice on keeping jobs off the control plane group, and the EX467 reference.
Method: documentation only; no commands were run.
