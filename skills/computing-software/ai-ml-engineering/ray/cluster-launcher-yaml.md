---
id: computing-software.ai-ml-engineering.ray.cluster-launcher-yaml
name: cluster-launcher-yaml
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-up, cluster-yaml, ray-down, head-node-type]
level: practitioner
status: docs-checked
description: "Launch Ray clusters on cloud VMs with the cluster launcher YAML: provider, available_node_types, setup commands, ray up/down/attach/exec."
sources:
  - https://docs.ray.io/en/latest/cluster/vms/getting-started.html
  - https://docs.ray.io/en/latest/cluster/vms/references/ray-cluster-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster launcher YAML

```yaml
# cluster.yaml
cluster_name: dev
max_workers: 10
upscaling_speed: 1.0
idle_timeout_minutes: 5
provider:
  type: aws
  region: us-west-2
auth:
  ssh_user: ubuntu
available_node_types:
  head:
    node_config:
      InstanceType: m5.2xlarge
    resources: {CPU: 2}
  gpu:
    min_workers: 0
    max_workers: 8
    node_config:
      InstanceType: g5.xlarge
    resources: {GPU: 1}
head_node_type: head
setup_commands:
  - pip install -U "ray[default]" torch
```

```bash
ray up -y cluster.yaml        # create or update
ray attach cluster.yaml       # ssh to the head node
ray exec cluster.yaml 'ray status'
ray down -y cluster.yaml
```

## Notes
- `head_node_type` names one key of `available_node_types`. Changing it, or the head type's `node_config`, and running `ray up` prompts to scale down the old head and restart the cluster.
- Changing a worker type's `node_config` and running `ray up` scales down its existing nodes and creates new ones; deleting a type scales all its nodes down.
- `resources` is required unless the provider is AWS or Kubernetes (auto-detected there). `node_config` is required per node type.
- Per-type `max_workers` defaults to the cluster-wide value; for the head type it defaults to 0. `min_workers` defaults to 0.
- `head_start_ray_commands` and `worker_start_ray_commands` have defaults; the head default includes `--autoscaling-config=~/ray_bootstrap_config.yaml`. Override only when needed.
- The reference advises avoiding long `setup_commands` by baking dependencies into an image, to cut startup time.
- For running work, the docs recommend Ray Jobs over `ray exec`.

## Verify
`ray exec cluster.yaml 'ray status'` lists the head and the expected workers.

## Checked
Checked 2026-11-09 against the Ray VM getting-started page and the cluster YAML configuration reference (field sections for available_node_types, head_node_type, setup and start commands, node type resources/min/max read). Removed unconfirmed items: the `ray submit` and `ray dashboard` commands, `--no-restart`, port list, same-version-join claim, the pinned Ray version and image ID placeholders, and the CPU 0 head comment.

Method: docs-checked 2026-11-09 against docs.ray.io vms getting-started and ray-cluster-configuration pages; documentation only, no commands were run.
