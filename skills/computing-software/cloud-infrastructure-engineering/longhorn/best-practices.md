---
id: computing-software.cloud-infrastructure-engineering.longhorn.best-practices
name: best-practices
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [best-practices, hardware, kernel, disks, scheduling]
level: practitioner
status: docs-checked
description: "Longhorn 1.13 recommended configuration: node sizing, supported Kubernetes and kernels, disk reservations, backups, CPU reservation and scheduling settings."
sources:
  - https://longhorn.io/docs/1.13.0/best-practices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply the documented production recommendations.

Hardware: V1 needs 3 nodes minimum with 4 vCPU and 4 GiB RAM each, SSD or NVMe preferred; V2 adds 1 dedicated core and 2 GiB for hugepages (1024 x 2 MiB), kernel 6.7+, modules `vfio_pci`, `uio_pci_generic`, `nvme-tcp`. On AWS burstable VMs, set `CpuCredits=unlimited` (the page gives this under the V2 data engine). AMD64 or ARM64; 10 Gbps between nodes.

Kubernetes: minimum v1.21; supported 1.33 to 1.36; CoreDNS at least 2 replicas.

Kernel: 5.8+ for filesystem optimisation, 5.17+ to freeze the filesystem for snapshots, 5.19+ for V2 NVMe/TCP. Avoid 6.5.6, 5.15.0-94, 6.5.0-21 and 6.5.0-1014-aws.

Disks:
- Use a dedicated disk, not the root disk.
- Root disk: minimal available storage 25%, over-provisioning 100%; dedicated disk: minimal available 10%.
- Aggregate several disks with LVM; persist extra disks in `/etc/fstab` and use `mount --bind`, not `ln -s`.
- V2 block disks: run `wipefs -a` first.

Operations:
- At least one recurring backup per volume, or one recurring snapshot if no backup target.
- Clean snapshots periodically and trim filesystems periodically.
- Enable only one data engine per cluster.
- Do not modify the default `longhorn` StorageClass; create a new one.
- Add liveness checks to ext4 workloads.

CPU: V1 Guaranteed Instance Manager CPU 12% by default.

Recommended settings: Replica Node Level Soft Anti-Affinity `false`, Allow Volumes Creation with Degraded Availability `false`, Replica Auto-Balance `least-effort`. Default priority class `longhorn-critical`.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/best-practices/

Changed: moved the AWS CpuCredits=unlimited advice from the V1 CPU line to the V2 data engine requirements, where the page puts it.

Method: documentation only; no commands were run.
