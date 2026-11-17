---
id: computing-software.ai-ml-engineering.ray.autoscaler-config
name: autoscaler-config
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-autoscaler, idle-timeout, upscaling-speed, resource-demand]
level: practitioner
status: docs-checked
description: "Understand the Ray autoscaler: demand-based scaling, node types, idle timeout, upscaling_speed, and min/max worker settings."
sources:
  - https://docs.ray.io/en/latest/cluster/key-concepts.html
  - https://docs.ray.io/en/latest/cluster/vms/user-guides/configuring-autoscaling.html
  - https://docs.ray.io/en/latest/cluster/vms/references/ray-cluster-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscaler

The autoscaler is a process on the head node that adds worker nodes when tasks, actors or placement groups are queued for lack of resources, and removes worker nodes that stay idle. It reacts only to logical resource requests (those in `@ray.remote`, shown by `ray status`), not to physical utilisation or application metrics.

```yaml
max_workers: 20
idle_timeout_minutes: 2
upscaling_speed: 2.0
available_node_types:
  cpu_worker:
    min_workers: 1
    max_workers: 20
    resources: {CPU: 16}
    node_config: {}   # provider-specific, for example InstanceType on AWS
```

## Settings (cluster launcher YAML)
- `max_workers`: default 2; counts workers only, not the head. Lowering it at runtime makes the autoscaler remove nodes immediately, which can disrupt running work.
- `min_workers`: default 0; kept regardless of utilisation. Per node type, the sum of `min_workers` must not exceed the cluster `max_workers`, and a type's `max_workers` must not exceed the cluster one.
- `upscaling_speed`: default 1.0, minimum 1.0. Number of nodes allowed pending as a multiple of current nodes (1.0 with 20 nodes allows 20 pending launches). The minimum number of pending launches is 5 whatever the setting.
- `idle_timeout_minutes`: default 5, minimum 0. A worker is idle when it has no active tasks, actors or referenced objects (in memory or spilled). It does not apply to the head node.
- `available_node_types.<name>.resources`: what a node type provides, so the autoscaler picks the right type for a demand. If omitted, it can be auto-detected only on AWS and Kubernetes.

## Gotchas
- Idle also means no referenced objects, so nodes holding data are not removed.
- Autoscaling adds node launch overhead and can be tricky to configure; the docs recommend starting with a non-autoscaling cluster if you are new to Ray.
- Deleting a node type from `available_node_types` and running `ray up` scales down all nodes of that type; changing its `node_config` replaces its existing nodes.

## Verify
Submit more work than capacity; `ray status` shows the queued demand, then the node count grows, and idle workers disappear after the timeout.

## Checked
Checked 2026-11-09 against the Ray docs pages key-concepts, configuring-autoscaling and the cluster YAML configuration reference (read in full or by section). Removed unconfirmed claims: `request_resources` usage, the monitor.log path, "infeasible" log wording, KubeRay `enableInTreeAutoscaling` and the v2 autoscaler remark, plus the boot-time and placement-group idle statements.

Method: docs-checked 2026-11-09 against docs.ray.io key-concepts, configuring-autoscaling and ray-cluster-configuration pages; documentation only, no commands were run.
