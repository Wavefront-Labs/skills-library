---
id: computing-software.devops-ci-cd.nomad.ephemeral-disk-block
name: ephemeral-disk-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, ephemeral-disk, sticky, migrate, alloc-data, local-dir, disk-size, data-migration, cache, hcl]
level: practitioner
status: docs-checked
description: "Use the Nomad ephemeral_disk block with size, sticky and migrate, including the best-effort data migration limits, the unenforced size and what is lost on alloc stop."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/ephemeral_disk.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad ephemeral_disk block

`ephemeral_disk` (group level) describes the scratch disk shared by all tasks in the group. It is reachable inside the allocation under `alloc/data/`. Task logs are also written to it (`computing-software.devops-ci-cd.nomad.logs-block`).

```hcl
group "example" {
  ephemeral_disk {
    migrate = true
    size    = 500
    sticky  = true
  }
}
```

## Parameters (defaults)
- `size` (`300`) - MB. The current implementation does **not enforce** the limit, but it is used during job placement.
- `sticky` (`false`) - best effort to place the updated allocation on the same machine, moving the `local/` and `alloc/data` directories to the new allocation.
- `migrate` (`false`) - best effort copy of the previous allocation's data even when it ran on another client. Turning it on implies `sticky`. The task blocks from starting until the copy finishes.

## Migration limits
- Clients must reach each other directly over the Nomad HTTP port.
- Any transfer failure loses the data, so use it only for data you can recreate (cache). Migration is atomic: a partial copy is removed on error.
- No migration happens if the client garbage-collected a failed allocation or the allocation was stopped with `nomad alloc stop`, because the original allocation is already gone.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 ephemeral_disk job specification page: size default 300 and non-enforcement, sticky, migrate and its limits, alloc/data and log location. Removed: the overcommit inference and the use-volumes advice.

Method: documentation only; no commands were run.
