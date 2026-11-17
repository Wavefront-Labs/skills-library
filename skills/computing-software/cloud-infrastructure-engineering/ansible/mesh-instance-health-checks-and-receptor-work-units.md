---
id: computing-software.cloud-infrastructure-engineering.ansible.mesh-instance-health-checks-and-receptor-work-units
name: mesh-instance-health-checks-and-receptor-work-units
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-mesh, instance-health-check, receptor-work-units, receptorctl]
level: advanced
status: docs-checked
description: "Run instance health checks from the controller, read node_state and errors, and inspect receptor work units with receptorctl work list, results and release."
sources: ["https://github.com/ansible/awx/blob/devel/docs/clustering.md", "https://github.com/ansible/awx/blob/devel/awx/api/views/__init__.py", "https://github.com/ansible/awx/blob/devel/awx/main/models/ha.py", "https://github.com/ansible/receptor/tree/devel/docs/source/receptorctl", "https://github.com/ansible/receptor/blob/devel/docs/source/user_guide/workceptor.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Instance health checks and receptor work units

## Health checks
```bash
curl -s -X POST -H "Authorization: Bearer $T" https://aap.example.com/api/v2/instances/12/health_check/
curl -s -H "Authorization: Bearer $T" https://aap.example.com/api/v2/instances/12/health_check/
```
- POST to `/api/v2/instances/<id>/health_check/` starts a health check; GET returns the last result. Health checks work only on execution nodes (hop nodes are not found by this endpoint). If one is already pending, the API answers that it is already in progress.
- Permission: system administrators or system auditors.
- The check runs `ansible-runner --worker-info` against the node; the CPU, memory and runner version it returns are used to calculate the instance capacity. The UI "Run health check" action on the Instances page does the same.
- Each control node also runs a periodic `cluster_node_heartbeat`; a node whose `last_seen` is older than `CLUSTER_NODE_HEARTBEAT_PERIOD * CLUSTER_NODE_MISSED_HEARTBEAT_TOLERANCE` is marked lost.
- The instance fields `errors`, `last_health_check`, `capacity` and `node_state` show the outcome. `node_state` values: provisioning, provision-fail, installed, ready, unavailable, deprovisioning, deprovision-fail. A failed check sets the node to unavailable with capacity 0 and the reason in `errors`.
- `awx-manage list_instances` prints each instance group with its capacity, plus per-instance capacity, node type, version and heartbeat; instances with zero capacity (other than hop nodes) are shown in red.

## receptorctl
Use the node's control socket (`--socket`, or the `RECEPTORCTL_SOCKET` environment variable; default is a Unix socket, `tcp://` for TCP):
```bash
receptorctl --socket <socket_path> status                 # network status; --json available
receptorctl --socket <socket_path> ping <remote_node>
receptorctl --socket <socket_path> traceroute <remote_node>
receptorctl --socket <socket_path> work list
receptorctl --socket <socket_path> work results <unit-id>
receptorctl --socket <socket_path> work release <unit-id>
```
- `status` also shows the work types available on nodes.
- `work results` returns results for completed, failed, stopped or still-running units.
- `work release` deletes units; `--all` deletes all units known to the connected node, `--force` deletes locally even if the remote node is unreachable.
- Work unit data is stored on disk under `{datadir}/{nodeID}/{unitID}/`; the default datadir is `/tmp/receptor` and is set with `datadir` in the `node` section.

## Debugging a stuck job
1. Find the work unit ID for the job, then `receptorctl work list` on the node that holds it for its state.
2. `work results <id>` streams the unit's output.
3. Release finished or stuck units with `work release`.

## Verify
- [ ] Every execution node shows `ready`, non-zero capacity and a recent `last_health_check`.

## Checked
2026-11-09. Checked against AWX `docs/clustering.md` (node health section), the AWX API source (`InstanceHealthCheck` view and URL route), the Instance model (`node_type`, `node_state` choices, error handling), `list_instances` management command, and the receptor docs for receptorctl status, ping, traceroute, work list, results, release, and work unit storage.
Removed as unsupported: `awx instances list` CLI call and the jq output filter, the claim that hop-node checks verify reachability, specific error strings, "periodic every N" values, the `/run/receptor/receptor.sock` path, containerized socket remark, `podman ps`/`journalctl` steps, and the large-output slowdown claim.
Method: documentation only; no commands were run.
