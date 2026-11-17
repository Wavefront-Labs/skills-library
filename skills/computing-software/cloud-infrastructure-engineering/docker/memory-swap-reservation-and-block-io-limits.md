---
id: computing-software.cloud-infrastructure-engineering.docker.memory-swap-reservation-and-block-io-limits
name: memory-swap-reservation-and-block-io-limits
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, resource-limits, memory-limit, memory-swap, memory-reservation, blkio, device-read-bps, io-limits, cgroups]
level: advanced
description: "Set --memory with --memory-swap and --memory-reservation correctly on cgroup v2, and throttle disk I/O with --device-read/write-bps/iops and blkio weight."
sources: ["https://docs.docker.com/engine/containers/resource_constraints/", "https://docs.docker.com/reference/cli/docker/container/run/", "https://github.com/compose-spec/compose-spec/blob/main/spec.md", "https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Memory swap/reservation and block I/O limits

## Memory flags
| Flag | Meaning |
|---|---|
| `--memory 1g` | hard memory limit |
| `--memory-swap 1g` | **total** memory+swap; if positive, `--memory` must also be set. Equal to `--memory` = no swap |
| `--memory-swap -1` | unlimited swap (up to what the host has) |
| `--memory-swap 0` | ignored (treated as unset) |
| unset (with `--memory` set) | swap up to the same amount as `--memory` (2x total) if the host has swap |
| `--memory-reservation 512m` | soft limit, must be lower than `--memory`; applies on host contention |
| `--memory-swappiness 0-100` | 0 turns off anonymous page swapping; default inherited from the host |

```sh
docker run --memory 1g --memory-swap 1g --memory-reservation 768m app:1
```
- Set `--memory-swap` equal to `--memory` to give a container no swap (the Docker docs note a performance penalty when applications swap often).
- Reservation must be lower than the limit; it only matters when the host is under pressure.
- `docker info` ends with `WARNING: No swap limit support` when the kernel lacks that capability; the Docker Engine troubleshooting guide covers enabling it.

## Block I/O
```sh
docker run --device-read-bps /dev/nvme0n1:50mb --device-write-bps /dev/nvme0n1:20mb \
  --device-write-iops /dev/nvme0n1:500 backup:1
docker run --blkio-weight 300 batch:1               # 10-1000 relative share
```
- Limits apply per **block device**, by path of the device holding the data (find with
  `df /var/lib/docker` -> `lsblk`). Throttling `/dev/sda` does nothing if writes hit `/dev/nvme0n1`.
- On cgroup v1 the throttling settings apply only to direct I/O; cgroup v2 has no such limitation (OCI runtime specification).

## Compose
```yaml
deploy:
  resources:
    limits: { memory: 1g }
    reservations: { memory: 768m }
memswap_limit: 1g
blkio_config:
  weight: 300
  device_write_bps: [{ path: /dev/nvme0n1, rate: 20mb }]
```

## Verify
```sh
docker inspect -f '{{.HostConfig.Memory}} {{.HostConfig.MemorySwap}} {{.HostConfig.MemoryReservation}}' app
docker stats --no-stream app
```

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master), the Compose specification, the OCI runtime specification (config-linux) and the Engine API swagger. Confirmed: `--memory-swap` semantics (positive needs `--memory`; equal to `--memory` means no swap; 0 ignored; -1 unlimited; unset gives twice `--memory` if the host has swap); `--memory-reservation` soft limit lower than `--memory`; `--memory-swappiness` 0-100, default inherited; `--blkio-weight` 10-1000; `--device-read-bps/-write-bps/-write-iops`; the `No swap limit support` warning; Compose `memswap_limit`, `blkio_config` (`weight`, `device_write_bps` with `path` and `rate`), `deploy.resources`; cgroup v1 throttles only direct I/O and v2 does not; `HostConfig.Memory`, `MemorySwap`, `MemoryReservation` in the API. Removed: cgroup v2 file mapping, `swapaccount=1`, memory.high, BFQ and weight-on-NVMe claims, overlay/volume accounting claim, cgroup file and dd verify commands.
Method: documentation only; no commands were run.
