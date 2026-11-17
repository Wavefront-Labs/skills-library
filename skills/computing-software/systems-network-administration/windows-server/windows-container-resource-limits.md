---
id: computing-software.systems-network-administration.windows-server.windows-container-resource-limits
name: windows-container-resource-limits
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, windows-container-resource-limits, docker, cpu-limits, memory-limits]
level: practitioner
status: docs-checked
description: "Limit CPU, memory and storage for Windows containers with docker run flags, understand process vs Hyper-V isolation behaviour, and check limits are applied."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/resource-controls
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/system-requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU and memory limits for Windows containers
By default containers are subject to normal fair-share Windows resource management. Resource controls are set on the
container's parent job object; with Hyper-V isolation they are applied to the virtual machine and to the job object
inside it.

## Flags (docker run) and what they map to
| Flag | Windows implementation |
|---|---|
| `--memory` | HCS MemoryMaximumInMB; shared kernel: job memory limit; Hyper-V isolation: VM memory |
| `--cpus` | HCS ProcessorCount; shared kernel: simulated with a hard-cap CPU rate; Hyper-V: number of virtual processors exposed |
| `--cpu-percent` | HCS ProcessorMaximum; hard-cap CPU rate; Hyper-V: hypervisor limit on virtual processors |
| `--cpu-shares` | HCS ProcessorWeight; weight-based CPU rate (job object weight range 1 to 9, default 5) |
| `--io-maxbandwidth`, `--io-maxiops` | storage IOPS and bandwidth limits via job object IO rate control |
| `--storage-opt size=` | HCS StorageSandboxSize (container scratch size) |

```powershell
docker run -d --name api --cpus 2 --memory 4g --storage-opt size=40G myregistry/api:1.4
docker stats --no-stream api
```
The memory cap must be high enough for the per-container system processes (user management, networking and so on); the
system requirements page has a table of minimum memory.

## Verify
- [ ] `docker stats` shows memory capped at the limit and CPU within the set share under load.

## Checked

2026-10-26 against the Windows containers resource controls page (Virtualization-Documentation, last commit 2026-10-20): the Docker flag to HCS to job object mapping for memory, CPU count, percent and shares, storage IO and sandbox size, Hyper-V isolation behaviour, CPU weight range, per-container system process memory note. Removed unconfirmed claims: the 20 GB default scratch size, `--cpu-count`, the rule that only one CPU flag is honoured, the default Hyper-V utility VM size, Kubernetes limit behaviour and OOM exit codes.

Method: documentation only; no commands were run.
