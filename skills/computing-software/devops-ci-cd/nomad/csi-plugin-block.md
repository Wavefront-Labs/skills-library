---
id: computing-software.devops-ci-cd.nomad.csi-plugin-block
name: csi-plugin-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, csi-plugin-block, csi-plugin, csi, node-plugin, controller-plugin, monolith, health-timeout, mount-dir, privileged, system-job, hcl]
level: advanced
status: docs-checked
description: "Run a CSI storage plugin as a Nomad task with csi_plugin id, type node controller or monolith, mount_dir, stage_publish_base_dir and health_timeout, and deploy it safely."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/csi_plugin.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad csi_plugin block

A task with `csi_plugin` declares that it provides a Container Storage Interface plugin; Nomad registers it so other jobs can claim volumes through it.

```hcl
csi_plugin {
  id             = "aws-efs0"
  type           = "node"
  mount_dir      = "/csi"
  health_timeout = "30s"
}
```

## Parameters
- `id` (required) - plugin ID. Controller and node instances of one plugin must share the same ID.
- `type` (required) - `node` (needed on every client that mounts volumes), `controller` (talks to the storage provider's API; some plugins need it), or `monolith` (both roles).
- `mount_dir` - path inside the container where the plugin expects its Unix socket; match the plugin's `--endpoint` argument (`unix://csi/csi.sock` with `mount_dir = "/csi"`). Usually not required.
- `stage_publish_base_dir` - base directory for staging and publishing volumes. Cannot be a subdirectory of `mount_dir`.
- `health_timeout` (`30s`) - how long the supervisor waits before restarting an unhealthy plugin.

## Privileges
`node` and `monolith` plugins need root (or `CAP_SYS_ADMIN`) to mount volumes. With the Docker driver set `privileged = true`; no other default driver has that option. Controller plugins do not need it.

## Deployment guidance
- Plugins are not in the data path: tasks use a bind mount. But Nomad must talk to the plugin on a node to unmount when an allocation stops, so stop volume-claiming jobs before stopping the `node` or `monolith` plugin. `nomad node drain` drains plugin tasks last automatically.
- Only the most recently placed allocation per plugin ID and type is used by a client. Run node plugins as `type = "system"` jobs and spread controllers using a `distinct_hosts` constraint (`value = true`).
- Some plugins (AWS EBS) create volumes only in their own availability zone; use `topology_request` in the volume spec as that plugin's docs say.

## Checked

2026-11-03. Confirmed against the csi_plugin job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
