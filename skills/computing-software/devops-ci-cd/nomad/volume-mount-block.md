---
id: computing-software.devops-ci-cd.nomad.volume-mount-block
name: volume-mount-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, volume-mount, volume-mount-block, propagation-mode, selinux-label, destination, read-only, bind-mount, hcl]
level: practitioner
status: docs-checked
description: "Mount a group volume into a Nomad task with volume_mount using volume, destination, read_only, propagation_mode and selinux_label, and know the bidirectional propagation risk."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/volume_mount.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad volume_mount block

`volume_mount` (task level) mounts a group-level `volume` into the task.

```hcl
group "example" {
  volume "certs" {
    type      = "host"
    read_only = true
    source    = "ca-certificates"
  }
  task "example" {
    volume_mount {
      volume           = "certs"
      destination      = "/etc/ssl/certs"
      propagation_mode = "private"
    }
  }
}
```

## Parameters
- `volume` - name (label) of the group volume.
- `destination` - path inside the task's allocation.
- `read_only` (`false`) - narrow a writeable group volume to read-only for this mount. Default comes from the volume's `read_only`.
- `propagation_mode` (`"private"`) - `private`: task cannot see nested mounts; `host-to-task`: new mounts made outside the task become visible; `bidirectional`: task sees host mounts and can create its own (requires ReadWrite). The docs warn that `bidirectional` can damage the host if the task creates a mount and exits without cleaning it up.
- `selinux_label` - Linux only and driver-dependent: `Z` private/unshared content, `z` content shared among containers.

## Failure mode
The client fails the allocation if its configuration is changed to remove a volume that the allocation depends on.

Group-side setup is in `computing-software.devops-ci-cd.nomad.volume-block`.

## Checked

2026-11-03. Confirmed against the volume_mount job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
