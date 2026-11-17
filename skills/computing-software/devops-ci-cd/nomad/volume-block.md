---
id: computing-software.devops-ci-cd.nomad.volume-block
name: volume-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, volume-block, volume, host-volume, csi-volume, dynamic-host-volume, per-alloc, sticky, access-mode, attachment-mode, mount-options, hcl]
level: practitioner
status: docs-checked
description: "Request storage for a Nomad group with the volume block for host, dynamic host and CSI volumes including source, sticky, per_alloc, access_mode, attachment_mode and mount_options."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/volume.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad volume block

`volume "<name>"` (group level) says the group needs a volume; the label is the name tasks use in `volume_mount` (`computing-software.devops-ci-cd.nomad.volume-mount-block`). The server only schedules the group onto nodes that can satisfy it: static host volumes in client config, dynamic host volumes (`volume create` / `volume register`), or CSI volumes.

```hcl
volume "data" {
  type            = "csi"
  source          = "csi-volume"
  read_only       = true
  attachment_mode = "file-system"
  access_mode     = "single-node-writer"
  per_alloc       = true
  mount_options {
    fs_type     = "ext4"
    mount_flags = ["noatime"]
  }
}
```

## Parameters
- `type` - `"host"` (static or dynamic host volume) or `"csi"`.
- `source` (required) - published host volume name, or the registered CSI volume ID.
- `read_only` (`false`) - default for the mount's `read_only`; also used for host volume ACL checks and scheduling.
- `sticky` (`false`) - dynamic host volumes only: reschedules and replacements keep receiving the same volume ID when available. Use for stateful deployments.
- `per_alloc` (`false`) - appends `[n]` (allocation index) to `source`: allocation `myjob.mygroup.mytask[0]` needs volume `myvolume[0]`. Cannot be true for system or sysbatch jobs or jobs using canaries; mutually exclusive with `sticky`. Prefer `sticky` for dynamic host volumes and `per_alloc` for CSI.
- `access_mode` and `attachment_mode` must together exactly match one of the volume's `capability` blocks. CSI: both required. `access_mode` is one of `single-node-reader-only`, `single-node-writer`, `multi-node-reader-only`, `multi-node-single-writer`, `multi-node-multi-writer` (most plugins only do single-node). `attachment_mode` is `file-system` or `block-device`. Dynamic host volumes: optional; access defaults to `single-node-writer` (or `single-node-reader-only` when `read_only = true`), attachment to `file-system`.
- `mount_options` (CSI file-system only) - `fs_type`, `mount_flags`; override the options given at volume registration.

## Gotcha: interpolation
The block is used for scheduling, so `${NOMAD_ALLOC_INDEX}` cannot appear in `source`; use `per_alloc = true` instead. HCL2 `${var.path}` is fine in task env and `destination`.

## Checked

2026-11-03. Confirmed against the volume job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
