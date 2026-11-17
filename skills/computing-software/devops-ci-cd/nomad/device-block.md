---
id: computing-software.devops-ci-cd.nomad.device-block
name: device-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, device-block, device, gpu, nvidia, fpga, device-plugin, count, device-attributes, units, resources, hcl]
level: advanced
status: docs-checked
description: "Request GPUs and other hardware in Nomad with the device block name forms, count, constraint and affinity on device attributes, and unit-aware comparisons like GiB."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/device.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad device block

`device` (inside `resources`) is both a scheduling and a runtime requirement for hardware attached to a node (GPUs, FPGAs, TPUs). Nomad places the task on a node with matching devices, then asks the client's device plugin how to mount them and what environment variables to expose (see that plugin's docs). Support is limited to Linux and container-based drivers (isolation per task).

```hcl
resources {
  device "nvidia/gpu" {
    count = 2

    constraint {
      attribute = "${device.attr.memory}"
      operator  = ">="
      value     = "2 GiB"
    }

    affinity {
      attribute = "${device.attr.memory}"
      operator  = ">="
      value     = "4 GiB"
      weight    = 75
    }
  }
}
```

Meaning: two Nvidia GPUs of any model, hard requirement of at least 2 GiB memory, preference for 4 GiB or more.

## Parameters
- Label/name forms: `<type>` (`gpu`, `fpga`), `<vendor>/<type>` (`nvidia/gpu`, `amd/gpu`), `<vendor>/<type>/<model>` (`nvidia/gpu/1080ti`).
- `count` (`1`) - number of device instances.
- `constraint` and `affinity` - repeatable; same syntax as the job-level blocks (`computing-software.devops-ci-cd.nomad.constraint-block`, `computing-software.devops-ci-cd.nomad.affinity-block`).

## Attributes usable in constraint and affinity
`${device.ids}` (comma-separated IDs), `${device.type}`, `${device.vendor}`, `${device.model}`, `${device.attr.<property>}` (for example `memory`). Which properties exist depends on the device plugin.

## Units
Devices report typed values with units (a GPU might report "4096 MiB"), so a constraint like "greater than 3.5 GiB" matches because Nomad converts units. Byte units supported: base 2 KiB, MiB, GiB, TiB, PiB, EiB and base 10 kB, KB, MB, GB, TB, PB, EB; byte-rate variants with `/s` exist too.

To keep a GPU on the same NUMA node as the task's cores see `computing-software.devops-ci-cd.nomad.numa-block`.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 device job specification page: name forms, count default 1, device attributes, byte and byte-rate units, Linux and container-driver limit, the example block. Nothing removed.

Method: documentation only; no commands were run.
